import logging
from datetime import datetime
from typing import List

import ulid
from flask import render_template, Blueprint, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from starter_code.form import VenueForm, ArtistForm
from starter_code.models import Artist, db, Show, Venue

venue_route = Blueprint('venues', __name__)


@venue_route.route('/venues', methods=['GET'])
def get_venues():
    venues = Venue.query.all()
    data = get_all_venues(venues)
    return render_template('pages/venues.html', areas=data)

@venue_route.route('/venues/create', methods=['GET'])
def create_venue_form():
    venue_form = VenueForm(request.form, meta= {'csrf': False})
    return render_template('forms/new_venue.html', form=venue_form)

@venue_route.route('/venues/create', methods=['POST'])
def ceate_venue():
    venue_form = VenueForm(request.form, meta= {'csrf': False})
    if venue_form.validate():
        try:
            new_venue = Venue()
            new_venue.id = ulid.ulid()
            new_venue.name = venue_form.name.data
            new_venue.state = venue_form.state.data
            new_venue.city = venue_form.city.data
            new_venue.genres = venue_form.genres.data
            new_venue.address = venue_form.address.data
            new_venue.phone = venue_form.phone.data
            new_venue.website = venue_form.website_link.data
            new_venue.facebook_link = venue_form.facebook_link.data
            new_venue.seeking_talent = venue_form.seeking_talent.data
            new_venue.seeking_description = venue_form.seeking_description.data
            new_venue.image_link = venue_form.image_link.data

            db.session.add(new_venue)
            db.session.commit()
            return redirect(url_for('venues.get_venues'))
        except SQLAlchemyError as err:
            db.session.rollback()
    else:
        return render_template('forms/new_venue.html', form=venue_form)


@venue_route.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    searched_vanues = Venue.query.filter(Venue.name.contains(search_term))
    result = {
        'data': searched_vanues,
        'count': len(list(searched_vanues))
    }
    return render_template('pages/search_venues.html', results=result, search_term=search_term)


@venue_route.route('/venues/<venue_id>', methods=['GET'])
def show_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    format_venue = get_venue_by_id(venue)
    return render_template('pages/show_venue.html', venue=format_venue)


@venue_route.route('/venues/<venue_id>/edit', methods=['POST'])
def update_venue_by_id(venue_id):
    venue_form = VenueForm(request.form, meta= {'csrf': False})
    if venue_form.validate():
        try:
            update_venue = Venue.query.get(venue_id)
            update_venue.name = venue_form.name.data
            update_venue.state = venue_form.state.data
            update_venue.city = venue_form.city.data
            update_venue.genres = venue_form.genres.data
            update_venue.address = venue_form.address.data
            update_venue.phone = venue_form.phone.data
            update_venue.website = venue_form.website_link.data
            update_venue.facebook_link = venue_form.facebook_link.data
            update_venue.seeking_talent = venue_form.seeking_talent.data
            update_venue.seeking_description = venue_form.seeking_description.data
            update_venue.image_link = venue_form.image_link.data

            db.session.commit()
            return redirect(url_for('venues.show_venue', venue_id=venue_id))
        except SQLAlchemyError as er:
            logging.info(f'Update venue fail: {er}')
            db.session.rollback()
    else:
        return render_template('forms/edit_venue.html', form=venue_form)


@venue_route.route('/venues/<venue_id>/edit', methods=['GET'])
def get_edit_venue_form(venue_id):
    venue_form = VenueForm(request.form, meta= {'csrf': False})
    venue = Venue.query.get_or_404(venue_id)
    return render_template('forms/edit_venue.html', form=venue_form, venue=venue)

@venue_route.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.filter(Venue.id == venue_id)[0]
        db.session.delete(venue)
        db.session.commit()
        return "OK"
    except SQLAlchemyError as er:
        logging.info(f'Delete artist fail: {er}')
        db.session.rollback()


def get_all_venues(venues: List[Venue]):
    data: List[dict] = []
    for venue in venues:
        flag: bool = False
        short_data = {
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': len(list(venue.shows))
        }
        show_item = {
            'city': venue.city,
            'state': venue.state,
            'venues': [short_data]
        }
        if not data:
            data.append(show_item)
            continue

        for item in data:
            if venue.state == item['state']:
                if venue.city == item['city']:
                    flag = True
                    item['venues'] = [*item['venues'], short_data]

        if not flag:
            data.append(show_item)


    return data

def get_venue_by_id(venue: Venue):
    past_shows = []
    upcoming_shows = []
    # Get all shows
    for show in venue.shows:
        temp_show = {
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime('%m%d%Y, %H:%M')
        }
        if show.start_time > datetime.now():
            upcoming_shows.append(temp_show)
        else:
            past_shows.append(temp_show)

    return {
        **venue.toDict(),
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }
