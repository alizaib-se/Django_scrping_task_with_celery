from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255)
    brand_url = models.URLField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    asin = models.CharField(max_length=10)
    sku = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.URLField(max_length=500)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.asin})"
