import csv
import sqlite3

data = []

# Create a database connection to a SQLite database
db = sqlite3.connect('products.db')
cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS products(
    id integer PRIMARY KEY,
    name text NOT NULL,
    price real,
    img_link text,
    site_id text,
    site_name text,
    scrapetime datetime NOT NULL DEFAULT CURRENT_DATE);""")
db.commit()

filename = "data_output.csv"
with open(filename) as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)


for row in data:
    cur.execute("INSERT INTO products(name, price, img_link, site_name) VALUES(?, ?, ?, ?)", (row['name'], row['price'], row['image_link'], row['brand']))
db.commit()
db.close()