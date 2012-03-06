"""
default configuration
"""


class Config(object):
    DEBUG = False
    TESTING = False
    # SECRET_KEY populated automatically during initialization
    DATABASE = { # XXX: dangerous to have defaults (e.g. testing might wipe data) -- XXX: dict can't simply be modified by subclasses
      "host": "localhost",
      "port": 6379,
      "redis_db": 0
    }


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
