from rest_framework import serializers
from .models import Category, MenuItem

# ------------------------
# Category Serializer
# ------------------------
class CategorySerializer(serializers.ModelSerializer):
    # Nested items for easy frontend rendering
    items = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'items']

    def get_items(self, obj):
        # Only return available menu items
        available_items = obj.items.filter(is_available=True)
        return MenuItemSerializer(available_items, many=True, context=self.context).data


# ------------------------
# MenuItem Serializer
# ------------------------
class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_name',
            'image', 'is_available', 'preparation_time', 'created_at', 'updated_at'
        ]
