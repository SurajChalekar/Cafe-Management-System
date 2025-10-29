from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Cart, CartItem, Order, OrderItem, GlobalSettings
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer
from .permissions import IsStaffUser, IsCustomerUser, IsOwnerOrStaff
from menu.models import MenuItem
from menu.models import GlobalSettings
from users.permissions import IsStaffUser

class GlobalOrderStatusView(APIView):
    permission_classes = [permissions.AllowAny]  # or IsAuthenticated if needed

    def get(self, request):
        settings, _ = GlobalSettings.objects.get_or_create(id=1)
        return Response({'allow_orders': settings.allow_orders})

class GlobalSettingsView(APIView):
    permission_classes = [permissions.IsAdminUser]  # or [IsStaffUser] if you created one

    def get(self, request):
        settings, _ = GlobalSettings.objects.get_or_create(id=1)
        return Response({'allow_orders': settings.allow_orders})

    def patch(self, request):
        settings, _ = GlobalSettings.objects.get_or_create(id=1)
        allow_orders = request.data.get('allow_orders')

        if allow_orders is not None:
            settings.allow_orders = allow_orders
            settings.save()

        return Response({'allow_orders': settings.allow_orders})


# ---------------------- Cart Views ----------------------
class CartDetailView(generics.RetrieveAPIView):
    """
    Get the current user's cart
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(customer=self.request.user)
        return cart


class CartAddItemView(APIView):
    """
    Add item to cart
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser]

    def post(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        item_id = request.data.get('item')
        quantity = int(request.data.get('quantity', 1))

        try:
            menu_item = MenuItem.objects.get(id=item_id, is_available=True)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response(CartSerializer(cart).data)


class CartRemoveItemView(APIView):
    """
    Remove item from cart, decrease quantity, or remove all quantities
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser]

    def delete(self, request, cart_item_id, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        remove_all = request.query_params.get('all', 'false').lower() == 'true'

        try:
            cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
            
            if remove_all:
                cart_item.delete()
                return Response({'detail': 'Item completely removed from cart'})
            
            # Decrease by 1
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                return Response({'detail': 'Decreased quantity by 1', 'quantity': cart_item.quantity})
            else:
                cart_item.delete()
                return Response({'detail': 'Item removed from cart'})

        except CartItem.DoesNotExist:
            return Response({'error': 'Item not in cart'}, status=status.HTTP_404_NOT_FOUND)
class CartClearView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser]

    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        cart.items.all().delete()  # delete all CartItem objects
        return Response({'detail': 'Cart cleared successfully'})

class CartCheckoutView(APIView):
    """
    Convert the current cart into an order
    """
    permission_classes = [permissions.IsAuthenticated, IsCustomerUser]

    def post(self, request, *args, **kwargs):
        # ✅ Check global order toggle
        settings, _ = GlobalSettings.objects.get_or_create(id=1)
        if not settings.allow_orders:
            raise PermissionDenied("Ordering is currently disabled by staff.")

        # ✅ Get the user's cart
        try:
            cart = Cart.objects.get(customer=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'No cart found'}, status=status.HTTP_404_NOT_FOUND)

        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Create order
        order = Order.objects.create(customer=request.user)

        # ✅ Move cart items to order
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity
            )

        # ✅ Calculate total price
        order.calculate_total()

        # ✅ Clear cart
        cart.items.all().delete()

        return Response({
            'message': 'Order placed successfully',
            'order_id': order.id
        }, status=status.HTTP_201_CREATED)

# ---------------------- Order Views ----------------------
class OrderListCreateView(generics.ListCreateAPIView):
    """
    List current user's orders or create a new order (via checkout)
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff_member():
            return Order.objects.all()
        return Order.objects.filter(customer=user)


class ActiveOrdersView(generics.ListAPIView):
    """
    Staff view: list all non-completed orders
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get_queryset(self):
        return Order.objects.exclude(status__in=['completed', 'cancelled']).order_by('-created_at')


class UpdateOrderStatusView(generics.UpdateAPIView):
    """
    Staff view: update order status
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)
