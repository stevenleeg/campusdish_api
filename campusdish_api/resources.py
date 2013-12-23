from flask.ext.restful import Resource, abort
from campusdish_api.models import DiningHall, Meal
from sqlalchemy import func
import datetime

class DiningHallResource(Resource):
    def get(self, location, meal):
        dining_hall = DiningHall.query.filter(
            func.lower(DiningHall.name) == func.lower(location)).first()
        if dining_hall == None:
            abort(404, message = "Location does not exist")

        meal = Meal.query.filter_by(name = meal).first()
        if meal == None:
            abort(404, message = "Invalid meal")

        date = datetime.date(2013, 12, 21)

        stations = {}
        for station in dining_hall.stations:
            dishes = []

            q_dishes = station.dish_instances.filter_by(date = date).all()
            for dish in q_dishes:
                dishes.append({
                    "title": dish.dish.name,
                })

            if len(q_dishes) > 0:
                stations[station.name] = dishes

        return { 
            "status": 200,
            "date": str(date),
            "stations": stations,
            "meal": meal.name
        }

