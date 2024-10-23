from django.contrib import admin
from .models import Brand, Product

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'asin', 'sku', 'brand', 'updated_at']
    search_fields = ['name', 'asin']
