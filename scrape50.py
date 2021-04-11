import requests
from bs4 import BeautifulSoup
import pandas as pd

base_link = "https://www.lookfantastic.com/health-beauty/"
sorting_modifier = "?pageNumber=1&sortOrder=salesRank"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
data = []

def get_top_products(category, link, headers):
    """Scrape info from top products page of specified category link"""

    # Modify link to sort by top sales rank
    link_modified = base_link + link + sorting_modifier


    page = requests.get(link_modified, headers=headers).text
    soup = BeautifulSoup(page, 'html.parser')
    product_list = soup.find_all('li', {"class": "productListProducts_product"})

    for product in product_list:
        product_data = product.find('span', {"class": "js-enhanced-ecommerce-data"})

        try:
            name = product_data.get('data-product-title').replace('\n', "")
        except:
            name = None

        try:
            price = float(product_data.get('data-product-price').replace('\n', "").replace("£", ""))
        except:
            price = None

        try:
            brand = product_data.get('data-product-brand').replace('\n', "")
        except:
            brand = None

        try:
            product_id = product_data.get('data-product-master-product-id').replace('\n', "")
        except:
            product_id = None

        try:
            image_link = product.find('img').get('src').replace('\n', "")
        except:
            image_link = None

        item = {'category': category, 'name': name, 'price': price, 'brand': brand, 'product_id': product_id, 'image_link': image_link}
        data.append(item)


# TODO find replacement for hard coding category links
categories = {
    'foundation': "make-up/complexion/foundation-makeup.list",
    'mascara': "make-up/eyes/mascaras.list"
    }

# Loop through categories, appending to list, then append to pandas dictionary
for category, link in categories.items():
    get_top_products(category, link, headers)

df = pd.DataFrame(data)
df.to_csv('data_output.csv', index=False)