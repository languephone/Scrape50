from flask import Flask, render_template
import csv

app = Flask(__name__)

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
                products.append(row)
    


    return render_template("index.html", category=category, products=products)