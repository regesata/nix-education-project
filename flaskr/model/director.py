"""
Model for director table and helper table
for m-to-m relation with movie table
"""
from flaskr import db
# helper table for movie-director m-to-m relationship
movies_directors = db.Table("movies_directors",
                            db.Column("director_id", db.Integer,
                                      db.ForeignKey("director.id"), primary_key=True),
                            db.Column("movie_id", db.Integer,
                                      db.ForeignKey("movie.id"), primary_key=True))


class Director(db.Model):
    """Class describes director entity of database"""
    id = db.Column(db.Integer, db.Sequence("director_id_seq"), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date)

    def __repr__(self):
        return f"Director(id={self.id!r}, first_name={self.first_name!r}, " \
               f"last_name={self.last_name!r}, date_of_birth={self.date_of_birth!r})"