"""Model for movie table"""

from flaskr import db
from .genre import movies_genre
from .director import movies_directors



class Movie(db.Model):
    """Class describes movie entity"""
    id = db.Column(db.Integer, db.Sequence("movie_id_seq"), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.relationship("Genre", secondary=movies_genre, backref="genre")
    release_date = db.Column(db.Date)
    director = db.relationship("Director", secondary=movies_directors, backref="movie")
    description = db.Column(db.Text)
    rate = db.Column(db.Integer)
    poster = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    def __repr__(self):
        return f"Movie(id={self.id!r}, title={self.title!r}, release_year={self.release_year!r}, " \
               f"description={self.description}, poster={self.poster!r}, user_id={self.user_id!r})"
