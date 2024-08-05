from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.http import Http404
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

    def get_readonly_fields(self, request, obj=None):
        """ Оставляю персоналу все поля для чтения кроме is_active что бы он мог блокировать пользователей """

        if not request.user.has_perm('users.can_view_all_fields'):
            active_fields = {
                'is_active',
            }
            readonly_fields = [field.name for field in self.model._meta.get_fields() if field.name not in active_fields]
            return readonly_fields
        return []

    def get_queryset(self, request):
        """ Для персонала исключил всех кроме пользователей, что бы они не могли банить друг друга """

        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False, is_staff=False)
        return queryset

    def get_object(self, request, object_id, from_field=None):
        """ Для персонала отключил возможность просматривать персонал прыгая по урлам в админке """

        obj = super().get_object(request, object_id, from_field)
        if not request.user.has_perm('can_view_is_staff'):
            if obj is None:
                raise Http404('Пользователь не существует')
            elif obj.is_staff or obj.is_superuser:
                raise Http404('Недостаточно прав для просмотра этого пользователя')
        return obj


admin.site.register(User, CustomUserAdmin)


