import os
from dotenv import load_dotenv

load_dotenv()

CONFIG_MODE = os.environ["CONFIG_MODE"]
SQLALCHEMY_DATABASE_URI = os.environ["DEVELOPMENT_DATABASE_URL"]


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI


config = {
    "development": DevelopmentConfig
}
