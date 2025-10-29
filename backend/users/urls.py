# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    MyTokenObtainPairView,
    LogoutView,
    UserProfileView,
    UserDetailView,
    StaffDashboardView,
    ChangePasswordView
)

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # Staff-only endpoints
    path('staff/users/', StaffDashboardView.as_view(), name='staff-users'),
    
    # User detail
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
