from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role='Donor', **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        return self.create_user(username, password, role='Admin', **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('NGO', 'NGO'),
        ('Donor', 'Donor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Donor')

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"
