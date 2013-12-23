from campusdish_api import api
import campusdish_api.resources as resources


api.add_resource(resources.DiningHallResource, "/v0/dining_hall/<string:location>/<string:meal>")
api.add_resource(resources.DiningHallsResource, "/v0/dining_hall")
api.add_resource(resources.MealsResource, "/v0/meal")
