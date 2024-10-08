from flask import Flask

from starter_code.config import (config, CONFIG_MODE)
from starter_code.models import (db, migrate)

from starter_code.routes.venue import venue_route
from starter_code.routes.artist import artist_route
from starter_code.routes.show import show_route
from starter_code.routes.index import home_route


def create_app():
    """Application-factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[CONFIG_MODE])
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(venue_route)
    app.register_blueprint(artist_route)
    app.register_blueprint(show_route)
    app.register_blueprint(home_route)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
