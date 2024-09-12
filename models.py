from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import (config, CONFIG_MODE)

db = SQLAlchemy()
migrate = Migrate()


# MODELS Section
genre_of_venue = db.Table(
    'genre_of_venue',
    db.Column('venue_id', db.String(), db.ForeignKey('venues.id')),
    db.Column('genre_id', db.String(), db.ForeignKey('genres.id'))
)

genre_of_artist = db.Table(
    'genre_of_artist',
    db.Column('artist_id', db.String(), db.ForeignKey('artists.id')),
    db.Column('genre_id', db.String(), db.ForeignKey('genres.id'))
)

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String())
    state = db.Column(db.String())
    phone = db.Column(db.String())
    website = db.Column(db.String())
    facebook_link = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    image_link = db.Column(db.String())
    genres = db.relationship("Genre", secondary=genre_of_venue, backref=db.backref('venues'))


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.relationship("Genre", secondary=genre_of_artist, backref=db.backref('artists'))


class Show(db.Model):
    __tablename__ = 'shows'
    venue_id = db.Column(db.String(), db.ForeignKey('venues.id'), primary_key=True)
    artist_id = db.Column(db.String(), db.ForeignKey('artists.id'), primary_key=True)
    venue_name = db.Column(db.String())
    artist_name = db.Column(db.String())
    start_time = db.Column(db.DateTime)

def create_app(app, config_mode=CONFIG_MODE):
    """Application-factory pattern"""
    app.config.from_object(config[config_mode])
    db.init_app(app)
    migrate.init_app(app, db)
    return app
