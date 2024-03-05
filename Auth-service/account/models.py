from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
from django.db import models


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username