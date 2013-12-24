from functools import wraps
from flask import request, Response
import os

def check_auth(password):
    acceptable = os.environ["ADM_PASS"]
    return True if password == acceptable else False

def authenticate():
    return Response(
        "Please authenticate to continue", 
        401,
        { "WWW-Authenticate": "Basic realm=\"Login required\""})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.password):
            return authenticate()

        return f(*args, **kwargs)

    return decorated
