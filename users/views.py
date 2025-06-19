from django.conf import settings
from django.contrib import messages
from django.views.generic import CreateView, FormView, TemplateView
from .forms import UserRegisterForm, LoginForm
from .models import User
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth import views as auth_views, update_session_auth_hash, login, authenticate
from django.shortcuts import get_object_or_404, redirect, render


# Create your views here.
class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('mailings:home')

    def form_valid(self, form):
        user = form.save()
        token = user.generate_verification_token()
        user.is_active = False
        user.save()

        verification_link = f"http://{settings.DOMAIN}/users/verify/{token}/"
        send_mail(
            "Подтверждение регистрации в сервисе рассылок",
            f"Перейдите по ссылке для подтверждения: {verification_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(
            self.request, "Письмо с подтверждением отправлено на вашу электронную почту"
        )
        return super().form_valid(form)


class LoginView(FormView):
    "Аутентификация пользователя"

    form_class = LoginForm
    template_name = "users/login.html"

    def get_success_url(self):
        return self.request.POST.get('next', reverse_lazy('mailings:home'))

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, "Подтвердите ваш адрес электронной почты")
            return redirect("login")

        login(self.request, user)

        return super().form_valid(form)


class VerifyEmailView(TemplateView):
    """Подтверждение email по токену"""

    template_name = "users/verify_email.html"

    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
            user.is_active = True
            user.verification_token = ""
            user.save()
            messages.success(request, "Ваша электронная почта успешно подтверждена.")
            return redirect("users:login")
        except User.DoesNotExist:
            messages.error(request, "Недействительная ссылка подтверждения.")
            return redirect("users:register")
