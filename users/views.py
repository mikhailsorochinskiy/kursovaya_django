from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.views.generic import CreateView, FormView, TemplateView, UpdateView, DetailView, ListView
from .forms import UserRegisterForm, LoginForm, PwdResetForm, UserPwdResetConfirmForm, UserUpdateForm
from .models import User
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.contrib.auth import views as auth_views, update_session_auth_hash, login, authenticate
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404, redirect, render, Http404


# Create your views here.
class UserListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = User.objects.all()
        if self.request.user.is_superuser:
            return queryset.exclude(is_superuser=True)
        if self.request.user.has_perm('mailings.can_view_mailing'):
            perm = Permission.objects.get(
                codename='can_view_mailing',
                content_type__app_label='mailings'
            )
            return queryset.exclude(
                Q(is_superuser=True) |
                Q(user_permissions=perm) |
                Q(groups__permissions=perm)
            ).distinct()
        raise PermissionDenied


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


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        if self.request.user.has_perm('mailings.can_view_mailing'):
            return user
        if user != self.request.user:
            raise PermissionDenied("Вы не можете смотреть данные чужого пользователя.")
        return user


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'

    def get_success_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        if user == self.request.user:
            return UserUpdateForm
        # if user.has_perm('catalog.can_unpublish_product') and user.has_perm('catalog.delete_product'):
        #     return ProductModeratorForm
        raise PermissionDenied


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


class PwdResetView(FormView):
    form_class = PwdResetForm
    template_name = 'users/pwd_reset_form.html'
    success_url = reverse_lazy('users:pwd_reset_done')  # Используйте имя URL без параметров

    def form_valid(self, form):
        email = form.cleaned_data['email']
        # Сохраните email в сессии, если нужно использовать его в PwdResetDone
        self.request.session['reset_email'] = email

        user = User.objects.get(email=email)
        token = user.generate_verification_token()
        user.is_active = False
        user.save()

        verification_link = f"http://{settings.DOMAIN}/users/password_reset/confirm/{token}/"
        send_mail(
            "Смена пароля",
            f"Перейдите по ссылке для смены пароля: {verification_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class PwdResetDone(TemplateView):
    template_name = 'users/pwd_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session.get('reset_email', '')
        return context


class PwdResetConfirmView(FormView):
    form_class = UserPwdResetConfirmForm
    template_name = "users/pwd_reset_confirm.html"
    success_url = reverse_lazy('users:login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.get_user_by_token()
        kwargs['user'] = user  # Передаем пользователя в форму
        return kwargs

    def get_user_by_token(self):
        token = self.kwargs.get('token')
        try:
            user = User.objects.get(verification_token=token)
            return user
        except User.DoesNotExist:
            raise Http404("Недействительная ссылка для сброса пароля")

    def form_valid(self, form):
        user = form.save()  # Сохраняем новый пароль
        user.is_active = True  # Активируем аккаунт (если нужно)
        user.verification_token = ""  # Очищаем токен
        user.save()
        messages.success(self.request, "Пароль успешно изменён!")
        return super().form_valid(form)


def activate_deactivate_user(request, user_id):
    """Контролер активирует деактивированного и деактивирует активированного"""
    if request.user.is_superuser or request.user.has_perm('mailings.can_view_mailing'):
        if request.method == "POST":
            print('aaa')
            user = User.objects.get(id=user_id)
            if user.is_active:
                user.is_active = False
                user.save()
                print('aaa')
            else:
                user.is_active = True
                user.save()
        return redirect('users:users')
    raise PermissionDenied