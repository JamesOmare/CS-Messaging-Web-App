from decouple import config
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = config('DEBUG')
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
   