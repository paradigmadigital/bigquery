from functools import wraps
from flask import request, Response
import os


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    valid_user = os.environ.get('AUTH_USER')
    valid_pass = os.environ.get('AUTH_PASS')

    if valid_user and valid_pass:
        return username == valid_user and password == valid_pass
    else:
        return True

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
