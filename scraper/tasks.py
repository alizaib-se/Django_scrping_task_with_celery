import logging
from scraper.models import Brand, Product
from celery import shared_task

from scraper.utils import scrape_amazon_products

logger = logging.getLogger(__name__)

# @shared_task(bind=True, max_retries=3)
def scrape_brand_products(brand_id):
    logger.info("started processing")
    try:
        brand = Brand.objects.get(id=brand_id)
        products_data = scrape_amazon_products(brand.brand_url)

        for product_data in products_data:
            Product.objects.update_or_create(
                asin=product_data['asin'],
                brand=brand,
                defaults={
                    'name': product_data['name'],
                    'sku': product_data['sku'],
                    'image_url': product_data['image_url'],
                }
            )
        logger.info(f"Successfully scraped products")

    except Brand.DoesNotExist:
        logger.error(f"Brand with id {brand.id} does not exist.")
    except Exception as exc:
        logger.error(f"Error while scraping products for brand {brand.id}: {exc}")
        # raise self.retry(exc=exc, countdown=60)



@shared_task(bind=True, max_retries=3)
def scrape_products_for_all_brands(self):
    logger.info("scheduler started to update products")
    brands = Brand.objects.all()
    for brand in brands:
        scrape_brand_products.delay(brand.id)
    logger.info("scheduler finished its execution")



