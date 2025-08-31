from rest_framework import serializers
from .models import NGO, Campaign, Donation

class NGOSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        fields = ["id", "owner", "name", "description", "approved"]
        read_only_fields = ["owner", "approved"]

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["id", "ngo", "title", "description", "target_amount", "active"]
        read_only_fields = ["ngo"]

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ["id", "donor", "campaign", "amount", "created_at", "paid"]
        read_only_fields = ["donor", "created_at", "paid"]
