# Scrape50
## A final project for CS50 which scrapes retail websites for data to be used in competitor brand analysis.

Video Demo: https://youtu.be/sCcBmjpwqdM

The project consists of three components:
- A python script using the Beautiful Soup library to scrape retail websites and save product information indcluding brand, product name, image links, and price.
- A SQL database which stores the scraped data.
- A Flask web framework to display product & brand information.

Languages used:
- **Python** for the Flask web framework and data cleansing
- **HTML** for the individual web pages used to display information
- **CSS** to style the individual web pages
- **JavaScript** to create interactions between the user and displayed content

The backbone of this project is the scrapers.py file, which contains python code to scrape information from retail websites.  I used the Requests library to fetch HTML data from various retailers, and the BeautifulSoup library to parse that data and add specific HTML tags & classes into a list of product data.  For each item in the list of product data, I separated out information such as the product name, price, brand, and image link, then added those items to a product dictionary.  Finally, I added each product dictionary to a SQL database.

Because each website is slightly different in structure, the code to parse the HTML and identify product information has to be slightly different.  I decided to use classes to organise this part of the code, with each retailer given a separate class, and the code to parse the HTML data put into a method for that class.  I also created a parent class called Scraper, which contains methods which would be common to all websites, including data cleansing using regex patterns and saving product dictionaries to SQL.

The end user will never have to see or interact with the code in scrapers.py, because all of the user interface is handled by a Flask web application.  The code for the Flask application is contained in the application.py file, and is primarily concerned with taking data from the SQL database mentioned above and returning HTML templates which display that data.  Throughout the site, I used Bootstrap to quickly create nice-looking elements such as the top navbar, cards, and buttons.  Although the use of Bootstrap helped to speed up development and create a clean look, I felt that it took away too much from the learning process, leaving me struggling to correct certain CSS elements.

The site itself has 4 main pages:
	
- The ‘/‘ route is a relatively simple landing page which presents the user with links to the other sections of the site, and  navbar at the top.
- The ‘/brands’ route allows users to input the name of a brand add see its distribution among UK retailers.  When typing, I use JavaScript to look for keyup events, and send the contents of the search bar to a ‘/search’ route using an AJAX request with JQuery.  I felt this was necessary to implement instead of a regular GET request because the names of many brands include accent marks (Lancôme, Estée Lauder), or can be abbreviated.  If the user sees feedback as they are typing, they can see the brand start to show up before the accent mark and they will know that the brand does exist in the database.  Without that feedback, the user would simply see a blank result to the query and assume the brand isn’t in the database.
- The ‘/<string:category>’ route returns a template with a grid of products sorted by price, and can be accessed via a drop-down list of categories in the navbar
- The ‘/admin’ route allows the user to refresh the data from any of the retailers listed, and shows the date of the last data refresh.  By ticking the checkbox next to the name of the retailer and submitting a POST request, an instance of the class for each retailer ticked is created, with the code then calling methods to get new product information and add it to the SQL database.