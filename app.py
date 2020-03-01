from flask import Flask, render_template
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db

@app.route("/")
def index():
    mars_data = db.marsdata.find_one()
    return render_template("index.html", mars=mars_data)



@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    db.marsdata.update({}, mars_data, upsert=True)
    return "Scraping Successful"



if __name__ == "__main__":
    app.run(debug=True)