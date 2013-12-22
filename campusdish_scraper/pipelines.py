from campusdish_api.models import DiningHall, Station, Dish, DishInstance
from campusdish_api import db 
from scrapy.exceptions import DropItem
import hashlib, os, datetime

class SqlAlchemyPipeline(object):
    def open_spider(self, spider):
        self.dining_halls = {}
        self.stations = {}
        for dining_hall in DiningHall.query.all():
            self.dining_halls[dining_hall.name] = dining_hall
            self.stations[dining_hall.name] = {}

            for station in dining_hall.stations:
                self.stations[dining_hall.name][station.name] = station
    
    def close_spider(self, spider):
        db.session.commit()
        db.session.remove()

    def process_item(self, item, spider):
        item_hash = hashlib.md5(
            item['location'] 
            + item['station'] 
            + item['meal']
            + item['title'] 
            + str(item['date'])
        )
        
        dining_hall = self.dining_halls[item['location']]

        # Does the station exist yet?
        if item['station'] not in self.stations[item['location']]:
            station = Station(item['station'], dining_hall)
            self.stations[item['location']][station.name] = station
            db.session.add(station)
        else:
            station = self.stations[item['location']][item['station']]
        
        # Does this dish exist yet?
        dish = Dish.query.filter_by(
            name = item['title'],
            station = station,
        ).first()

        if dish == None:
            dish = Dish(item['title'], station)
            db.session.add(dish)

        # What about this instance?
        inst = DishInstance.query.filter_by(
            dish = dish,
            date = item['date'],
            meal = item['meal']
        ).first()

        if inst == None:
            inst = DishInstance(dish, item['date'], item['meal'])
            db.session.add(inst)

        return item
