import os
import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from app import create_app


load_dotenv()


def setup_logging(app):
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/' + app.config['LOG_FILE'],
            maxBytes=10240,
            backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Anniversary startup')


app = create_app()
setup_logging(app)

if __name__ == "__main__":
    app.run()
