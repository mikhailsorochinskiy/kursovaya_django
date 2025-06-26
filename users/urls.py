from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (UserCreateView, LoginView, VerifyEmailView, PwdResetView, PwdResetDone, PwdResetConfirmView,
                    UserDetailView, UserUpdateView, UserListView, activate_deactivate_user)

app_name = 'users'

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailings:home'), name='logout'),
    path("verify/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("password_reset/", PwdResetView.as_view(), name="pwd_reset"),
    path("password_reset/done/", PwdResetDone.as_view(), name="pwd_reset_done"),
    path("password_reset/confirm/<str:token>/", PwdResetConfirmView.as_view(), name="pwd_reset_confirm"),
    path("user/info/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user/update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("users/", UserListView.as_view(), name="users"),
    path("user/<int:user_id>/is_active/", activate_deactivate_user, name="user_active"),
]
