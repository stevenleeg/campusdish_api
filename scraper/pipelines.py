from pymongo import MongoClient
from scrapy.exceptions import DropItem
import hashlib, os, datetime

class MongoPipeline(object):
    def open_spider(self, spider):
        self.conn = MongoClient(os.environ['DB_HOST'], int(os.environ['DB_PORT']))
        self.db = self.conn['cd_api']
        self.dishes = self.db['dishes']

    def process_item(self, item, spider):
        item_hash = hashlib.md5(
            item['location'] 
            + item['station'] 
            + item['title'] 
            + str(item['date'])
        )
        
        # Does this already exist in the database?
        if self.dishes.find_one({ "_id": item_hash.hexdigest() }) != None:
            raise DropItem("Item already exists in database")

        # Convert date to datetime for BSON encoding
        date = datetime.datetime(item['date'].year, item['date'].month, item['date'].day)

        db_item = {
            "_id": item_hash.hexdigest(),
            "location": item['location'],
            "station": item['station'],
            "title": item['title'],
            "date": date
        }

        self.dishes.insert(db_item)

        return item
