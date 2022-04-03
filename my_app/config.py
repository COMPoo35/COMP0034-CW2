"""Flask config class."""
import pathlib


class Config(object):
    SECRET_KEY = 'Oe2VTPHqLagq6BrB6rci4w'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_PATH = pathlib.Path(__file__).parent.parent.joinpath("data")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(DATA_PATH.joinpath('my_app.sqlite'))
    UPLOADED_PHOTOS_DEST = pathlib.Path(__file__).parent.joinpath("static/img")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    ENV = 'testing'
    DEBUG = False
    SQLALCHEMY_ECH0 = True
