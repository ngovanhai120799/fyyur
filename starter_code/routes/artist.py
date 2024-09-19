import logging
from datetime import datetime

import ulid
from flask import render_template, Blueprint, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from starter_code.form import ArtistForm
from starter_code.models import Artist, db, Show, Venue

artist_route = Blueprint('artists', __name__)


@artist_route.route('/artists', methods=['GET'])
def get_artists():
    artists = Artist.query.all()
    return render_template('pages/artists.html', artists=artists)


@artist_route.route('/artists/create', methods=['GET'])
def create_artist_form():
    artist_form = ArtistForm(request.form, meta= {'csrf': False})
    artist = Artist()
    return render_template('forms/new_artist.html', form=artist_form, artist=artist)


@artist_route.route('/artists/create', methods=['POST'])
def create_artist():
    artist_form = ArtistForm(request.form, meta= {'csrf': False})
    if artist_form.validate():
        try:
            artist = Artist()
            artist.id = ulid.ulid()
            artist.name = artist_form.name.data
            artist.genres = artist_form.genres.data
            artist.city = artist_form.city.data
            artist.state = artist_form.state.data
            artist.phone = artist_form.phone.data
            artist.website = artist_form.website_link.data
            artist.facebook_link = artist_form.facebook_link.data
            artist.seeking_venue = artist_form.seeking_venue.data
            artist.seeking_description = artist_form.seeking_description.data
            artist.image_link = artist_form.image_link.data

            db.session.add(artist)
            db.session.commit()

            return redirect(url_for('artists.get_artists'))
        except SQLAlchemyError as er:
            logging.info(f'Create artist fail: {er}')
            db.session.rollback()
    else:
        return render_template('forms/new_artist.html', form=artist_form)


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
    artist = Artist.query.get_or_404(artist_id)
    artist_detail = get_artist_detail(artist)
    return render_template('pages/show_artist.html', artist=artist_detail)


@artist_route.route('/artists/<artist_id>/edit', methods=['POST'])
def update_artist(artist_id):
    artist_form = ArtistForm(request.form, meta= {'csrf': False})
    if artist_form.validate():
        try:
            artist = Artist.query.get_or_404(artist_id)

            artist.name = artist_form.name.data
            artist.genres = artist_form.genres.data
            artist.city = artist_form.city.data
            artist.state = artist_form.state.data
            artist.phone = artist_form.phone.data
            artist.website = artist_form.website_link.data
            artist.facebook_link = artist_form.facebook_link.data
            artist.seeking_venue = artist_form.seeking_venue.data
            artist.seeking_description = artist_form.seeking_description.data
            artist.image_link = artist_form.image_link.data

            db.session.commit()
            return redirect(url_for('artists.show_artist', artist_id=artist_id))
        except SQLAlchemyError as er:
            logging.info(f'Update artist fail: {er}')
            db.session.rollback()
    else:
        return render_template('forms/edit_artist.html', form=artist_form)


@artist_route.route('/artists/<artist_id>/edit', methods=['GET'])
def edit_artist_form(artist_id):
    artist_form = ArtistForm(request.form, meta= {'csrf': False})
    artist = Artist.query.get_or_404(artist_id)
    return render_template('forms/edit_artist.html',
                           form=artist_form, artist=artist)


@artist_route.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        artist = Artist.query.get_or_404(artist_id)
        db.session.delete(artist)
        db.session.commit()
    except SQLAlchemyError as er:
        logging.info(f'Delete artist fail: {er}')
        db.session.rollback()


def get_artist_detail(artist: Artist):
    past_shows = []
    upcoming_shows = []

    for show in artist.shows:
        # Get the venue that orgnize the show
        show_detail = {
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.start_time.strftime('%m%d%y, %H:%M')
        }
        if show.start_time > datetime.now():
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
