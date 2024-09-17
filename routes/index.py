from flask import render_template, Blueprint, request


home_route = Blueprint('home', __name__)

@home_route.route('/', methods=['GET'])
def welcome():
    return render_template('pages/home.html')

@home_route.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@home_route.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500