from flask import render_template, Blueprint, request

api = Blueprint('/', __name__)


@api.route('/', methods=['GET'])
def welcome():
    return render_template('pages/home.html', request=request)
