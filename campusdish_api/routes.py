from campusdish_api import api, app
from campusdish_api.app import api_index
import campusdish_api.resources as resources

api.add_resource(resources.DiningHallResource, "/v0/dining_hall/<string:location>/<string:meal>")
api.add_resource(resources.DiningHallsResource, "/v0/dining_hall")
api.add_resource(resources.MealsResource, "/v0/meal")
api.add_resource(resources.ScheduleResource, "/v0/schedule")

app.add_url_rule("/", "api_index", api_index)
