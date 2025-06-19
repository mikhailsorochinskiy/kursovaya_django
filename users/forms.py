from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'avatar', 'country', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    "Форма входа с email"

    username = forms.EmailField(label="Email")
