import csv
import sqlite3

data = []

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