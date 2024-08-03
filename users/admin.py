from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.urls import path
from django.utils.http import unquote
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .forms import UserRegisterForm, UpdateUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    form = UpdateUserChangeForm
    change_password_form = AdminPasswordChangeForm
    model = User
    list_display = ['email', 'avatar', 'last_login', 'is_active', 'is_superuser', 'is_staff']

    fieldsets = (
        (None, {'fields': ('email', 'password', 'avatar', 'groups', 'user_permissions')}),
        ('Permissions', {'fields': ('is_manager', 'is_active', 'is_staff')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'avatar', 'is_manager', 'is_active', 'groups', 'user_permissions')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
