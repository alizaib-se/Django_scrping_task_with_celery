from rest_framework import generics
from rest_framework.response import Response
from .models import Brand, Product
from .serializers import BrandSerializer, ProductSerializer
from .tasks import scrape_brand_products

from django.http import HttpResponse


def home_view(request):
    return HttpResponse("Welcome to the Amazon Scraping API. Visit /api/brands/ to explore.")



class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ScrapeProductsView(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):

        try:
            brand = Brand.objects.get(id=request.data.get('brand_id'))
        except Brand.DoesNotExist:
            return Response({"error": "Brand not found."}, status=404)


        scrape_brand_products(brand_id=brand.id)

        return Response({"status": "Products scraped and saved successfully."})




"""
working url: https://www.amazon.com/stores/page/CFA3A81A-3CE1-4871-807C-675ECC7C46A0?ingress=2&visitId=5b6293a0-4257-4c7b-ae20-e1d1d3e58af0&store_ref=bl_ast_dp_brandLogo_sto&ref_=ast_bln"
"""
