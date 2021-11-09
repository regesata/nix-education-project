"""
Initializing of flask app and db connection
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///model.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)



from flaskr.model import user
#db.create_all()