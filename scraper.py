import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.thewhiskyexchange.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

productlinks = []
for i in range(1,6):
    k = requests.get(f"https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={i}&psize=24&sort=pasc").text
    soup = BeautifulSoup(k, 'html.parser')
    productlist = soup.find_all('li', {"class":"product-grid__item"})

    for product in productlist:
        link = product.find('a', {"class": "product-card"}).get('href')
        productlinks.append(baseurl + link)

data = []
for link in productlinks:
    f = requests.get(link, headers=headers).text
    hun = BeautifulSoup(f, 'html.parser')

    try:
        price = hun.find('p', {"class": "product-action__price"}).text.replace('\n', "")
    except:
        price = None

    try:
        about = hun.find('div', {"class": "product-main__description"}).text.replace('\n', "")
    except:
        about = None

    try:
        rating = hun.find('div', {"class": "review-overview"}).text.replace('\n', "")
    except:
        rating = None

    try:
        name = hun.find('h1', {"class": "product-main__name"}).text.replace('\n', "")
    except:
        name = None

    whisky = {"name": name, "price": price, "rating": rating, "about": about}

    data.append(whisky)

df = pd.DataFrame(data)

print(df)


