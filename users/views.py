from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UpdateUserChangeForm, StyledAuthenticationForm, StyledPasswordResetForm, \
    ProfileUpdateForm
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse


class CustomLoginView(LoginView):
    form_class = StyledAuthenticationForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация',
    }


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:register')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):

        response = super().form_valid(form)
        user = form.save()
        user.is_active = False  # Деактивируем пользователя до подтверждения почты
        user.save()
        # Отправка подтверждающего письма
        verification_link = self.request.build_absolute_uri(
            reverse_lazy('users:verify_email', kwargs={'token': user.token})
        )
        send_mail(
            'Подтверждение регистрации',
            f'Перейдите по ссылке для подтверждения регистрации: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        # Проверяем, было ли отправлено письмо
        if response.status_code == 302:  # Статус код 302 означает успешное перенаправление
            # Сообщение об успешной отправке письма
            messages.success(self.request, 'Регистрация прошла успешно! Подтвердите свой email для активации аккаунта.')
        else:
            messages.error(self.request, 'Произошла ошибка при отправки письма')

        return response


def verify_email(request, token):
    try:
        user = get_object_or_404(User, token=token)
        user.is_active = True
        user.save()
        # return HttpResponse('Email verified successfully!')
        return redirect(reverse('users:login'))
    except User.DoesNotExist:
        return HttpResponse('Invalid verification token', status=400)


class PasswordResetView(FormView):
    template_name = 'users/password_reset.html'
    form_class = StyledPasswordResetForm
    success_url = reverse_lazy('users:password_reset')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            new_password = get_random_string(8)
            user.password = make_password(new_password)
            user.save()
            send_mail(
                'Восстановление пароля',
                f'Ваш новый пароль: {new_password}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            #  Проверяем, было ли отправлено письмо
        if response.status_code == 302:  # Статус код 302 означает успешное перенаправление
            #  Сообщение об успешной отправке письма
            messages.success(self.request, 'Письмо для сброса пароля отправлено. Пожалуйста, проверьте вашу почту.')
        else:
            messages.error(self.request, 'Произошла ошибка при отправке письма для сброса пароля.')

        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('main:main')

    def get_object(self, queryset=None):
        return self.request.user


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('mailer:home')
