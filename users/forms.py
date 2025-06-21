from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'avatar', 'country', 'password1', 'password2')


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone_number', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Удаляем поле пароля и связанные с ним поля
        del self.fields['password']


class UserPwdResetConfirmForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        # Удаляем поле старого пароля (оставляем только new_password1 и new_password2)
        del self.fields['old_password']
    class Meta:
        fields = ('new_password1', 'new_password2')


class LoginForm(AuthenticationForm):
    "Форма входа с email"

    username = forms.EmailField(label="Email")


class PwdResetForm(forms.Form):
    email = forms.EmailField(help_text='Введите почту, на которую будет отправлено письмо с подтверждением о смене пароля')