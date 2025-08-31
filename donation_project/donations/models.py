from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class NGO(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ngos")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Campaign(models.Model):
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name="campaigns")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.ngo.name})"

class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="donations")
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=True)  # In real payment, set after payment webhook

    def __str__(self):
        return f"{self.donor} -> {self.campaign} : {self.amount}"
