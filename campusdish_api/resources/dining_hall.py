from flask.ext.restful import Resource

class DiningHall(Resource):
    def get(self, location, meal):
        # TODO: Select code

        stations = {}
        for dish in dishes:
            if dish['station'] not in stations:
                stations[dish['station']] = []
            
            stations[dish['station']].append({ 
                "title": dish['title'],
                "date": str(dish['date'])[0:10]
            })

        return { 
            "status": 200,
            "stations": stations,
            "meal": meal
        }

