import os
from dotenv import load_dotenv

SECRET_KEY = os.urandom(32)
load_dotenv()

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

CONFIG_MODE = os.environ["CONFIG_MODE"]
SQLALCHEMY_DATABASE_URI = os.environ["DEVELOPMENT_DATABASE_URL"]


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI


config = {
    "development": DevelopmentConfig
}
