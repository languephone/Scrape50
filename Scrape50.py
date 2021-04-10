import requests
from bs4 import BeautifulSoup
import pandas as pd

foundation_link = "https://www.lookfantastic.com/health-beauty/make-up/complexion/foundation-makeup.list"
mascara_link = "https://www.lookfantastic.com/health-beauty/make-up/eyes/mascaras.list"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

def get_top_products(category, link, headers):
    """Scrape info from top products page of specified category link"""

    # Modify link to sort by top sales rank
    link_modified = link + "?pageNumber=1&sortOrder=salesRank"

    data = []
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
            price = product_data.get('data-product-price').replace('\n', "")
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

        item = {'category': category, 'name': name, 'price': price, 'brand': brand, 'product_id': product_id}
        data.append(item)

    return data

foundations = get_top_products('Foundation', foundation_link, headers)

df = pd.DataFrame(foundations)
df.to_csv('data_output.csv', index=False)

print(df)