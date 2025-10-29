from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class GlobalSettings(models.Model):
    allow_orders = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Allow Orders: {self.allow_orders}"

    class Meta:
        verbose_name = "Global Setting"
        verbose_name_plural = "Global Settings"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='items',
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    preparation_time = models.IntegerField(
        help_text="Time in minutes", default=15, validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['is_available']),
        ]

    def __str__(self):
        category_name = self.category.name if self.category else "Uncategorized"
        return f"{self.name} ({category_name}) - ₹{self.price}"

    @property
    def price_in_rupees(self):
        """Return price formatted in ₹"""
        return f"₹{self.price}"