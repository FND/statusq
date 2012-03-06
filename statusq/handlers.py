from __future__ import absolute_import, division, with_statement

import os

from flask import g, request, url_for, redirect, abort, make_response, \
        send_from_directory, render_template
from flask.views import MethodView

from . import app, database
from .auth import requires_auth, authenticate


@app.before_request
def before_request():
    g.db = database.connect(app) # XXX: not required for every request


@app.teardown_request
def teardown_request(exc):
    pass # no need to explicitly close the database connection


@app.route("/", methods=["GET", "POST"])
def root():
    from . import messages # TODO: rename module

    username = request.authorization.username if request.authorization else None

    if request.method == "GET":
        posts = messages.stream(username) if username else None
        return render_template("frontpage.html", posts=posts)
    elif request.method == "POST":
        if not username:
            abort(401)
        msg = request.form["msg"]
        messages.create(username, msg)
        if not _is_browser():
            return make_response(None, 204)
        else:
            return redirect(url_for("root"))


@app.route("/api") # XXX: rename?
def api(): # TODO: include handlers' docstrings
    links = ['<li><a href="%s">%s</a></li>' % (rule.rule, rule.rule)
            for rule in app.url_map.iter_rules() if "GET" in rule.methods]
    return "<ul>%s</ul>" % "\n".join(links)


class Users(MethodView):

    def get(self):
        return render_template("user.html")

    def post(self): # TODO: special responses for browsers
        """
        create user

        responses (except for browsers, which are special-cased):
        204 success
        409 username already exists
        """
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if g.db.get("users:%s" % username):
            abort(409)
        # TODO: further validate input

        uid = g.db.incr("users:enum")
        pipe = g.db.pipeline()
        pipe.set("users:%s:uid" % username, uid) # XXX: unnecessary?
        pipe.set("users:%s" % username, password) # TODO: hash password
        pipe.sadd("users", username)
        pipe.execute() # TODO: check results
        watch(username, username) # XXX: DEBUG?

        if not _is_browser():
            return make_response(None, 204)
        else:
            return redirect(url_for("login"))

app.add_url_rule("/users", view_func=Users.as_view("users")) # TODO: move elsewhere


@app.route("/login")
@requires_auth
def login():
    return request.authorization.__str__() # TODO: return to origin


@app.route("/favicon.ico") # NB: should be served directly by the web server
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
            "favicon.ico", mimetype="image/vnd.microsoft.icon")


def watch(username, *overlords):
    for overlord in overlords:
        g.db.sadd("users:%s:overlords" % username, overlord)
        g.db.sadd("users:%s:minions" % overlord, username)


def unwatch(username, *overlords):
    for overlord in overlords:
        g.db.sadd("users:%s:overlords" % username, overlord)
        g.db.sadd("users:%s:minions" % overlord, username)


def _is_browser():
    """
    fugly hack to special-case browser responses
    """
    return request.accept_mimetypes.best == "text/html"
