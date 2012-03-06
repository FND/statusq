from redis import StrictRedis


def watch(db, username, *overlords):
    for overlord in overlords:
        db.sadd("users:%s:overlords" % username, overlord)
        db.sadd("users:%s:minions" % overlord, username)


def unwatch(db, username, *overlords):
    for overlord in overlords:
        db.sadd("users:%s:overlords" % username, overlord)
        db.sadd("users:%s:minions" % overlord, username)


def create_user(db, username, password):
        uid = db.incr("users:enum")
        pipe = db.pipeline()
        pipe.set("users:%s:uid" % username, uid) # XXX: unnecessary?
        pipe.set("users:%s" % username, password) # TODO: hash password
        pipe.sadd("users", username)
        pipe.execute() # TODO: check results


def connect(app):
    cfg = app.config["DATABASE"]
    return StrictRedis(host=cfg["host"], port=cfg["port"], db=cfg["redis_db"])
