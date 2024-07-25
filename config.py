import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'ANNIVERSARY_DATABASE_URL') or 'sqlite:///smoltest_3.db'
    UPLOAD_FOLDER = 'uploads'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
