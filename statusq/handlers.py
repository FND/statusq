from __future__ import absolute_import, division, with_statement

import os

from flask import g, send_from_directory

from . import app


@app.route("/")
def root():
    links = ['<li><a href="%s">%s</a></li>' % (rule.rule, rule.rule)
            for rule in app.url_map.iter_rules() if "GET" in rule.methods]
    return "<ul>%s</ul>" % "\n".join(links)


@app.route("/favicon.ico") # NB: should be served directly by the web server
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
            "favicon.ico", mimetype="image/vnd.microsoft.icon")
