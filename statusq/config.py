"""
default configuration
"""


class Config(object):
    DEBUG = False
    TESTING = False
    # SECRET_KEY populated automatically during initialization


class ProductionConfig(Config):
    DATABASE = {
      "host": "localhost",
      "port": 6379,
      "redis_db": 0
    }


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = {
      "host": "localhost",
      "port": 6379,
      "redis_db": 1
    }


class TestingConfig(Config):
    TESTING = True
    DATABASE = {
      "host": "localhost",
      "port": 6379,
      "redis_db": 2
    }
