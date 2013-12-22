from flask.ext.sqlalchemy import SQLAlchemy
from campusdish_api import app
db = SQLAlchemy(app)

class DiningHall(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    menu_url = db.Column(db.String)
    page_str = db.Column(db.String)
    org_id = db.Column(db.String)

class Station(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    dining_hall_id = db.Column(db.Integer, db.ForeignKey("dining_hall.id"))
    dining_hall = db.relationship(
        'DiningHall', backref=db.backref("stations"))

    def __init__(self, name, dining_hall):
        self.name = name
        self.dining_hall_id = dining_hall.id
        self.dining_hall = dining_hall
    
class Dish(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"))
    station = db.relationship(
        'Station', backref=db.backref("dishes"))

    def __init__(self, name, station):
        self.name = name
        self.station = station
        self.station_id = station.id

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

class DishInstance(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.Date)

    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"))
    meal = db.relationship(
        'Meal', backref=db.backref("dish_instances"))

    station_id = db.Column(db.Integer, db.ForeignKey("station.id"))
    station = db.relationship(
        'Station', backref=db.backref("dish_instances"))

    dish_id = db.Column(db.Integer, db.ForeignKey("dish.id"))
    dish = db.relationship(
        'Dish', backref=db.backref("instances"))

    def __init__(self, dish, date, meal):
        self.dish = dish
        self.dish_id = dish.id

        self.meal = meal
        self.meal_id = meal.id

        self.station = self.dish.station
        self.station_id = self.dish.station_id

        self.date = date
