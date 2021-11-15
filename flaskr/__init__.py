"""
Initializing of flask app and db connection
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///model.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)
from flaskr.model import director
from flaskr.model import genre
from flaskr.model import movies
from flaskr.model import role
from flaskr.model import user
db.create_all()
db.session.commit()