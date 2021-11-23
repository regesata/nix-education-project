"""
Model for genre table and helper table movie-genre
for relation m-to-m for movie table
"""
from sqlalchemy.orm import validates
from flaskr import db
from flaskr.model.validators import Validators

movies_genre = db.Table("movies_genre",
                        db.Column("genre_id", db.Integer,
                                  db.ForeignKey("genre.id"), primary_key=True),
                        db.Column("movie_id", db.Integer,
                                  db.ForeignKey("movie.id"), primary_key=True))


# pylint: disable=R0201
# pylint: disable=unused-argument
class Genre(db.Model):
    """
    Class describes genre entity
    Methods
    -------
        validate_title(self, key, title): str sqlalchemy validator for title

    Attributes
    ---------
        id: int index for record, autoincrement
        title: str must be between 2 and 100 characters
    """
    id = db.Column(db.Integer, db.Sequence("genre_id_seq"), primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    @validates('title')
    def validate_title(self, key, title) -> str:
        """Validator for title"""
        if not Validators.validate_name(title):
            raise AssertionError("Title is not valid")
        return title

    def __repr__(self):
        return f"Genre(id={self.id}, title={self.title})"
