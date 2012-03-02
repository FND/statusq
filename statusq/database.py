from redis import StrictRedis


def connect(app):
    cfg = app.config["DATABASE"]
    return StrictRedis(host=cfg["host"], port=cfg["port"], db=cfg["redis_db"])
