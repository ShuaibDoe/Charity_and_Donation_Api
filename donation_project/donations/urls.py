from django.urls import path
from .views import (
    NGOCreateView, NGOApproveView,
    CampaignCreateView, CampaignListView,
    DonationCreateView, NGODashboardView, LeaderboardView
)

urlpatterns = [
    path("ngos/create/", NGOCreateView.as_view(), name="ngo-create"),
    path("ngos/<int:pk>/approve/", NGOApproveView.as_view(), name="ngo-approve"),

    path("campaigns/", CampaignListView.as_view(), name="campaign-list"),
    path("campaigns/create/", CampaignCreateView.as_view(), name="campaign-create"),

    path("donations/create/", DonationCreateView.as_view(), name="donation-create"),
    path("ngo/dashboard/", NGODashboardView.as_view(), name="ngo-dashboard"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
]
