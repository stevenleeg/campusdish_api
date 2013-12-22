from flask import Flask, redirect, g
from flask.ext.restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import os, datetime

app = Flask(__name__)
api = Api(app)

# Setup database
db_uri = "postgres://%s:%s@%s:%s/%s" % (
    os.environ['DB_USER'],
    os.environ['DB_PASS'],
    os.environ['DB_HOST'],
    os.environ['DB_PORT'],
    os.environ['DB_NAME'],
)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
import models

@app.route("/")
def index():
    return redirect("https://github.com/stevenleeg/campusdish_api/blob/master/README.md")

class Location(Resource):
    def get(self, location, meal):

        stations = {}
        for dish in dishes:
            if dish['station'] not in stations:
                stations[dish['station']] = []
            
            stations[dish['station']].append({ 
                "title": dish['title'],
                "date": str(dish['date'])[0:10]
            })

        return { 
            "status": 200,
            "stations": stations,
            "meal": meal
        }

api.add_resource(Location, "/v1/location/<string:location>/<string:meal>")

if __name__ == "__main__":
    app.run(debug = True)
