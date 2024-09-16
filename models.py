from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()
migrate = Migrate()


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genres = db.Column(db.ARRAY(db.String()))
    city = db.Column(db.String())
    state = db.Column(db.String())
    phone = db.Column(db.String())
    website = db.Column(db.String())
    facebook_link = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    image_link = db.Column(db.String())

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genres = db.Column(db.ARRAY(db.String()))
    city = db.Column(db.String())
    state = db.Column(db.String())
    phone = db.Column(db.String())
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String())

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
