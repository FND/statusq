from functools import wraps

from flask import request, Response

from . import app, database


def requires_auth(f):
    """
    authentication decorator
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def check_auth(username, password):
    """
    validates username / password combinations
    """
    db = database.connect(app) # XXX: we're already connected!?
    return password == db.get("users:%s" % username) # TODO: hash password


def authenticate():
    """
    sends a 401 response to trigger HTTP Basic Auth prompt
    """
    return Response("Please log in", 401,
            { "WWW-Authenticate": 'Basic realm="Login Required"' })
