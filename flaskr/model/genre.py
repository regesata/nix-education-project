"""
Model for genre table and helper table movie-genre
for relation m-to-m for movie table
"""
from flaskr import db

movies_genre = db.Table("movies_genre",
                        db.Column("genre_id", db.Integer,
                                  db.ForeignKey("genre.id"), primary_key=True),
                        db.Column("movie_id", db.Integer,
                                  db.ForeignKey("movie.id"), primary_key=True))


class Genre(db.Model):
    """Class describes genre entity"""
    id = db.Column(db.Integer, db.Sequence("genre_id_seq"), primary_key=True)
    title = db.Column(db.String, nullable=False)
    movie = db.relationship("Movie", secondary=movies_genre, backref="genre")

    def __repr__(self):
        return f"Genre(id={self.id}, title={self.title}"