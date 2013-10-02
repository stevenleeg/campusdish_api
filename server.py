from flask import Flask, redirect
from flask.ext.restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    return redirect("https://github.com/stevenleeg/campusdish_api/blob/master/README.md")

class Location(Resource):
    def get(self, location):
        return { "hello": location }

api.add_resource(Location, "/v1/location/<string:location>")

if __name__ == "__main__":
    app.run(debug = True)
