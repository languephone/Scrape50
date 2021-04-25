import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3


class Scraper:
    """A class to create a template for sites to be scraped."""

    def __init__(self):
        """Initialise nothing.  Does this make sense?"""


    def clean_product_name(self, product_name):
        """Remove colour and/or shade information from product name"""

        replacements = ['- Black', '(Various Shades)', '01']
        for replacement in replacements:
            product_name = product_name.replace(replacement, "").strip()

        return product_name


    def write_to_sql(self):
        """Take a list of dictionaries of scraped data, and write to a SQLite database"""

        # Create a database connection to a SQLite database
        db = sqlite3.connect('products.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS products(
            id integer PRIMARY KEY,
            name text NOT NULL,
            brand text,
            price real,
            img_link text,
            category text NOT NULL,
            site_id text,
            scrapedate datetime NOT NULL DEFAULT CURRENT_DATE);""")
        db.commit()

       # Insert rows into database
        for row in self.data:
            cur.execute("INSERT INTO products(name, brand, price, img_link, category, site_id) VALUES(?, ?, ?, ?, ?, ?)",
                (row['name'], row['brand'], row['price'], row['image_link'], row['category'], row['site_id']))
        db.commit()
        db.close()

    def write_to_csv(self):
        """Take a list of dictionaries of scraped data, and write to a CSV file"""

        df = pd.DataFrame(self.data)
        df.to_csv('data_output.csv', index=False)


class LookFantastic(Scraper):
    "A class to scrape from the Look Fantastic website."

    def __init__(self):
        """Initialize attributes of the parent class."""
        super().__init()
        self.site = "Look Fantastic"
        self.base_link = "https://www.lookfantastic.com/health-beauty/"
        self.sorting_modifier = "?pageNumber=1&sortOrder=salesRank"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        # TODO find replacement for hard coding category links
        self.categories = {
            'foundation': "make-up/complexion/foundation-makeup.list",
            'mascara': "make-up/eyes/mascaras.list"
            }
        self.data = []

    def get_top_products(self, category):
        """Scrape info from top products page of specified category link"""

        # Modify link to sort by top sales rank
        link_modified = self.base_link + self.categories[category] + self.sorting_modifier


        page = requests.get(link_modified, headers=self.headers).text
        soup = BeautifulSoup(page, 'html.parser')
        product_list = soup.find_all('li', {"class": "productListProducts_product"})

        for product in product_list:
            product_data = product.find('span', {"class": "js-enhanced-ecommerce-data"})

            try:
                name = product_data.get('data-product-title').replace('\n', "")
            except:
                name = None

            try:
                price = product_data.get('data-product-price').replace('\n', "").replace("£", "")
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

            item = {'category': category, 'name': name, 'price': price, 'brand': brand, 'product_id': product_id, 'image_link': image_link, 'site_id': site}
            self.data.append(item)



# Call write_to_x functions to send data to CSV and SQL
write_to_csv(data)
write_to_sql(data)