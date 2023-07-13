from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, password, **extra_fields):
        if not user_name:
            raise ValueError('The UserName must be set')
        email = self.normalize_email(user_name)
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(user_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=16)
    user_name = models.CharField(max_length=56, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.user_name
