from flask import Blueprint, render_template, redirect, url_for, request


main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/')
def main():
    return render_template('main.html')


@main_routes.route('/contacts')
def contacts():
    return render_template('contacts.html')
