from scrapy.exceptions import DropItem

class PostgresPipeline(object):
    def open_spider(self, spider):
        # TODO: DB stuff
        return

    def process_item(self, item, spider):
        print "%s::%s::%s::%s" % (item['location'], item['station'], item['date'], item['title'])

    def close_spider(self, spider):
        # TODO: Moar db stuff
        return
