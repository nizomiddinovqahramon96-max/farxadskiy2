from django.forms import ModelForm
from .models import Elon, ImageElon, CustomUser
from django import forms

class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'password', 'avatar']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class AddElonForm(ModelForm):

    class Meta:
        model = Elon
        fields = ['title', 'brand', 'model', 'color', 'year', 'price', 'km', 'xolat', 'motor']