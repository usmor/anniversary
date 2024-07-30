from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.main_routes import main_routes as main_routes_blueprint
    from app.routes.person_routes import person_routes as person_routes_blueprint
    app.register_blueprint(main_routes_blueprint)
    app.register_blueprint(person_routes_blueprint)

    from app.models.models import StatusList

    with app.app_context():
        db.create_all()
        db.session.commit()

        if StatusList.query.first() is None:
            statuses = [
                'Бакалавр',
                'Магистрант',
                'Аспирант',
                'Преподаватель',
                'Менеджер',
                'Лаборант']
            for stat in statuses:
                new_status = StatusList(status=stat)
                db.session.add(new_status)
            db.session.commit()

    return app
