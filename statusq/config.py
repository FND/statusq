"""
default configuration
"""

class Config(object):
    DEBUG = False
    TESTING = False
    # SECRET_KEY populated automatically during initialization
    DATABASE = None


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
