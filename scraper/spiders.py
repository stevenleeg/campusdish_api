from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scraper.items import Dish
import re, os

HALL_MENU_URLS = {
    "danforth": "http://www.campusdish.com/en-US/CSNE/Rochester/Menus/DanforthFreshFoodCompany.htm",
    "douglass": "http://www.campusdish.com/en-US/CSNE/Rochester/Menus/DouglassDiningCenter.htm"
}

class DishSpider(BaseSpider):
    name = "dish_spider"
    allowed_domains = ["campusdish.com"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        #
        # Meals available
        #
        meals_list = hxs.select("//select[@name='ucFiveDayMenu:cboMeal']")
        current_meal = meals_list.select("option[@selected]/text()").extract()[0].lower()
        meals_available = [x.lower() for x in meals_list.select("option/text()").extract()]

        print "%s, parsed! Current meal: %s" % (response.meta["dining_hall"], current_meal)
        print "Meals available:"
        for meal in meals_available:
            print "\t%s" % meal

        main_data = hxs.select("//div[@id='ucFiveDayMenu_MenuArea']")
        #
        # Let's look at the stations
        #
        stations_list = main_data.select("table[@class='ConceptTab']")
        stations = [x.lower() for x in stations_list.select("tr[2]/td[1]/text()").extract()]
        
        print "Stations:"
        for station in stations:
            print "\t%s" % station

        #
        # And now each menu for the station
        #
        for i, station in enumerate(stations):
            station_n = (i + 1) * 2
            days = main_data.select("table[%d]/tr/td" % station_n)

            print "Station %s meals:" % station
            for day in days:
                meals = day.select("table/tr/td/div[@class='menuTxt']/table/tr/td/a/text()").extract()
                if len(meals) > 0:
                    print "\t%s" % meals

    def start_requests(self):
        danforth = Request(HALL_MENU_URLS["danforth"])
        danforth.meta["dining_hall"] = "Danforth"
        douglass = Request(HALL_MENU_URLS["douglass"])
        douglass.meta["dining_hall"] = "Douglass"
        return [danforth, douglass]
