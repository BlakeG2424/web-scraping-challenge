# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to index.html template using data from Mongo
@app.route("/")
def home(): 

    # Find one record of data from the mongo database and return it
    mars = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", mars=mars)

# Route to scrape
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.replace_one({}, mars_data, upsert=True)

    # Redirect back to home page and return a message to show it was succesful
    return redirect('/')
    
if __name__ == "__main__":
    app.run(debug=True)
