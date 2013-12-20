from flask import Flask, redirect, g
from flask.ext.restful import Resource, Api
from pymongo import MongoClient
import os, datetime

app = Flask(__name__)
api = Api(app)

@app.before_request
def db_connect():
    g.conn = MongoClient(os.environ['DB_HOST'], int(os.environ['DB_PORT']))
    g.db = g.conn['cd_api']

@app.route("/")
def index():
    return redirect("https://github.com/stevenleeg/campusdish_api/blob/master/README.md")

class Location(Resource):
    def get(self, location, meal):
        coll = g.db['dishes']

        current = datetime.date.today()
        week_begin = current - datetime.timedelta(days = (current.weekday() + 1 % 6))
        week_begin = datetime.datetime(week_begin.year, week_begin.month, week_begin.day)
        week_end = week_begin + datetime.timedelta(days = 7)

        dishes = coll.find({ 
            "location": location, 
            "meal": meal,
            #"date": { "$gte": week_begin, "$lt": week_end }
            "date": datetime.datetime(current.year, current.month, current.day),
        }).sort("station")

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
