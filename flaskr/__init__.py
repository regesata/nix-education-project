"""
Initializing of flask app and db connection
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///model.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "too secret"
db = SQLAlchemy(app)
log_manager = LoginManager()
log_manager.init_app(app)

from flaskr.model import director
from flaskr.model import genre
from flaskr.model import role
from flaskr.model import user
from flaskr.model import movie


@log_manager.user_loader
def load_user(user_id):
    return user.User.query.get(user_id)


db.create_all()
db.session.commit()
migrate = Migrate()
migrate.init_app(app, db)
