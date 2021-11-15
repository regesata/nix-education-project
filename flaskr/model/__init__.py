"""
Initializing of flask app and db connection
"""
from flask_sqlalchemy import SQLAlchemy
from flaskr import app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///model.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)




from flaskr.model import director
from flaskr.model import genre
from flaskr.model import movie
from flaskr.model import role
from flaskr.model import user
db.create_all()
db.session.commit()


