import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import re

class Scraper:
    """A class to create a template for sites to be scraped."""

    def __init__(self):
        """Initialise nothing.  Does this make sense?"""

    def loop_through_categories(self):
        """Loop through specified categories and call get_top_products()."""
        for category in self.categories:
            self.get_top_products(category)

    def clean_all_products(self):
        for product in self.product_data:
            product['clean_name'] = self._clean_product_name(product['name'], product['brand'])

    def _clean_product_name(self, product_name, brand):
        """Remove brand, colour and/or shade, size & SPF information from product name"""

        # Remove brand name from product name if exists:
        #product_name = product_name.replace(brand, "").strip()

        product_name = re.split(r'( - |, )', product)[0]

        patterns = [r"[0-9.]+ *(ml|oz|g)", r"\(Various Shades\)", r" SPF *\d+",
            r" \d+ *SPF", r" [-–] *\d* Black *"]
        for pattern in patterns:
            product_name = re.sub(pattern, "", product_name).strip()

        return product_name

    def write_products_to_sql(self):
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
        for row in self.product_data:
            cur.execute("INSERT INTO products(name, brand, price, img_link, category, site_id) VALUES(?, ?, ?, ?, ?, ?)",
                (row['name'], row['brand'], row['price'], row['image_link'], row['category'], row['site_id']))
        db.commit()
        db.close()


    def write_brands_to_sql(self):
        """Take a list of dictionaries of scraped data, and write to a SQLite database"""

        # Create a database connection to a SQLite database
        db = sqlite3.connect('products.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS brands(
            id integer PRIMARY KEY,
            brand text NOT NULL,
            site text NOT NULL,
            scrapedate datetime NOT NULL DEFAULT CURRENT_DATE);""")
        db.commit()

       # Insert rows into database
        for brand in self.brand_data:
            cur.execute("INSERT INTO brands(brand, site) VALUES(?, ?)", (brand, self.site))
        db.commit()
        db.close()

    def write_to_csv(self, data_set):
        """Take a list of dictionaries of scraped data, and write to a CSV file"""

        df = pd.DataFrame(data_set)
        df.to_csv(f'data_output_classes_{self.site}.csv', index=False)


class LookFantastic(Scraper):
    "A class to scrape from the Look Fantastic website."

    def __init__(self):
        """Initialize attributes of the parent class."""
        super().__init__()
        self.site = "Look Fantastic"
        self.base_link = "https://www.lookfantastic.com/"
        self.sorting_modifier = "?pageNumber=1&sortOrder=salesRank"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        # TODO find replacement for hard coding category links
        self.categories = {
            'foundation': "health-beauty/make-up/complexion/foundation-makeup.list",
            'mascara': "health-beauty/make-up/eyes/mascaras.list"
            }
        self.brand_page = "brands.list"
        self.product_data = []
        self.brand_data = []

    def get_top_products(self, category):
        """Scrape product info from top products page of specified category link"""

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
                # Check for RRP field, which will appear only on discounted products
                price = product.find('span', {"class": "productBlock_rrpValue"}).text.replace('\n', "").replace("£", "")
            except:
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

            item = {'category': category, 'name': name, 'price': price, 'brand': brand, 'product_id': product_id, 'image_link': image_link, 'site_id': self.site}
            self.product_data.append(item)


    def get_all_brands(self):
        """Scrape list of brands from A-Z brand section of site."""

        # Modify link to add on brands section
        link_modified = self.base_link + self.brand_page

        page = requests.get(link_modified, headers=self.headers).text
        soup = BeautifulSoup(page, 'html.parser')
        brand_list = soup.find_all('li', {"class": "responsiveBrandsPageScroll_brandTabsItem"})

        for brand in brand_list:
            try:
                name = brand.a.string.replace('\n', "")
            except:
                pass

            self.brand_data.append(name)


class HouseOfFraser(Scraper):
    "A class to scrape from the House of Fraser website."

    def __init__(self):
        """Initialize attributes of the parent class."""
        super().__init__()
        self.site = "House of Fraser"
        self.base_link = "https://www.houseoffraser.co.uk/beauty/"
        self.sorting_modifier = ""
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        # TODO find replacement for hard coding category links
        self.categories = {
            'foundation': "foundations",
            'mascara': "mascaras"
            }
        self.product_data = []

    def get_top_products(self, category):
        """Scrape info from top products page of specified category link"""

        # Modify link to sort by top sales rank
        link_modified = self.base_link + self.categories[category] + self.sorting_modifier


        page = requests.get(link_modified, headers=self.headers).text
        soup = BeautifulSoup(page, 'html.parser')
        product_grid = soup.find("ul",{"class":"s-productscontainer2"})
        product_list = product_grid.find_all("li", recursive=False)

        for product in product_list:

            try:
                name = product.get('li-name').replace('\n', "")
            except:
                name = None

            try:
                price = product.get('li-price').replace('\n', "").replace("£", "")
            except:
                price = None

            try:
                brand = product.get('li-brand').replace('\n', "")
            except:
                brand = None

            try:
                product_id = product.get('li-productid').replace('\n', "")
            except:
                product_id = None

            try:
                image_link = product.find('img').get('src').replace('\n', "")
            except:
                try:
                    image_link = product.find('img').get('data-original').replace('\n', "")
                except:
                    image_link = None

            item = {'category': category, 'name': name, 'price': price, 'brand': brand, 'product_id': product_id, 'image_link': image_link, 'site_id': self.site}
            self.product_data.append(item)


class CultBeauty(Scraper):
    "A class to scrape from the Cult Beauty website."

    def __init__(self):
        """Initialize attributes of the parent class."""
        super().__init__()
        self.site = "Cult Beauty"
        self.base_link = "https://www.cultbeauty.co.uk/"
        self.sorting_modifier = ""
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
        # TODO find replacement for hard coding category links
        self.categories = {
            'foundation': "",
            'mascara': ""
            }
        self.brand_page = "brands"
        self.product_data = []
        self.brand_data = []


    def get_all_brands(self):
        """Scrape list of brands from A-Z brand section of site."""

        # Modify link to add on brands section
        link_modified = self.base_link + self.brand_page

        page = requests.get(link_modified).text
        soup = BeautifulSoup(page, 'html.parser')
        letter_group = soup.find_all('div', {"class": "letterGroup"})

        for letter in letter_group:
            brand_list = letter.find_all('li')
            for brand in brand_list:

                try:
                    name = brand.a.string.replace('\n', "")
                except:
                    pass

                self.brand_data.append(name)


class Asos(Scraper):
    "A class to scrape from the ASOS website."

    def __init__(self):
        """Initialize attributes of the parent class."""
        super().__init__()
        self.site = "ASOS"
        self.base_link = "https://www.asos.com/"
        self.sorting_modifier = ""
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        # TODO find replacement for hard coding category links
        self.categories = {
            'foundation': "",
            'mascara': ""
            }
        self.brand_page = "women/face-body/a-to-z-of-brands/cat/?cid=2373"
        self.product_data = []
        self.brand_data = []


    def get_all_brands(self):
        """Scrape list of brands from A-Z brand section of site."""

        # Modify link to sort by top sales rank
        link_modified = self.base_link + self.brand_page

        page = requests.get(link_modified, headers=self.headers).text
        soup = BeautifulSoup(page, 'html.parser')
        brand_sections = soup.find_all('li', {"class": "vqk6pTa"})
        for section in brand_sections:

            try:
                name = section.a.string.replace('\n', "")
            except:
                pass

            self.brand_data.append(name)


class Next(Scraper):
    "A class to scrape from the Beauty Bay website."

    def __init__(self):
        """Initialize attributes of the parent class."""
        super().__init__()
        self.site = "Next"
        self.base_link = "https://www.next.co.uk/"
        self.sorting_modifier = ""
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        # TODO find replacement for hard coding category links
        self.categories = {
            'foundation': "",
            'mascara': ""
            }
        self.brand_page = "brands/beauty"
        self.product_data = []
        self.brand_data = []


    def get_all_brands(self):
        """Scrape list of brands from A-Z brand section of site."""

        # Modify link to add on brands section
        link_modified = self.base_link + self.brand_page

        page = requests.get(link_modified, headers=self.headers).text
        soup = BeautifulSoup(page, 'html.parser')
        brand_sections = soup.find_all('div', {"class": "col-md-3 bp-brand-name"})

        for brand in brand_sections:
            try:
                name = brand.a.string.replace('\n', "")
            except:
                pass

            self.brand_data.append(name)


class Boots(Scraper):
    "A class to scrape from the Boots website."

    def __init__(self):
        """Initialize attributes of the parent class."""
        super().__init__()
        self.site = "Boots"
        self.base_link = "https://www.boots.com/"
        self.sorting_modifier = ""
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        # TODO find replacement for hard coding category links
        self.categories = {
            'foundation': "",
            'mascara': ""
            }
        self.brand_page = "beauty/all-beauty-and-skincare-brands"
        self.product_data = []
        self.brand_data = []


    def get_all_brands(self):
        """Scrape list of brands from A-Z brand section of site."""

        # Modify link to add on brands section
        link_modified = self.base_link + self.brand_page

        page = requests.get(link_modified, headers=self.headers).text
        soup = BeautifulSoup(page, 'html.parser')
        brand_section = soup.find('div', {"id": "brand-lists"})
        brands = brand_section.find_all('a')
        
        for brand in brands:
            try:
                name = brand.string.replace('\n', "")
            except:
                pass

            self.brand_data.append(name)