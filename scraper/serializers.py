from rest_framework import serializers
from .models import Product, Brand


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'asin', 'sku', 'image_url', 'brand']


class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'brand_url','products']
