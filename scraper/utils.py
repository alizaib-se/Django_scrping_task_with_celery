from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random

# List of User Agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',

]


# Function to introduce random delays
def random_delay(min_delay=1, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))

# Function to get a random user agent
def get_random_user_agent():
    return random.choice(USER_AGENTS)

def extract_products_from_response1(soup):
    products = soup.find_all('li', {'data-testid': 'product-grid-item'})

    product_list = []
    for product in products:
        name = product.find('a')['title']  # Get the title from the link
        asin = product['data-csa-c-item-id']  # Get the ASIN from the item id
        image_url = product.find('img')['src']  # Get the image URL
        sku = None  # SKU is not available in the provided HTML

        product_details = {
            'name': name,
            'asin': asin,
            'sku': sku,
            'image_url': image_url
        }

        product_list.append(product_details)
    return product_list

def extract_products_from_response2(soup):
    product_divs = soup.find_all('div', {'data-component-type': 's-search-result'})

    products = []

    for product in product_divs:
        _name = product.select_one('h2.a-size-mini a span.a-size-base-plus').get_text(strip=True)
        _name = _name if _name else None

        asin = product.get('data-asin')

        sku_tag = product.find('div', class_='sg-col-inner')
        sku = sku_tag.get('data-uuid') if sku_tag else None

        image_tag = product.find('img', class_='s-image')
        image_url = image_tag.get('src') if image_tag else None

        product_data = {
            'name': _name,
            'asin': asin,
            'sku': sku,
            'image_url': image_url
        }
        products.append(product_data)
    return products


def scrape_amazon_products(brand_url):
    # Set up Selenium options
    options = Options()
    options.headless = True  # Run headless Chrome (without GUI)
    options.add_argument(f"user-agent={get_random_user_agent()}")  # Set random user agent

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(brand_url)

    # Scroll down to load more products
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_delay(2, 5)  # Wait for new content to load

        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # No more products to load
        last_height = new_height

    # After scrolling, parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Check for CAPTCHA detection
    if "captcha" in soup.text.lower():
        print("CAPTCHA detected. Please solve the CAPTCHA manually.")
        driver.quit()
        return []


    for extractor in [extract_products_from_response1, extract_products_from_response2]:
        product_list = extractor(soup)
        if product_list:
            break

    driver.quit()

    return product_list


