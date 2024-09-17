import logging
from datetime import datetime

import ulid
from flask import render_template, Blueprint, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from form import ArtistForm
from models import Artist, db, Show, Venue

artist_route = Blueprint('artists', __name__)


@artist_route.route('/artists', methods=['GET'])
def get_artists():
    artists = Artist.query.all()
    data = [artist.toDict() for artist in artists]
    return render_template('pages/artists.html', artists=data)


@artist_route.route('/artists/create', methods=['GET'])
def create_artist_form():
    artist_form = ArtistForm()
    artist = Artist()
    return render_template('forms/new_artist.html', form=artist_form, artist=artist)


@artist_route.route('/artists/create', methods=['POST'])
def create_artist():
    try:
        artist = Artist()
        artist.id = ulid.ulid()
        artist.name = request.form.get('name', '')
        artist.genres = request.form.getlist('genres')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.website = request.form.get('website')
        artist.facebook_link = request.form.get('facebook_link')
        artist.seeking_venue = request.form.get('seeking_venue')
        artist.seeking_description = request.form.get('seeking_description')
        artist.image_link = request.form.get('image_link')

        db.session.add(artist)
        db.session.commit()

        return redirect(url_for('artists.get_artists'))
    except SQLAlchemyError as er:
        logging.info(f'Create artist fail: {er}')
        db.session.rollback()


@artist_route.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term')
    searched_artists = Artist.query.filter(Artist.name.contains(search_term))
    result = {
        'data': searched_artists,
        'count': len(list(searched_artists))
    }
    return render_template('pages/search_artists.html', results=result, search_term=search_term)


@artist_route.route('/artists/<artist_id>', methods=['GET'])
def show_artist(artist_id):
    artist = list(Artist.query.filter(Artist.id == artist_id))[0]
    artist_detail = get_artist_detail(artist)
    return render_template('pages/show_artist.html', artist=artist_detail)


@artist_route.route('/artists/<artist_id>/edit', methods=['POST'])
def update_artist(artist_id):
    try:
        artist = list(Artist.query.filter(Artist.id == artist_id))[0]

        artist.name = request.form.get('name', '')
        artist.genres = request.form.getlist('genres')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.website = request.form.get('website')
        artist.facebook_link = request.form.get('facebook_link')
        artist.seeking_venue = request.form.get('seeking_venue')
        artist.seeking_description = request.form.get('seeking_description')
        artist.image_link = request.form.get('image_link')

        db.session.add(artist)
        db.session.commit()
        return redirect(url_for('artists.show_artist', artist_id=artist_id))
    except SQLAlchemyError as er:
        logging.info(f'Update artist fail: {er}')
        db.session.rollback()


@artist_route.route('/artists/<artist_id>/edit', methods=['GET'])
def edit_artist_form(artist_id):
    artist_form = ArtistForm()
    artist = list(Artist.query.filter(Artist.id == artist_id))[0]
    return render_template('forms/edit_artist.html',
                           form=artist_form, artist=artist)


@artist_route.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        artist = list(Artist.query.filter(Artist.id == artist_id))[0]
        db.session.delete(artist)
        db.session.commit()
    except SQLAlchemyError as er:
        logging.info(f'Delete artist fail: {er}')
        db.session.rollback()


def get_artist_detail(artist):
    past_shows = []
    upcoming_shows = []

    # Get all shows of the artists
    shows = Show.query.filter(Show.artist_id == artist.id)
    if shows:
        for show in shows:
            # Get the venue that orgnize the show
            venue = Venue.query.filter(Venue.id == show.id)[0]
            show_detail = {
                'venue_id': venue.id,
                'venue_name': venue.name,
                'venue_image_link': venue.image_link,
                'start_time': show.start_time
            }
            if show.start_time > datetime.today():
                upcoming_shows.append(show_detail)
            else:
                past_shows.append(show_detail)

    return {
        **artist.toDict(),
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }
