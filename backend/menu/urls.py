from django.urls import path
from .views import (
    CategoryListView, MenuItemListView, MenuItemDetailView,
    MenuItemManageView, MenuItemUpdateDeleteView
)

app_name = "menu"

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('items/', MenuItemListView.as_view(), name='menuitem-list'),
    path('items/<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-detail'),

    # staff endpoints
    path('staff/items/', MenuItemManageView.as_view(), name='staff-menuitem-manage'),
    path('staff/items/<int:pk>/', MenuItemUpdateDeleteView.as_view(), name='staff-menuitem-update'),
]
