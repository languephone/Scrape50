from flask import Flask, render_template
import csv

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

    products = []
    # Import product info from csv file into list
    filename = 'data_output.csv'
    with open(filename) as f:
        dict_reader = csv.DictReader(f)
        for row in dict_reader:
            if row['category'] == category:
                row['price'] = float(row['price'])
                products.append(row)
    products.sort(key = lambda i: float(i['price']))

    return render_template("index.html", category=category, products=products)