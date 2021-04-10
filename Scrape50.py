import requests
from bs4 import BeautifulSoup
import pandas as pd

link = "https://www.lookfantastic.com/health-beauty/make-up/eyes/mascaras.list?pageNumber=1&sortOrder=salesRank"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

data = []
page = requests.get(link).text
soup = BeautifulSoup(page, 'html.parser')
product_list = soup.find_all('li', {"class": "productListProducts_product"})

# Use individual elements to get product name & price
for product in product_list:
    try:
        name = product.find('h3', {"class": "productBlock_productName"}).text.replace('\n', "")
    except:
        name = None

    try:
        price = product.find('span', {"class": "productBlock_priceValue"}).get('content').replace('\n', "")
    except:
        price = None

    mascara = {'name': name, 'price': price}
    data.append(mascara)

df = pd.DataFrame(data)

print(df)