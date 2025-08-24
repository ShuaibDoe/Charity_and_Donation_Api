from rest_framework import serializers
from .models import Donation, Campaign, NGO

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = "__all__"

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = "__all__"

class NGOSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        fields = "__all__"
