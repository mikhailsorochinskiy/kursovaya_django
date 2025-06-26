from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text='Введите номер телефона',
                                    verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name="Аватар",
                               help_text='Загрузите фото для вашей аватарки')
    country = models.CharField(max_length=50, blank=True, null=True, help_text='Ваша страна', verbose_name='Страна')
    is_active = models.BooleanField(default=True, null=True, blank=True)
    verification_token = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def generate_verification_token(self):
        "Генерация и сохранение токена верификации"
        self.verification_token = secrets.token_urlsafe(32)
        self.save()
        return self.verification_token
