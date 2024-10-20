from flask import Flask, render_template
from db_updater_by_scraping import scrape_chess_players_selenium    
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os


app = Flask(__name__)
if load_dotenv(".env"):
    url = os.getenv("url_mongo")
    app.config["MONGO_URI"] = url
    mongo = PyMongo(app)
else:
    print(".env not found")



@app.route('/', methods=["GET"])
def main_page():
    data = mongo.db.chess_players.find({}, {"_id": 0})
    data = list(data)
    
    return {"message": data}
 
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 