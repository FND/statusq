from __future__ import absolute_import, division, with_statement

import os

from redis import StrictRedis

from flask import g, request, abort, make_response, send_from_directory, \
        render_template
from flask.views import MethodView

from . import app


@app.before_request
def before_request(): # XXX: not required for every request
    cfg = app.config["DATABASE"]
    g.db = StrictRedis(host=cfg["host"], port=cfg["port"], db=cfg["redis_db"])


@app.teardown_request
def teardown_request(exc):
    pass # no need to explicitly close the database connection


@app.route("/")
def root():
    return render_template("user.html")


@app.route("/api") # XXX: rename?
def api(): # TODO: include handlers' docstrings
    links = ['<li><a href="%s">%s</a></li>' % (rule.rule, rule.rule)
            for rule in app.url_map.iter_rules() if "GET" in rule.methods]
    return "<ul>%s</ul>" % "\n".join(links)


class Users(MethodView):

    def post(self): # TODO: special responses for browsers
        """
        create user

        responses:
        204 success
        409 username already exists
        """
        username = request.form["username"]
        password = request.form["password"]

        if g.db.get("users:%s" % username):
            abort(409)
        # TODO: further validate input

        uid = g.db.incr("users:enum")
        pipe = g.db.pipeline()
        pipe.set("users:%s:uid" % username, uid) # XXX: unnecessary?
        pipe.set("users:%s" % username, password) # TODO: hash password
        pipe.sadd("users", username)
        pipe.execute() # TODO: check results

        return make_response(None, 204)

app.add_url_rule("/users", view_func=Users.as_view("users")) # TODO: move elsewhere


@app.route("/favicon.ico") # NB: should be served directly by the web server
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
            "favicon.ico", mimetype="image/vnd.microsoft.icon")
