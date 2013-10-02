from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from model import Dish, db_connect, create_table

class PostgresPipeline(object):
    def open_spider(self, spider):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind = engine)

    def process_item(self, item, spider):
        print "%s::%s::%s::%s" % (item['location'], item['station'], item['date'], item['title'])
        session = self.Session()
        item = Dish(**item)
        item.generate_id()

        # See if it already exists
        count = session.query(Dish).filter(Dish.id == item.id).count()
        if count != 0:
            print "Skipping!"
            session.close()
            return item

        session.add(item)
        session.commit()
        session.close()

        return item
