from flask import Flask, render_template
import csv
import sqlite3

app = Flask(__name__)

def gbp(value):
    """Format value as GBP."""
    return f"£{value:,.2f}"




# Custom filter
app.jinja_env.filters["gbp"] = gbp

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<string:category>")
def category(category):

    # Create a database connection to a SQLite database
    db = sqlite3.connect('products.db')
    cur = db.cursor()
    cur.execute("""SELECT * FROM products""")
    product_rows = cur.fetchall()
    db.close()


    # Convert SQL response from list of tuples to list of dictionaries
    products = []
    keys = ('id', 'name', 'brand', 'price', 'image_link', 'site_id')
    for row in product_rows:
        products.append(dict(zip(keys, row)))

    products.sort(key = lambda i: float(i['price']))

    return render_template("index.html", category=category, products=products)