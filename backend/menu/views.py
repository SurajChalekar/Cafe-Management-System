from rest_framework import generics, permissions, filters
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from users.permissions import IsStaffUser  # custom permission

# ------------------------
# Customers (read-only)
# ------------------------
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]  # anyone can view categories


class MenuItemBaseView:
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemListView(MenuItemBaseView, generics.ListAPIView):
    queryset = MenuItem.objects.filter(is_available=True)
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'preparation_time']


class MenuItemDetailView(MenuItemBaseView, generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]


# ------------------------
# Staff (create/edit/delete)
# ------------------------
class MenuItemManageView(MenuItemBaseView, generics.ListCreateAPIView):
    permission_classes = [IsStaffUser]

    def perform_create(self, serializer):
        serializer.save()
        print(f"MenuItem created by {self.request.user}")


class MenuItemUpdateDeleteView(MenuItemBaseView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsStaffUser]
