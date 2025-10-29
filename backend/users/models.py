from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    """
    Custom User model for the café management system.
    """
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer',
        help_text='User role in the system'
    )
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, help_text='Delivery/contact address')
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [models.Index(fields=['role'])]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_staff_member(self):
        """Check if user is staff or admin"""
        return self.role in ['staff', 'admin']

    def is_admin(self):
        return self.role == 'admin'

    def get_full_name(self):
        """Return first_name + last_name or fallback to username"""
        return super().get_full_name() or self.username
