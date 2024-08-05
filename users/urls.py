from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .apps import UsersConfig
from .views import RegisterView, verify_email, PasswordResetView, ProfileUpdateView, UserLogoutView, CustomLoginView


app_name = UsersConfig.name

urlpatterns = [
    #path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
#    path('login2/', UserLoginForm(), name='login2'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_update'),


]