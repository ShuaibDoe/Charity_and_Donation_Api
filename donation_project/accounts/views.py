from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import (
    UserRegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)
