from flask import Flask, render_template, request
import csv
import sqlite3
from scrapers import LookFantastic, HouseOfFraser, Asos, CultBeauty

app = Flask(__name__)

def gbp(value):
    """Format value as GBP."""
    return f"£{value:,.2f}"

# Custom filter
app.jinja_env.filters["gbp"] = gbp

# Function to get distinct categories
def get_category_list():
    """Connect to SQL database and get list of unique categories."""

    # Create a database connection to a SQLite database
    db = sqlite3.connect('products.db')
    cur = db.cursor()
    cur.execute("""SELECT DISTINCT category FROM products""")
    # Convert SQL output from tuples to list
    categories = [x[0] for x in cur.fetchall()]
    db.close()
    return categories

@app.route("/")
def index():

    categories = get_category_list()
    return render_template("index.html", categories=categories)


@app.route("/<string:category>")
def category(category):

    # Create a database connection to a SQLite database
    db = sqlite3.connect('products.db')
    cur = db.cursor()
    cur.execute("""SELECT * FROM products WHERE category=? AND scrapedate=(SELECT MAX(scrapedate) FROM products WHERE category=?)""", (category, category))
    product_rows = cur.fetchall()
    cur.execute("""SELECT DISTINCT brand FROM products""")
    brands = [x[0] for x in cur.fetchall()]
    categories = get_category_list()
    db.close()

    # Convert SQL response from list of tuples to list of dictionaries
    products = []
    keys = ('id', 'name', 'brand', 'price', 'image_link', 'site_id')
    for row in product_rows:
        products.append(dict(zip(keys, row)))

    products.sort(key = lambda i: float(i['price']))

    return render_template("category.html", category=category, products=products, brands=brands, categories=categories)


@app.route("/brands")
def brands():

    categories = get_category_list()
    brand = request.args.get("q")

    if brand == None:
        brand = ""

    # Create a database connection to a SQLite database
    db = sqlite3.connect('products.db')
    cur = db.cursor()
    cur.execute("""SELECT brand, site, MIN(scrapedate) FROM brands
        WHERE lower(brand) LIKE ? GROUP BY site, brand
        ORDER BY brand ASC""", ("%" + brand.lower() + "%",))
    brand_rows = cur.fetchall()
    categories = get_category_list()
    db.close()

    # TODO: filter brands by latest scrapedate, and pull first scrapedate for each brand

    # Convert SQL response from list of tuples to list of dictionaries
    brands = []
    keys = ('brand', 'site', 'scrapedate')
    for row in brand_rows:
        brands.append(dict(zip(keys, row)))

    #brands.sort(key = lambda i: i['brand'])

    return render_template("brand.html", brands=brands, categories=categories)


@app.route("/admin", methods=["GET", "POST"])
def admin():

    categories = get_category_list()

    # Create a database connection to a SQLite database
    db = sqlite3.connect('products.db')
    cur = db.cursor()
    cur.execute("""SELECT site, MAX(scrapedate) FROM brands GROUP BY site""")
    brand_rows = cur.fetchall()
    cur.execute("""SELECT DISTINCT site_id FROM products""")
    sites_products = [x[0] for x in cur.fetchall()]
    db.close()

    # Convert SQL response from list of tuples to list of dictionaries
    sites_brands = []
    keys = ('site', 'scrapedate')
    for row in brand_rows:
        sites_brands.append(dict(zip(keys, row)))

    if request.method == "POST":
        if request.form.get("ASOS") == "brands":
            asos = Asos()
            asos.get_all_brands()
            asos.write_brands_to_sql()
        if request.form.get("Cult Beauty") == "brands":
            cb = CultBeauty()
            cb.get_all_brands()
            cb.write_brands_to_sql()
        if request.form.get("Look Fantastic") == "brands":
            lf = LookFantastic()
            lf.get_all_brands()
            lf.write_brands_to_sql()
        if request.form.get("Look Fantastic") == "products":
            lf = LookFantastic()
            lf.loop_through_categories()
            lf.clean_all_products()
            lf.write_products_to_sql()
        if request.form.get("House of Fraser") == "products":
            hof = HouseOfFraser()
            hof.loop_through_categories()
            hof.clean_all_products()
            hof.write_products_to_sql()

    return render_template("admin.html", categories=categories, sites_brands=sites_brands, sites_products=sites_products)