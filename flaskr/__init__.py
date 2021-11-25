"""
Initializing of flask app and db connection
"""
from flask import Flask
from flaskr.utils import get_logger_fact, LOGGER_NAME
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager

log = get_logger_fact(LOGGER_NAME)

db = SQLAlchemy()
log_manager = LoginManager()
migrate = Migrate()


def create_app(conf_obj):
    app = Flask(__name__)
    app.config.from_object(conf_obj)
    db.init_app(app)
    log_manager.init_app(app)
    migrate.init_app(app, db)

    log.info("Application started")
    return app






