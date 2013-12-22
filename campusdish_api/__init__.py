from flask import Flask, redirect, g
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from campusdish_api.resources import DiningHall
import os

app = Flask(__name__)
api = Api(app)

# Setup database
db_uri = "postgres://%s:%s@%s:%s/%s" % (
    os.environ['DB_USER'],
    os.environ['DB_PASS'],
    os.environ['DB_HOST'],
    os.environ['DB_PORT'],
    os.environ['DB_NAME'],
)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
import models

# Add resources
api.add_resource(DiningHall, "/v1/dining_hall/<string:location>/<string:meal>")

if __name__ == "__main__":
    app.run(debug = True)
