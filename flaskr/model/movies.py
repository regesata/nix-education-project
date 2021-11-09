"""Model for movie table"""

from . import db
class Movie(db.Model):
    """Class describes movie entity"""
    id = db.Column(db.Integer, db.Sequence("movie_id_seq"), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    poster = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    def __repr__(self):
        return f"Movie(id={self.id!r}, title={self.title!r}, release_year={self.release_year!r}, " \
               f"description={self.description}, poster={self.poster!r}, user_id={self.user_id!r})"
