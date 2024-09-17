from flask import Flask

from config import (config, CONFIG_MODE)
from models import (db, migrate)

from routes.venue import venue_route
from routes.artist import artist_route
from routes.index import api
from routes.show import show_route


def create_app():
    """Application-factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[CONFIG_MODE])
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(venue_route)
    app.register_blueprint(artist_route)
    app.register_blueprint(show_route)
    app.register_blueprint(api)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
