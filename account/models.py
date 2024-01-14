from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

  email = models.EmailField( unique=True, max_length=254)
  username = models.CharField(unique=True, max_length=50)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  gender = models.CharField(max_length=20, null=True, blank=True)
  phone = models.CharField(max_length=15, null=True, blank=True)
  is_email_verified = models.BooleanField(default=False)

  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)


  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  objects = CustomUserManager()

  def __str__(self):
      return self.email