from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


# -------------------- CartItem Inline --------------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ('total_price',)
    can_delete = True
    verbose_name = "Cart Item"
    verbose_name_plural = "Cart Items"


# -------------------- Cart Admin --------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price_display', 'created_at', 'updated_at')
    search_fields = ('customer__username', 'customer__email')
    inlines = [CartItemInline]
    list_per_page = 20

    def total_price_display(self, obj):
        return obj.total_price()
    total_price_display.short_description = 'Total Price'


# -------------------- OrderItem Inline --------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('item_price',)

    def item_price(self, obj):
        return obj.item.price * obj.quantity
    item_price.short_description = 'Item Total'


# -------------------- Order Admin --------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'customer__email')
    inlines = [OrderItemInline]
    readonly_fields = ('total_price',)
    list_per_page = 20
