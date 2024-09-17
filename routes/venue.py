import logging
from datetime import datetime
from typing import List

import ulid
from flask import render_template, Blueprint, request, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from form import VenueForm
from models import Artist, db, Show, Venue

venue_route = Blueprint('venues', __name__)


@venue_route.route('/venues', methods=['GET'])
def get_venues():
    venues = Venue.query.all()
    data = get_all_venues(venues)
    return render_template('pages/venues.html', areas=data)

@venue_route.route('/venues/create', methods=['GET'])
def create_venue_form():
    venue_form = VenueForm()
    return render_template('forms/new_venue.html', form=venue_form)

@venue_route.route('/venues/create', methods=['POST'])
def ceate_venue():
    new_venue = Venue()
    new_venue.id = ulid.ulid()
    new_venue.name = request.form.get('name')
    new_venue.state = request.form.get('state')
    new_venue.city = request.form.get('city')
    new_venue.genres = request.form.getlist('genres')
    new_venue.address = request.form.get('address')
    new_venue.phone = request.form.get('phone')
    new_venue.website = request.form.get('website')
    new_venue.facebook_link = request.form.get('facebook_link')
    new_venue.seeking_talent = bool(request.form.get('seeking_talent'))
    new_venue.seeking_description = request.form.get('seeking_description')
    new_venue.image_link = request.form.get('image_link')

    db.session.add(new_venue)
    db.session.commit()
    return redirect(url_for('venues.get_venues'))


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
    venue = Venue.query.filter(Venue.id == venue_id)[0]
    format_venue = get_vanue_by_id(venue_id, venue.toDict())
    return render_template('pages/show_venue.html', venue=format_venue)


@venue_route.route('/venues/<venue_id>/edit', methods=['POST'])
def update_venue_by_id(venue_id):
    try:
        update_venue = Venue.query.filter(Venue.id == venue_id)[0]
        update_venue.name = request.form.get('name')
        update_venue.state = request.form.get('state')
        update_venue.city = request.form.get('city')
        update_venue.genres = request.form.getlist('genres')
        update_venue.address = request.form.get('address')
        update_venue.phone = request.form.get('phone')
        update_venue.website = request.form.get('website')
        update_venue.facebook_link = request.form.get('facebook_link')
        update_venue.seeking_talent = bool(request.form.get('seeking_talent'))
        update_venue.seeking_description = request.form.get('seeking_description')
        update_venue.image_link = request.form.get('image_link')

        db.session.commit()

        return redirect(url_for('venues.show_venue', venue_id=venue_id))
    except SQLAlchemyError as er:
        logging.info(f'Update venue fail: {er}')
        db.session.rollback()

@venue_route.route('/venues/<venue_id>/edit', methods=['GET'])
def get_edit_venue_form(venue_id):
    venue_form = VenueForm()
    venue = Venue.query.filter(Venue.id == venue_id)[0]
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
        shows = Show.query.filter(Show.venue_id == venue.id)
        short_data = {
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': len(list(shows))
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


def get_vanue_by_id(venue_id, venue: dict):
    past_shows = []
    upcoming_shows = []
    # Get all shows
    all_shows = Show.query.filter(Show.venue_id == venue_id)
    if all_shows:
        for show in all_shows:
            # Get artist information
            artist = Artist.query.filter(Artist.id == show.artist_id)[0]
            show_detail = {
                'artist_id': artist.id,
                'artist_name': artist.name,
                'artist_image_link': artist.image_link,
                'start_time': show.start_time
            }
            if show.start_time > datetime.today():
                upcoming_shows.append(show_detail)
            else:
                past_shows.append(show_detail)

    return {
        **venue,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }
