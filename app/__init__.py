from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.person_routes import person_routes as person_routes_blueprint
    app.register_blueprint(person_routes_blueprint)

    with app.app_context():
        db.create_all()
        db.session.commit()

    return app
