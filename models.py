from app import db


# MODELS Section
class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.String(), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=True)
    state = db.Column(db.String(), nullable=True)
    genres = db.Column(db.String(120))
    seeking_talent = db.Column(db.boolean)
    image_link = db.Column(db.String(120))
    past_shows = db.Column(db.String(120))
    upcoming_shows = db.Column(db.String(120))
    past_shows_count = db.Column(db.String(120))


class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.String(), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
