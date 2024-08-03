from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from django.utils import timezone
import uuid
from utils.const import NULLABLE


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле Электронная почта должно быть заполнено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_manager', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_manager') is not True:
            raise ValueError('Superuser must have is_manager=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='email')
    avatar = models.ImageField(upload_to='avatars/', **NULLABLE, verbose_name='Аватар')
    token = models.UUIDField(default=uuid.uuid4, unique=True, **NULLABLE, verbose_name='Токен')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    last_login = models.DateTimeField(**NULLABLE, verbose_name='Дата последнего входа')
    is_staff = models.BooleanField(default=False, **NULLABLE, verbose_name='Пользователь')
    is_active = models.BooleanField(default=False, verbose_name='Пользователь активен')
    is_manager = models.BooleanField(default=False, blank=True, null=True, verbose_name='Менеджер')  # права менеджера

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        permissions = [
            ('can_view_all_fields', 'Может просматривать всю админку'),
            ('can_view_is_staff', 'Может просматривать персонал'),
        ]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



