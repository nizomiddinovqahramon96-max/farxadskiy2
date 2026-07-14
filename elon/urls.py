from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('add_elon/', views.add_elon_view, name='add_elon'),
    path('elon/<int:elon_id>/delete/', views.delete_elon_view, name='delete_elon'),
    path('elon/<int:elon_id>/update/', views.update_elon_view, name='update_elon'),
    path('elon/update/<int:elon_id>/', views.update_elon_view, name='update_elon_alt'),
    path('elon/<int:elon_id>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('liked-elons/', views.liked_elons_view, name='liked_elons'),
]