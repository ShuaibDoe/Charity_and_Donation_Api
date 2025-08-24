from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings
import stripe
from .models import Donation, Campaign, NGO
from .serializers import DonationSerializer, CampaignSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

#  Permission Checks
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Admin"

class IsNGO(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "NGO"

class IsDonor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Donor"


#  Create Donation (Email Notification)
class DonationCreateView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated, IsDonor]

    def perform_create(self, serializer):
        donation = serializer.save(donor=self.request.user)

        send_mail(
            subject="New Donation Received",
            message=f"Your NGO received a donation of ${donation.amount}.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[donation.campaign.ngo.email],
        )


#  NGO Dashboard
class NGODashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNGO]

    def get(self, request):
        total_donations = Donation.objects.filter(
            campaign__ngo__email=request.user.email
        ).aggregate(total=Sum("amount"))["total"] or 0

        return Response({
            "ngo": request.user.username,
            "total_donations": total_donations
        })


#  Donation Leaderboard
class LeaderboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        leaderboard = (
            Donation.objects.values("donor__username")
            .annotate(total_donated=Sum("amount"))
            .order_by("-total_donated")[:10]
        )
        return Response(leaderboard)


#  Stripe Payment Integration
class CreateCheckoutSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDonor]

    def post(self, request):
        amount = request.data.get("amount")
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Donation"},
                    "unit_amount": int(amount) * 100,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="http://localhost:8000/success/",
            cancel_url="http://localhost:8000/cancel/",
        )
        return Response({"session_url": session.url})

