from django.shortcuts import render, redirect, get_object_or_404
from .models import Elon, ImageElon, CustomUser, Like
from .forms import RegisterForm, AddElonForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from decimal import Decimal
from django.http import JsonResponse

# Dashboard routing hub

def dashboard_router(request, view_name, **kwargs):
    routes = {
        'home': home,
        'register': register_view,
        'login': login_view,
        'logout': logout_view,
        'profile': profile_view,
        'add_elon': add_elon_view,
        'delete_elon': delete_elon_view,
        'update_elon': update_elon_view,
    }
    view = routes.get(view_name)
    if not view:
        return redirect('home')
    return view(request, **kwargs)


def home(request):
    elonlar = Elon.objects.all().prefetch_related('images')

    brand = request.GET.get('brand', '').strip()
    model = request.GET.get('model', '').strip()
    year_str = request.GET.get('year', '').strip()
    price = request.GET.get('price', '').strip()
    motor = request.GET.get('motor', '').strip()

    if brand:
        elonlar = elonlar.filter(brand=brand)
    if model:
        elonlar = elonlar.filter(model__icontains=model)
    if year_str:
        try:
            year = int(year_str)
            elonlar = elonlar.filter(year=year)
        except (ValueError, TypeError):
            pass
    if price:
        try:
            elonlar = elonlar.filter(price=Decimal(price))
        except (ValueError, TypeError):
            pass
    if motor:
        elonlar = elonlar.filter(motor=motor)

    context = {
        'elonlar': elonlar,
        'BRAND_CHOICES': Elon.BRAND_CHOICES,
        'MOTOR_CHOICES': Elon.MOTOR_CHOICES,
        'selected_brand': brand,
        'selected_model': model,
        'selected_year': year_str,
        'selected_price': price,
        'selected_motor': motor,
    }
    return render(request, 'home.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def profile_view(request):
    user = request.user
    user_elons = Elon.objects.filter(owner=user).prefetch_related('images') if user.is_authenticated else Elon.objects.none()
    context = {
        'user_elons': user_elons
    }
    return render(request, 'profile.html', context)

def liked_elons_view(request):
    user = request.user
    liked_elons = Elon.objects.filter(likes__user=user).prefetch_related('images').distinct()
    return render(request, 'liked_elons.html', {'liked_elons': liked_elons})

def toggle_like(request, elon_id):
    if request.method != 'POST' or not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Ruxsat berilmagan'}, status=403)
    elon = get_object_or_404(Elon, id=elon_id)
    like, created = Like.objects.get_or_create(user=request.user, elon=elon)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    liked_count = elon.likes.count()
    return JsonResponse({'status': 'ok', 'liked': liked, 'liked_count': liked_count})

def logout_view(request):
    logout(request)
    return redirect('home')

def add_elon_view(request):
    if request.method == 'POST':
        form = AddElonForm(request.POST)
        if form.is_valid():
            elon = form.save(commit=False)
            elon.owner = request.user
            elon.save()
            for image in request.FILES.getlist('images'):
                ImageElon.objects.create(elon=elon, image=image)
            return redirect('profile')
    else:
        form = AddElonForm()
    return render(request, 'add_elon.html', {'form': form})

def delete_elon_view(request, elon_id):
    elon = get_object_or_404(Elon, id=elon_id, owner=request.user)
    if request.method == 'POST':
        elon.delete()
        return redirect('profile')
    user_elons = Elon.objects.filter(owner=request.user).prefetch_related('images') if request.user.is_authenticated else Elon.objects.none()
    return render(request, 'profile.html', {'user_elons': user_elons})

def update_elon_view(request, elon_id):
    elon = get_object_or_404(Elon, id=elon_id, owner=request.user)
    if request.method == 'POST':
        form = AddElonForm(request.POST, instance=elon)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AddElonForm(instance=elon)
    context = {
        'form': form,
        'elon': elon,
        'is_update': True,
    }
    return render(request, 'add_elon.html', context)