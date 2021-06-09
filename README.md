# Scrape50
## A final project for CS50 which scrapes websites for data to be used in cosmetics brand competitor analysis.

Video Demo: https://youtu.be/sCcBmjpwqdM

The project consists of three components:
- A python script using the Beautiful Soup library to scrape retail websites and save product information indcluding brand, product name, image links, and price.
- A SQL database which stores the scraped data.
- A Flask web framework to display product information.

Languages used:
- **Python** for the Flask web framework and data cleansing
- **HTML** for the individual web pages used to display information
- **CSS** to style the individual web pages
- **JavaScript** to create interactions between the user and displayed content

The backbone of this project is the scrapers.py file, which contains python code to scrape information from retail websites.  I used the Requests library to fetch HTML data from various retailers, and the BeautifulSoup library to parse that data and add specific HTML tags & classes into a list of product data.  For each item in the list of product data, I separated out information such as the product name, price, brand, and image link, then added those items to a product dictionary.  Finally, I added each product dictionary to a new list of products.

Because each website is slightly different in structure, the code to parse the HTML and identify product information has to be slightly different.  I decided to use classes to organise this part of the code, with each retailer given a separate class, and the code to parse the HTML data put into a method for that class.  I also created a parent class called Scraper, which contains methods which would be common to all websites, including data cleansing using regex patterns and saving the list of product dictionaries to SQL.

The end user will never have to see or interace with the code in scrapers.py, because all of the user interface is handled by a Flask web application.  The code for the Flask application is contained in the application.py file.