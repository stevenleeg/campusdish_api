from flask.ext.restful import Api, Resource, abort
from flask import request
from campusdish_api.models import DiningHall, Meal
from campusdish_api import app
from sqlalchemy import func
import datetime

api = Api(app)

class DiningHallResource(Resource):
    def get(self, location, meal):
        debug = (request.args.get("debug", False) != False)

        dining_hall = DiningHall.query.filter(
            func.lower(DiningHall.name) == func.lower(location)).first()
        if dining_hall == None:
            abort(404, message = "Location does not exist")

        meal = Meal.query.filter_by(name = meal).first()
        if meal == None:
            abort(404, message = "Invalid meal")

        date = datetime.date.today()

        stations = {}
        for station in dining_hall.stations:
            q_dishes = station.getDishes(date, meal, debug = debug)
            dishes = []

            for dish in q_dishes:
                dishes.append({
                    "title": dish.dish.name,
                })

            if len(dishes) > 0:
                stations[station.name] = dishes

        return { 
            "status": 200,
            "date": str(date),
            "stations": stations,
            "meal": meal.name
        }


class DiningHallsResource(Resource):
    def get(self):
        dining_halls = []
        q_dining_halls = DiningHall.query.all()

        for dining_hall in q_dining_halls:
            dining_halls.append({
                "name": dining_hall.name,
            })

        return {
            "status": 200,
            "dining_halls": dining_halls
        }

class MealsResource(Resource):
    def get(self):
        meals = []
        q_meals = Meal.query.all()

        for meal in q_meals:
            meals.append({
                "name": meal.name,
            })

        return {
            "status": 200,
            "meals": meals
        }

class ScheduleResource(Resource):
    def get(self):
        debug = (request.args.get("debug", False) != False)
        dining_halls = DiningHall.query.all()
        resp = {}
        for hall in dining_halls:
            state = hall.getState(debug = debug)
            if state != False:
                resp[hall.name] = {
                    "state": True,
                    "opened": str(state.open_time),
                    "closes": str(state.close_time),
                }
            else:
                next_open = hall.getNextOpen()
                menu_available = False
                if next_open != None:
                    menu_available = hall.menuAvailable(next_open.date())

                resp[hall.name] = {
                    "state": state,
                    "next_open": str(next_open) if next_open else None,
                    "menu_available": menu_available,
                }

        return {
            "status": 200,
            "dining_halls": resp,
        }
