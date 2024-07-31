from flask import Blueprint, render_template


main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/')
def main():
    return render_template('main.html')


@main_routes.route('/contacts')
def contacts():
    return render_template('contacts.html')


@main_routes.route('/emotion')
def emotion():
    return render_template('emotion.html')