from typing import List

import ulid
from flask import render_template, Blueprint, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from starter_code.form import ShowForm
from starter_code.models import Artist, db, Show, Venue

show_route = Blueprint('shows', __name__)


@show_route.route('/shows', methods=['GET'])
def get_shows():
    shows = Show.query.all()
    data = get_show_detail(shows)
    return render_template('pages/shows.html', shows=data)

@show_route.route('/shows/create', methods=['GET'])
def get_show_form():
    show_form = ShowForm()
    return render_template('forms/new_show.html', form=show_form)

@show_route.route('/shows/create', methods=['POST'])
def create_show():
    try:
        show = Show()
        show.id = ulid.ulid()
        show.artist_id = request.form.get('artist_id')
        show.venue_id = request.form.get('venue_id')
        show.start_time = request.form.get('start_time')

        db.session.add(show)
        db.session.commit()
        return redirect(url_for('shows.get_shows'))
    except SQLAlchemyError as err:
        db.session.rollback()

def get_show_detail(shows: List[Show]):
    data: List[dict] = []
    for show in shows:
        venue = Venue.query.filter(Venue.id == show.venue_id)[0]
        artist = Artist.query.filter(Artist.id == show.artist_id)[0]
        show_detail = {
            'venue_id': venue.id,
            'venue_name': venue.name,
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time
        }
        data.append(show_detail)
    return data