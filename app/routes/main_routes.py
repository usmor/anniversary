from flask import Blueprint, render_template
from app.models.models import StatusList
from app import db

main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/')
def main():
    if StatusList.query.first() is None:
        statuses = ['Бакалавр', 'Магистрант', 'Аспирант', 'Преподаватель', 'Менеджер', 'Лаборант']
        for stat in statuses:
            new_status = StatusList(status=stat)
            db.session.add(new_status)
        db.session.commit()
    return render_template('main.html')


@main_routes.route('/contacts')
def contacts():
    return render_template('contacts.html')
