from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

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

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


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

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String())
    state = db.Column(db.String())
    phone = db.Column(db.String())
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String())
    genres = db.relationship("Genre", secondary=genre_of_artist, backref=db.backref('artists'))

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.String(), primary_key=True)
    venue_id = db.Column(db.String(), db.ForeignKey('venues.id'))
    artist_id = db.Column(db.String(), db.ForeignKey('artists.id'))
    start_time = db.Column(db.DateTime)

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


def create_app(app, config_mode=CONFIG_MODE):
    """Application-factory pattern"""
    app.config.from_object(config[config_mode])
    db.init_app(app)
    migrate.init_app(app, db)
    return app
