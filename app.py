from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db

# @app.before_first_request
# def init_app():
#     mars_data = scrape_mars.scrape() 
#     db.marsdata.insert_one(mars_data)
       

@app.route("/")
def index():
    mars_data = db.marsdata.find_one()
    mars_data = scrape_mars.scrape()
    return render_template("index.html", mars = mars_data)
    

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape() 
    print(mars_data)
    db.marsdata.drop()
    db.marsdata.insert_one(mars_data)
    
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
