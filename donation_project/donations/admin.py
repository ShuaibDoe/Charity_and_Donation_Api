from django.contrib import admin
from .models import NGO, Campaign, Donation

admin.site.register(NGO)
admin.site.register(Campaign)
admin.site.register(Donation)