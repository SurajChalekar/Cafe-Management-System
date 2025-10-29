# users/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer
)
from .permissions import IsStaffUser, IsOwnerOrStaff

User = get_user_model()

# ------------------------
# Logout
# ------------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ------------------------
# Custom JWT Token with role info
# ------------------------
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'username': self.user.username,
            'role': getattr(self.user, 'role', None),
            'is_staff': self.user.is_staff_member(),
        })
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ------------------------
# User Registration
# ------------------------
class RegisterView(generics.CreateAPIView):
    """
    Register a new user
    POST /api/v1/auth/register/
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


# ------------------------
# User Profile
# ------------------------
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update logged-in user's profile
    GET/PUT/PATCH /api/v1/auth/profile/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'user': serializer.data,
            'message': 'Profile updated successfully'
        })


# ------------------------
# Change Password
# ------------------------
class ChangePasswordView(generics.UpdateAPIView):
    """
    Change password for logged-in user
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


# ------------------------
# Staff Dashboard
# ------------------------
class StaffDashboardView(generics.ListAPIView):
    """
    List all users (staff only)
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get_queryset(self):
        return User.objects.all().order_by('-created_at')


# ------------------------
# User Details
# ------------------------
class UserDetailView(generics.RetrieveAPIView):
    """
    Retrieve user details (object-level permission)
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        return User.objects.all()
