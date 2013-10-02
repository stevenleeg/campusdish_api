from scrapy.item import Item, Field

class Dish(Item):
    title = Field()
    station = Field()
    date = Field()
    location = Field()
