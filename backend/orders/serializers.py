from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem


# ---------------------- Cart Serializers ----------------------
class CartItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(source='menu_item.id', read_only=True)
    item_name = serializers.ReadOnlyField(source='menu_item.name')
    price = serializers.ReadOnlyField(source='menu_item.price')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'menu_item', 'item_id', 'item_name', 'price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'items', 'total_price', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return obj.total_price()


# ---------------------- Order Serializers ----------------------
class OrderItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(source='menu_item.id', read_only=True)
    item_name = serializers.ReadOnlyField(source='menu_item.name')
    price = serializers.ReadOnlyField(source='menu_item.price')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'item_id', 'item_name', 'price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.menu_item.price


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    customer = serializers.ReadOnlyField(source='customer.username')
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_items', 'total_price', 'status', 'created_at', 'updated_at']
