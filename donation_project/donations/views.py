from django.conf import settings
from django.db.models import Sum
from django.core.mail import send_mail

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NGO, Campaign, Donation
from .serializers import NGOSerializer, CampaignSerializer, DonationSerializer
from .permissions import IsAdmin, IsNGO, IsDonor

# --- NGO creation (NGO users only); Admin approves later ---
class NGOCreateView(generics.CreateAPIView):
    serializer_class = NGOSerializer
    permission_classes = [IsNGO]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, approved=False)

# --- Admin: approve NGOs ---
class NGOApproveView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            ngo = NGO.objects.get(pk=pk)
        except NGO.DoesNotExist:
            return Response({"detail": "NGO not found."}, status=404)
        ngo.approved = True
        ngo.save()
        return Response({"detail": "NGO approved."})

# --- Campaigns (NGO owners only) ---
class CampaignCreateView(generics.CreateAPIView):
    serializer_class = CampaignSerializer
    permission_classes = [IsNGO]

    def perform_create(self, serializer):
        # Only allow campaigns for approved NGO of the current user
        ngo = NGO.objects.filter(owner=self.request.user, approved=True).first()
        if not ngo:
            raise PermissionError("You must have an approved NGO to create a campaign.")
        serializer.save(ngo=ngo)

class CampaignListView(generics.ListAPIView):
    serializer_class = CampaignSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Campaign.objects.filter(active=True, ngo__approved=True)

# --- Donations (Donor only) ---
class DonationCreateView(generics.CreateAPIView):
    serializer_class = DonationSerializer
    permission_classes = [IsDonor]

    def perform_create(self, serializer):
        donation = serializer.save(donor=self.request.user, paid=True)  # mark as paid in this simple version
        # Send a basic email notification (console backend in dev)
        try:
            send_mail(
                subject="Donation Received",
                message=f"Thank you for donating {donation.amount} to {donation.campaign.title}.",
                from_email="no-reply@charity.local",
                recipient_list=[self.request.user.email] if self.request.user.email else [],
                fail_silently=True,
            )
        except Exception:
            pass

# --- NGO Dashboard (NGO only) ---
class NGODashboardView(APIView):
    permission_classes = [IsNGO]

    def get(self, request):
        ngo = NGO.objects.filter(owner=request.user, approved=True).first()
        if not ngo:
            return Response({"detail": "No approved NGO for this user."}, status=404)

        total = Donation.objects.filter(campaign__ngo=ngo, paid=True).aggregate(total=Sum("amount"))["total"] or 0
        campaigns = Campaign.objects.filter(ngo=ngo).count()
        donations_count = Donation.objects.filter(campaign__ngo=ngo, paid=True).count()
        return Response({
            "ngo": ngo.name,
            "approved": ngo.approved,
            "total_donations": str(total),
            "campaigns_count": campaigns,
            "donations_count": donations_count,
        })

# --- Leaderboard (top donors) ---
class LeaderboardView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = Donation.objects.filter(paid=True).values("donor__username").annotate(total=Sum("amount")).order_by("-total")[:10]
        return Response(list(qs))
