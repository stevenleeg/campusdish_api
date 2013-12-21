from scrapy.spider import BaseSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from scraper.items import Dish
import re, os, datetime

HALLS = {
    "danforth": "DanforthFreshFoodCompany.htm",
    "douglass": "DouglassDiningCenter.htm",
    "commons":  "TheCommons.htm",
}
URL_LOCATIONS = {
    "douglass": "Douglass%20Dining%20Center",
    "danforth": "Danforth%20Fresh%20Food%20Company",
    "commons":  "The%20Commons",
}
BASE_URL = "http://www.campusdish.com/en-US/CSNE/Rochester/Menus/"
ORG_ID = 195030

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
        current_meal_id = int(meals_list.select("option[@selected]/@value").extract()[0])
        meals_available = [int(x) for x in meals_list.select("option/@value").extract()]

        current = datetime.date.today()
        wk_begin = current - datetime.timedelta(days = (current.weekday() + 1 % 6))
        if "terminal" not in response.meta:
            for meal in meals_available:
                if(meal == current_meal_id):
                    continue

                req = Request(
                    BASE_URL + HALLS[response.meta["dining_hall"]] + "?"
                    + "LocationName=%s&" % URL_LOCATIONS[response.meta["dining_hall"]]
                    + "MealID=%d&" % meal
                    + "OrgID=%d&" % ORG_ID
                    + "Date=%d_%d_%d&" % (wk_begin.month, wk_begin.day, wk_begin.year)
                    + "ShowPrice=False&ShowNutrition=True",
                    callback = self.parse
                )

                req.meta['dining_hall'] = response.meta['dining_hall']
                req.meta['terminal'] = True
                yield req

        print "%s, parsed! Current meal: %s" % (response.meta["dining_hall"], current_meal)

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
        one_day = datetime.timedelta(1)
        meal_items = []
        for i, station in enumerate(stations):
            # Get a reference to the beginning of the week
            current = datetime.date.today()
            current = current - datetime.timedelta(days = (current.weekday() + 1 % 6))

            station_n = (i + 1) * 2
            days = main_data.select("table[%d]/tr[2]/td" % station_n)

            print "Station %s meals:" % station
            for day in days:
                meals = day.select("table/tr/td/div[@class='menuTxt']/table/tr/td[1]/a/text()").extract()
                print "\t%s: %s" % (current.strftime("%m-%d-%y"), meals)

                # Create the dish
                for meal in meals:
                    item = Dish()
                    item['location'] = response.meta['dining_hall']
                    item['station'] = station
                    item['meal'] = current_meal
                    item['title'] = meal.lower()
                    item['date'] = current

                    yield item

                current += one_day

    def start_requests(self):
        danforth = Request(BASE_URL + HALLS["danforth"])
        danforth.meta["dining_hall"] = "danforth"

        douglass = Request(BASE_URL + HALLS["douglass"])
        douglass.meta["dining_hall"] = "douglass"

        commons = Request(BASE_URL + HALLS["commons"])
        commons.meta["dining_hall"] = "commons"
        return [danforth, douglass, commons]
