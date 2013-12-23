from flask.ext.sqlalchemy import SQLAlchemy
from campusdish_api import app
from sqlalchemy import or_, and_
import datetime
db = SQLAlchemy(app)

class DiningHall(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    menu_url = db.Column(db.String)
    page_str = db.Column(db.String)
    org_id = db.Column(db.String)

    def getState(self):
        """
        Returns false if the dining hall is closed or a DiningHallSchedule
        if it is open
        """
        today = datetime.date.today()
        dt_now = datetime.datetime.now()
        now = datetime.time(dt_now.hour, dt_now.minute)
        schedules = self.schedules.filter(
            DiningHallSchedule.date_begin <= today,  
            DiningHallSchedule.date_end >= today).order_by(DiningHallSchedule.regular_schedule.desc())

        ids = []
        for schedule in schedules:
            ids.append(schedule.id)
            dow_str = today.strftime("%a")[0]
            if dow_str in schedule.days_of_week and schedule.open_time <= now and schedule.close_time >= now:
                return schedule

        return False

    def getNextOpen(self):
        """
        Returns a datetime consisting of the next time this dining hall will open
        """
        today = datetime.date.today()
        dt_now = datetime.datetime.now()
        now = datetime.time(dt_now.hour, dt_now.minute)
        schedule = self.schedules\
            .filter(DiningHallSchedule.date_begin >= today)\
            .order_by(DiningHallSchedule.date_begin).first()

        if schedule == None:
            return None
        
        dt = datetime.datetime(
            schedule.date_begin.year, 
            schedule.date_begin.month,
            schedule.date_begin.day,
            schedule.open_time.hour,
            schedule.open_time.minute)

        return dt

        
class DiningHallSchedule(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    dining_hall_id = db.Column(db.Integer, db.ForeignKey("dining_hall.id"))
    dining_hall = db.relationship(
        'DiningHall', backref=db.backref("schedules", lazy="dynamic"))
    
    open_time = db.Column(db.Time)
    close_time = db.Column(db.Time)

    date_begin = db.Column(db.Date)
    date_end = db.Column(db.Date)
    days_of_week = db.Column(db.String)

    regular_schedule = db.Column(db.Boolean)

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
        'Station', backref=db.backref("dishes", lazy="dynamic"))

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
        'Meal', backref=db.backref("dish_instances", lazy="dynamic"))

    station_id = db.Column(db.Integer, db.ForeignKey("station.id"))
    station = db.relationship(
        'Station', backref=db.backref("dish_instances", lazy="dynamic"))

    dish_id = db.Column(db.Integer, db.ForeignKey("dish.id"))
    dish = db.relationship(
        'Dish', backref=db.backref("instances", lazy="dynamic"))

    def __init__(self, dish, date, meal):
        self.dish = dish
        self.dish_id = dish.id

        self.meal = meal
        self.meal_id = meal.id

        self.station = self.dish.station
        self.station_id = self.dish.station_id

        self.date = date
