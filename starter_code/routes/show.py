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
    show_form = ShowForm(request.form, meta= {'csrf': False})
    return render_template('forms/new_show.html', form=show_form)

@show_route.route('/shows/create', methods=['POST'])
def create_show():
    show_form = ShowForm(request.form, meta= {'csrf': False})
    if show_form.validate():
        try:
            show = Show()
            show.id = ulid.ulid()
            show.artist_id = show_form.artist_id.data
            show.venue_id = show_form.venue_id.data
            show.start_time = show_form.start_time.data

            db.session.add(show)
            db.session.commit()
            return redirect(url_for('shows.get_shows'))
        except SQLAlchemyError as err:
            db.session.rollback()
    else:
        return render_template('forms/new_show.html', form=show_form)

def get_show_detail(shows: List[Show]):
    data: List[dict] = []
    for show in shows:
        show_detail = {
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time
        }
        data.append(show_detail)
    return data