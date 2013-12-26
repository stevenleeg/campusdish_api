from flask import request, Response
from flask.ext.admin import BaseView, expose, AdminIndexView, Admin
from flask.ext.admin.contrib.sqla import ModelView
from campusdish_api.auth import requires_auth
from campusdish_api.models import *
from campusdish_api import app
import os

def is_accesible():
    acceptable = os.environ["ADM_PASS"]
    auth = request.authorization
    if auth == None:
        return False
    return True if auth.password == acceptable else False

class AuthIndexView(AdminIndexView):
    def is_accessible(self):
        return is_accesible()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return Response(
                "Please authenticate to continue", 
                401,
                { "WWW-Authenticate": "Basic realm=\"Login required\""})

class AuthModelView(ModelView):
    def is_accessible(self):
        return is_accesible()

admin = Admin(app, 
    name = "Campusdish API",
    index_view = AuthIndexView()
)
admin.add_view(AuthModelView(DiningHall, db.session)) 
admin.add_view(AuthModelView(DiningHallSchedule, db.session)) 
