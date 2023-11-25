"""
Database models.
"""
from django.utils import timezone
import random
import string
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Content(models.Model):
    """Text Content object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    # set current time and don't change it with updates
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    # set current time and change it it with updates
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)
    pin = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pin:
            self.pin = self.generate_unique_pin()
        super(Content, self).save(*args, **kwargs)

    def generate_unique_pin(self):
        while True:
            # Generate a random string of 6 characters (letters and digits)
            pin = ''.join(random.choices(string.ascii_letters
                                         + string.digits, k=6))
            if not Content.objects.filter(pin=pin).exists():
                return pin

    def __str__(self):
        return self.title
