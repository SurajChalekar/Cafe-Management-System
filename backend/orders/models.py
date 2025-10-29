from django.db import models
from django.conf import settings
from menu.models import MenuItem
from django.utils import timezone

class GlobalSettings(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1)
    allow_orders = models.BooleanField(default=True)

    def __str__(self):
        return f"Allow Orders: {self.allow_orders}"
    
    
# ---------------------- Cart Models ----------------------
class Cart(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum([item.total_price() for item in self.items.all()])

    def __str__(self):
        return f"Cart of {self.customer}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.menu_item.name}"


# ---------------------- Order Models ----------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('served', 'Served'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    menu_items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        total = sum([oi.quantity * oi.menu_item.price for oi in self.order_items.all()])
        self.total_price = total
        self.save()
        return total

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.menu_item.name}"
