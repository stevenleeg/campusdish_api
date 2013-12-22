from flask.ext.restful import Resource, abort
import campusdish_api.models as models
import datetime

class DiningHallResource(Resource):
    def get(self, location, meal):
        dining_hall = models.DiningHall.query.filer_by(name = location).first()
        if dining_hall == None:
            abort(404, message = "Location does not exist")

        meal = models.Meal.query.filter_by(name = meal).first()
        if meal == None:
            abort(404, message = "Invalid meal")

        today = datetime.date.today()

        stations = {}
        for station in dining_hall.station:
            dishes = []

            dishes = station.dish_instances.query.filter_by(date = today)
            for dish in dishes:
                dishes.append({
                    "title": dish.name,
                })
        
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

