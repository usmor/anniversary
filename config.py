import os


class Config:
    SECRET_KEY = os.environ.get('ANNIVERSARY_SECRET_KEY') or os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'ANNIVERSARY_DATABASE_URL') or 'sqlite:///anniversary.db'
    UPLOAD_FOLDER = 'instance/uploads'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


HOST = os.environ.get('ANNIVERSARY_HOST') or '0.0.0.0'
PORT = os.environ.get('ANNIVERSARY_PORT') or 5001
