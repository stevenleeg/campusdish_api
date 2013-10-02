from scrapy.item import Item, Field

class Dish(Item):
    title = Field()
    date = Field()
    location = Field()
