from flask import Flask, render_template, request, jsonify
import csv
import sqlite3
import scrapers

app = Flask(__name__)

def gbp(value):
    """Format value as GBP."""
    return f"£{value:,.2f}"

# Custom filter
app.jinja_env.filters["gbp"] = gbp


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


def sql_to_dict(list_of_tuples, *keys):
    """Convert SQL response from list of tuples to list of dictionaries"""
    dicts = []
    keys = (keys)
    for row in list_of_tuples:
        dicts.append(dict(zip(keys, row)))
    return dicts


@app.route("/")
def index():

    categories = get_category_list()
    return render_template("index.html", categories=categories)


@app.route("/<string:category>")
def category(category):

    # Get products from SQL
    db = sqlite3.connect('products.db')
    cur = db.cursor()
    cur.execute("""SELECT name_clean, brand, price, img_link, site_id FROM products WHERE category=? AND scrapedate=(SELECT MAX(scrapedate) FROM products WHERE category=?)""", (category, category))
    product_rows = cur.fetchall()
    products = sql_to_dict(product_rows, 'name_clean', 'brand', 'price', 'image_link', 'site_id')
    products.sort(key = lambda i: float(i['price']))

    # Get categories & brands from SQL
    cur.execute("""SELECT DISTINCT brand FROM products WHERE category=? AND scrapedate=(SELECT MAX(scrapedate) FROM products WHERE category=?)""", (category, category))
    brands = [x[0] for x in cur.fetchall()]
    brands.sort()
    categories = get_category_list()
    db.close()

    return render_template("category.html", category=category, products=products, brands=brands, categories=categories)


@app.route("/brands")
def brands():

    categories = get_category_list()
    # TODO: filter brands by latest scrapedate, and pull first scrapedate for each brand
    return render_template("brand.html", categories=categories)


@app.route("/admin", methods=["GET", "POST"])
def admin():

    categories = get_category_list()

    # Get sites from product & brand tables from SQL
    db = sqlite3.connect('products.db')
    cur = db.cursor()
    cur.execute("""SELECT site, MAX(scrapedate) FROM brands GROUP BY site""")
    brand_rows = cur.fetchall()
    sites_brands = sql_to_dict(brand_rows, 'site', 'scrapedate')
    cur.execute("""SELECT site_id, MAX(scrapedate) FROM products GROUP BY site_id""")
    product_rows = cur.fetchall()
    sites_products = sql_to_dict(product_rows, 'site_id', 'scrapedate')
    db.close()

    if request.method == "POST":
        # Run brand refresh methods for any site sent in brand form
        brand_updates = request.form.getlist('brands')
        for site in brand_updates:
            class_ = getattr(scrapers, site.title().replace(' ', ''))
            instance = class_()
            instance.get_all_brands()
            instance.write_brands_to_sql()

        # Run product refresh methods for any site sent in product form
        product_updates = request.form.getlist('products')
        for site in product_updates:
            class_ = getattr(scrapers, site.title().replace(' ', ''))
            instance = class_()
            instance.loop_through_categories()
            instance.clean_all_products()
            instance.write_products_to_sql()

    return render_template("admin.html", categories=categories, sites_brands=sites_brands, sites_products=sites_products)

@app.route("/search")
def search():

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
    brands = sql_to_dict(brand_rows, 'brand', 'site', 'scrapedate')
    db.close()

    # TODO: filter brands by latest scrapedate, and pull first scrapedate for each brand

    return jsonify(brands)