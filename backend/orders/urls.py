# orders/urls.py
from django.urls import path
from .views import (
    CartClearView, CartDetailView, CartAddItemView, CartRemoveItemView, CartCheckoutView,
    OrderListCreateView, ActiveOrdersView, UpdateOrderStatusView, GlobalSettingsView, GlobalOrderStatusView
)

app_name = "orders"

urlpatterns = [
    # Cart endpoints
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', CartAddItemView.as_view(), name='cart-add-item'),
    path('cart/remove/<int:cart_item_id>/', CartRemoveItemView.as_view(), name='cart-remove-item'),
    path('cart/checkout/', CartCheckoutView.as_view(), name='cart-checkout'),
    path('cart/clear/', CartClearView.as_view(), name='cart-clear'),

    # Customer orders
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('global-order-status/', GlobalOrderStatusView.as_view(), name='global-order-status'),

    # Staff-only endpoints
    path('orders/active/', ActiveOrdersView.as_view(), name='active-orders'),
    path('orders/update/<int:pk>/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('staff/global-order-toggle/', GlobalSettingsView.as_view(), name='global-order-toggle'),
]
