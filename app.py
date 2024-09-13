import json
import ulid

from flask import Flask, request, jsonify
from models import (
    db,
    create_app,
    Venue,
    Genre
)

app = Flask(__name__)
create_app(app)


# Controllers
@app.route('/venues', methods=['GET'])
def get_all_venues():
    venues = Venue.query.all()
    return json.dumps(venues)


@app.route('/venues', methods=['POST'])
def create_new_venue():
    venue = Venue()
    body = request.get_json()

    venue.id = ulid.ulid()
    venue.name = body.get('name')
    db.session.add(venue)
    db.session.commit()
    return json.dumps(venue)


@app.route('/genres', methods=['POST'])
def create_genre():
    data = request.get_json()
    new_genre = Genre(id=ulid.ulid(), name=data['name'])
    db.session.add(new_genre)
    db.session.commit()
    return jsonify(new_genre)


@app.route('/', methods=['POST'])
def _import_genres_from_file():
    genres = Genre.query.all()
    if not genres:
        # Check local db have data or not
        f = open('./resources/genres.json')
        data = json.load(f)
        for item in data:
            new_genre = Genre(id=item['id'], name=item['name'])
            db.session.add(new_genre)
            db.session.commit()
        f.close()
    else:
        response = [genre.toDict() for genre in genres]
        return jsonify(response)


if __name__ == '__main__':
    app.run()
