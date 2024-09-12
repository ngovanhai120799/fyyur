import json
import os
import ulid

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import config

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(config_mode):
    """Application-factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_mode])

    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()

    return app


mode = os.environ.get('CONFIG_MODE')
app = create_app(mode)

if __name__ == '__main__':
    app.run()
