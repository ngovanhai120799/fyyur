import ulid
import json
from datetime import datetime

from flask import Blueprint, request, render_template
from sqlalchemy.exc import SQLAlchemyError

from models import Venue, db, Show, Artist

api = Blueprint('api', __name__)


@api.route('/')
def welcome():
    return render_template('pages/home.html')


@api.route('/venues', methods=['GET'])
def get_venue():
    data = get_all_venues()
    return render_template('pages/venues.html', areas=json.loads(data))


@api.route('/venues', methods=['POST'])
def ceate_venue():
    new_venue = Venue()
    new_venue.id = ulid.ulid()
    new_venue.name = request.form.get('name')
    new_venue.state = request.form.get('state')
    new_venue.city = request.form.get('city')
    new_venue.genres = request.form.get('genres')
    new_venue.address = request.form.get('address')
    new_venue.phone = request.form.get('phone')
    new_venue.website = request.form.get('website')
    new_venue.facebook_link = request.form.get('facebook_link')
    new_venue.seeking_talent = bool(request.form.get('seeking_talent'))
    new_venue.seeking_description = request.form.get('seeking_description')
    new_venue.image_link = request.form.get('image_link')

    db.session.add(new_venue)
    db.session.commit()
    return json.dumps(new_venue.toDict())


@api.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    searched_vanue = Venue.query.filter(Venue.name.contains(search_term))
    return render_template('pages/search_venues.html', results=list(searched_vanue),
                           search_term=search_term)


@api.route('/venues/venue_id/<venue_id>', methods=['GET'])
def show_venue(venue_id):
    venue = Venue.query.filter(Venue.id == venue_id)[0]
    format_venue = get_vanue_by_id(venue_id, venue)
    return render_template('pages/show_venue.html', venue=format_venue)


@api.route('/venues/venue_id/<venue_id>', methods=['PUT'])
def update_venue_by_id(venue_id):
    update_venue = Venue.query.filter(Venue.id == venue_id)[0]
    update_venue.name = request.form.get('name')
    update_venue.state = request.form.get('state')
    update_venue.city = request.form.get('city')
    update_venue.genres = request.form.get('genres')
    update_venue.address = request.form.get('address')
    update_venue.phone = request.form.get('phone')
    update_venue.website = request.form.get('website')
    update_venue.facebook_link = request.form.get('facebook_link')
    update_venue.seeking_talent = bool(request.form.get('seeking_talent'))
    update_venue.seeking_description = request.form.get('seeking_description')
    update_venue.image_link = request.form.get('image_link')

    db.session.add(update_venue)
    db.session.commit()

    format_venue = get_vanue_by_id(venue_id, update_venue)
    return render_template('pages/show_venue.html', venue=format_venue)


@api.route('/venues/venue_id/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        db.session.delete(venue_id)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()


def get_all_venues():
    data = []
    venues = Venue.query.all()
    for venue in venues:
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
                    item['venues'] = [*item['venues'], short_data]
                    continue
                else:
                    data.append(show_item)
    return json.dumps(data)


def get_vanue_by_id(venue_id, venue):
    past_shows = []
    upcoming_shows = []
    # Get all shows
    all_shows = Show.query.filter(Show.venue_id == venue_id)
    all_shows = list(all_shows)
    if all_shows:
        for show in all_shows:
            # Get artist information
            artist = Artist.query.filter(Artist.id == show.artist_id)
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
        **venue.toDict(),
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }
