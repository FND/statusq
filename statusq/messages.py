from time import time

from pretty import date as pretty_date

from flask import g


def create(username, msg):
    # TODO: validate message
    pid = g.db.incr("posts:enum")

    pipe = g.db.pipeline()
    pipe.set("posts:%s" % pid, msg)
    pipe.set("posts:%s:author" % pid, username)
    pipe.set("posts:%s:timestamp" % pid, time())
    pipe.lpush("posts", pid)
    pipe.lpush("posts:%s" % username, pid)
    pipe.execute() # TODO: check results

    for minion in g.db.smembers("users:%s:minions" % username):
        g.db.lpush("users:%s:stream" % minion, pid) # TODO: use pipe
    # TODO: mentions
    #for user in extract_usernames($txt)
    #    LPUSH users:$user:pings $pid


def stream(username, _type="overlords"): # TODO: rename function, `_type` argument
    if _type == "overlords":
        key = "users:%s:%s" % (username, "stream")
    elif _type == "all":
        key = "posts:%s" % username
    else:
        raise TypeError("invalid stream type")

    posts = g.db.lrange(key, 0, 10)

    for pid in posts:
        msg = g.db.get("posts:%s" % pid)
        author = g.db.get("posts:%s:author" % pid)
        timestamp = float(g.db.get("posts:%s:timestamp" % pid))
        yield {
            "author": author,
            "timestamp": timestamp, # XXX: should be ISO 8601
            "reltime": pretty_date(int(timestamp)), # XXX: move to template?
            "message": msg
        }
