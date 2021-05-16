import csv
import sqlite3
from fuzzywuzzy import fuzz, process

data = []

def create_table(database_name):
    """Create an initial product table in a SQLite 3 database."""

    # Create a database connection to a SQLite database
    db = sqlite3.connect(database_name)
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS products(
        id integer PRIMARY KEY,
        name text NOT NULL,
        brand text,
        price real,
        img_link text,
        category text NOT NULL,
        site_id text,
        scrapedate datetime NOT NULL DEFAULT CURRENT_DATE)""")
    db.commit()


def csv_to_sql(filename):
    """Read a csv file into the sql product table."""
    
    filename = "data_output.csv"
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    for row in data:
        cur.execute("INSERT INTO products(name, brand, price, img_link, category, site_id) VALUES(?, ?, ?, ?, ?, ?)",
        (row['name'], row['brand'], row['price'], row['image_link'], row['category'], row['site_id']))
    db.commit()
    db.close()

def sql_to_csv():
    db = sqlite3.connect('products.db')
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("""SELECT * FROM products WHERE scrapedate=(SELECT MAX(scrapedate) FROM products)""")
    data = [dict(row) for row in cur.fetchall()]
    db.close()
    csv_columns = data[0].keys()

    filename = "data_output.csv"
    with open(filename, 'w') as file_object:
        writer = csv.DictWriter(file_object, fieldnames=csv_columns)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def get_product_names(category):

    # Get categories & brands from SQL
    db = sqlite3.connect('products.db')
    cur = db.cursor()
    cur.execute("""SELECT * FROM products WHERE category=? AND scrapedate=(SELECT MAX(scrapedate) FROM products WHERE category=?)""", (category, category))
    product_rows = cur.fetchall()
    db.close()

    # Convert SQL response from list of tuples to list of dictionaries
    products = []
    keys = ('id', 'name', 'brand', 'price', 'image_link', 'site_id')
    for row in product_rows:
        products.append(dict(zip(keys, row)))

    products.sort(key = lambda i: i['name'])
    names = [product['name'] for product in products]

    return names

# create_table('products.db')
# csv_to_sql('data_output.csv')
# sql_to_csv()


# Get product names from Look Fantastic
db = sqlite3.connect('products.db')
cur = db.cursor()
cur.execute("""SELECT * FROM products WHERE scrapedate=(SELECT MAX(scrapedate) FROM products)""")
product_rows = cur.fetchall()
db.close()

# Convert SQL response from list of tuples to list of dictionaries
products = []
keys = ('id', 'name', 'brand', 'price', 'image_link', 'category', 'site_id')
for row in product_rows:
    products.append(dict(zip(keys, row)))

products.sort(key = lambda i: i['name'])
lf_names = set([product['brand'] for product in products if product['site_id'] == 'Look Fantastic'])
hof_names = set([product['brand'] for product in products if product['site_id'] == 'House of Fraser'])


print('------85 or higher------')
for name in hof_names:
    match = process.extractOne(name, lf_names, scorer=fuzz.partial_ratio)
    if match[1] >= 85:
        print(name, match)

print('------84 or lower------')
for name in hof_names:
    match = process.extractOne(name, lf_names, scorer=fuzz.partial_ratio)
    if match[1] < 85:
        print(name, match)

