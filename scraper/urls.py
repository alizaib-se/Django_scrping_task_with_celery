from django.urls import path
from .views import BrandListCreateView, ScrapeProductsView, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('brands/', BrandListCreateView.as_view(), name='brand-list-create'),
    path('brands/scrape/', ScrapeProductsView.as_view(), name='scrape-products'),
]
