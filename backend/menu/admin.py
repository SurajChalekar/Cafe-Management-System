from django.contrib import admin
from .models import Category, MenuItem
from django.utils.html import format_html


# -------------------- Category Admin --------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_per_page = 20


# -------------------- MenuItem Admin --------------------
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'is_available',
        'preparation_time',
        'updated_at',
        'image_tag',
    )
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')
    ordering = ('category', 'name')
    list_per_page = 20

    def image_tag(self, obj):
        """Display image thumbnail in admin list view."""
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px; width:auto; border-radius:4px;" />',
                obj.image.url
            )
        return "-"
    image_tag.short_description = 'Image'
