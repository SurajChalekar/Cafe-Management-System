from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "order_id",
        "payment_id",
        "amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("order_id", "payment_id", "user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("User Info", {"fields": ("user",)}),
        ("Payment Details", {"fields": ("order_id", "payment_id", "amount", "status")}),
        ("Timestamps", {"fields": ("created_at",)}),
    )
