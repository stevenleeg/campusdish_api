from campusdish_api import db

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
    
class Meal(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    station_id = db.Column(db.Integer, db.ForeignKey("station.id"))
    station = db.relationship(
        'Station', backref=db.backref("meals"))

class MealInstance(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.Date)
    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"))
    meal = db.relationship(
        'Meal', backref=db.backref("instances"))
