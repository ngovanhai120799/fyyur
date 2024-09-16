from flask import Flask

from config import (config, CONFIG_MODE)
from models import (db, migrate)
from routes.index import api


def create_app():
    """Application-factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[CONFIG_MODE])
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(api)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
