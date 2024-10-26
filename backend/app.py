from flask import Flask
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
    fide = mongo.db.fide_ratings.find({}, {"_id": 0})
    fide = list(fide)
    blitz = mongo.db.blitz_ratings.find({}, {"_id": 0})
    blitz = list(blitz)
    bullet = mongo.db.bullet_ratings.find({}, {"_id": 0})
    bullet = list(bullet)
    return {"fide": fide, "blitz": blitz, "bullet": bullet}
 
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 