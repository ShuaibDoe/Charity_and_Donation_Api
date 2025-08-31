from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "Admin", "Admin"
        NGO = "NGO", "NGO"
        DONOR = "Donor", "Donor"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.DONOR)

    def __str__(self):
        return f"{self.username} ({self.role})"
