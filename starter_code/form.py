import re
from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, ValidationError
from wtforms.validators import DataRequired, URL

from starter_code.choices import State, Genres

class BaseForm(Form):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()],choices=State.choices())
    phone = StringField('phone', validators=[DataRequired()])
    image_link = StringField('image_link')
    genres = SelectMultipleField('genres', validators=[DataRequired()], choices=Genres.choices())
    facebook_link = StringField('facebook_link', validators=[URL()])
    website_link = StringField('website_link', validators=[URL()])
    seeking_description = StringField('seeking_description')

    def _is_valid_phone(self, phone: str):
        regex = r'^\(?([0-9]{3})\)?([ .-]?)([0-9]{3})[ .-]?([0-9]{4})'
        return re.match(regex, phone)

    def validate_phone(self, field):
        if not self._is_valid_phone(field.data):
            raise ValidationError('Invalid phone')

    def validate_genres(self, field):
        if not set(field.data).issubset(dict(Genres.choices()).keys()):
            raise ValidationError('Invalid genres')

    def validate_state(self, field):
        if field.data not in dict(State.choices()).keys():
            raise ValidationError('Invalid state')

class VenueForm(BaseForm):
    address = StringField('address', validators=[DataRequired()])
    seeking_talent = BooleanField('seeking_talent')
    def validate(self, **kwargs):
        return super(VenueForm, self).validate(**kwargs)


class ArtistForm(BaseForm):
    seeking_venue = BooleanField('seeking_venue')
    def validate(self, **kwargs):
        return super(ArtistForm, self).validate(**kwargs)

class ShowForm(Form):
    artist_id = StringField('artist_id')
    venue_id = StringField('venue_id')
    start_time = DateTimeField('start_time', validators=[DataRequired()], default=datetime.today())