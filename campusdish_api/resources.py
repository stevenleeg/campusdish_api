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

        date = datetime.date.today()

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
        dining_halls = DiningHall.query.all()
        resp = {}
        for hall in dining_halls:

            state = hall.getState()
            if state != False:
                resp[hall.name] = {
                    "state": True,
                    "opens": str(state.open_time),
                    "closes": str(state.close_time),
                }
            else:
                next_open = hall.getNextOpen()
                resp[hall.name] = {
                    "state": state,
                    "next_open": str(next_open) if next_open else None,
                }

        return {
            "status": 200,
            "dining_halls": resp,
        }
