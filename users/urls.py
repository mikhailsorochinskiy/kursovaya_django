from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UserCreateView, LoginView, VerifyEmailView

app_name = 'users'

urlpatterns = [
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailings:home'), name='logout'),
    path("verify/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
]
