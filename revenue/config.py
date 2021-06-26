import os


basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_url = 'sqlite:///' + os.path.join(basedir, 'api/revenue.db')


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", sqlite_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False



