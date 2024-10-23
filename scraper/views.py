import logging

from rest_framework import generics
from rest_framework.response import Response
from .models import Brand, Product
from .serializers import BrandSerializer, ProductSerializer
from .tasks import scrape_brand_products

from django.http import HttpResponse

logger = logging.getLogger(__name__)

def home_view(request):
    return HttpResponse("the Amazon Scraping API")



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


        scrape_brand_products.delay(brand_id=brand.id)

        return Response({"status": "Products scraped and saved successfully."})
