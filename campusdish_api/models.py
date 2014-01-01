from flask.ext.sqlalchemy import SQLAlchemy
from campusdish_api import app
import datetime, os

#
# Setup database
#
db_uri = "postgres://%s:%s@%s:%s/%s" % (
    os.environ['DB_USER'],
    os.environ['DB_PASS'],
    os.environ['DB_HOST'],
    os.environ['DB_PORT'],
    os.environ['DB_NAME'],
)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)

class DiningHall(db.Model):
    """
    Represents a dining hall. This is *not* populated by the scraper and must be
    manually filled. You can find an example of how to populate it in the first
    database migration script.
    """
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    menu_url = db.Column(db.String)
    page_str = db.Column(db.String)
    org_id = db.Column(db.String)

    def getState(self, debug = False):
        """
        Returns false if the dining hall is closed or a DiningHallSchedule
        if it is open
        """
        today = datetime.date.today()
        dt_now = datetime.datetime.now()
        now = datetime.time(dt_now.hour, dt_now.minute)

        # Mock data for testing
        if debug:
            schedule = DiningHallSchedule()
            schedule.open_time = datetime.time(8, 0)
            schedule.close_time = datetime.time(22, 0)
            return schedule

        schedules = self.schedules.filter(
            DiningHallSchedule.date_begin <= today,  
            DiningHallSchedule.date_end >= today).order_by(DiningHallSchedule.regular_schedule.desc())

        ids = []
        for schedule in schedules:
            ids.append(schedule.id)
            dow_str = today.strftime("%a")
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
    
    def menuAvailable(self, date):
        """
        Returns true if there is a menu available for the given datetime.date, 
        otherwise false.
        """
        count = DiningHall.query\
            .join(DiningHall.stations)\
            .join(Station.dish_instances)\
            .filter(DishInstance.date == date)\
            .count()

        return (count > 0)

    def __repr__(self):
        return self.name.capitalize()
        
class DiningHallSchedule(db.Model):
    """
    Represents all the times that a dining hall is scheduled to be open.
    """
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
    """
    A station is exactly what you think it is: a station within a dining hall.
    """
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    dining_hall_id = db.Column(db.Integer, db.ForeignKey("dining_hall.id"))
    dining_hall = db.relationship(
        'DiningHall', backref=db.backref("stations"))

    def __init__(self, name = None, dining_hall = None):
        self.name = name
        if dining_hall != None:
            self.dining_hall_id = dining_hall.id
            self.dining_hall = dining_hall

    def getDishes(self, date, meal, debug = False):
        if debug:
            return self.dish_instances.filter_by(meal_id = meal.id).limit(3)

        return self.dish_instances.filter_by(
            date = date, 
            meal_id = meal.id).all()

    def __repr__(self):
        return self.name.capitalize()
    
class Dish(db.Model):
    """
    A dish is something like pasta, which would be served at the pasta station.
    This does *not* store the actual menus, just the items that could appear on
    a menu. Dates that dishes are served are represented by DishInstances
    """
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)

    def __init__(self, name = None):
        self.name = name

    def __repr__(self):
        return self.name.capitalize()

class Meal(db.Model):
    """
    The meal model represents various meals through the day and generally
    doesn't change after the first scrape (eg, breakfast, lunch, and dinner).
    """
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)

    def __init__(self, name = None):
        self.name = name

    def __repr__(self):
        return self.name.capitalize()

class DishInstance(db.Model):
    """
    A dishinstance is an instance of a dish on a particular day's menu and
    station.
    """
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

    def __init__(self, dish = None, date = None, meal = None, station = None):
        if dish != None:
            self.dish = dish
            self.dish_id = dish.id

        if meal != None:
            self.meal = meal
            self.meal_id = meal.id

        if station != None:
            self.station = station
            self.station_id = station.id

        self.date = date
