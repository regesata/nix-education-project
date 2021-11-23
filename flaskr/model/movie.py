"""Model for movie table"""
import datetime

from sqlalchemy.orm import validates
from flaskr.model.validators import Validators
from flaskr import db
from .genre import movies_genre
from .director import movies_directors


# pylint: disable=R0201
# pylint: disable=unused-argument
class Movie(db.Model):
    """
    Class describes movie entity

    Methods
    -------
        validate_title(self, key, title: str) -> str: sqlalchemy validator for title
        validate_release_date(self, key, release_date: date) -> date: sqlalchemy validator
                                                                      for first name
        validate_genre(self, key, genre: str) -> str: sqlalchemy validator for genre
        validate_rate(self, key, rate: int) -> int: sqlalchemy validator for genre

    Attributes
    ----------
        id: int index for record in table, autoincrement
        title: str Title must be between 2 and 100 characters
        release_data: date Should be between 1800-01-01 and today
        director : list Relation with Director entity. Can be multiply
        description: str Description text for movie
        rate: int Rate of movie. Must be between 1 and 10.
        poster: str Link to poster image in internet
        user_id: int Id of user who added this record


    """
    id = db.Column(db.Integer, db.Sequence("movie_id_seq"), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.relationship("Genre", secondary=movies_genre, backref="genre")
    release_date = db.Column(db.Date, nullable=False)
    director = db.relationship("Director", secondary=movies_directors, backref="movie")
    description = db.Column(db.Text)
    rate = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    @validates('title')
    def validate_title(self, key, title: str) -> str:
        """Validator for title"""
        if not Validators.validate_name(title):
            raise AssertionError("Title is not valid")
        return title

    @validates('genre')
    def validate_genre(self, key, genre: str) -> str:
        """
        Validate genre
        :raise Assertion error
        """
        if not genre:
            raise AssertionError("Genre id not provided")
        return genre

    @validates('release_date')
    def validate_release_date(self, key, release_date: datetime.date) -> datetime.date:
        """
        Validate release date
        :raise Assertion error
        """
        if not Validators.validate_date_of_birth(release_date):
            raise AssertionError("Release date is not valid")
        return release_date

    @validates('rate')
    def validate_rate(self, key, rate: int) -> int:
        """
        Validate rate. Rate must be between 1 and 10
        :raise Assertion error
        """
        if not Validators.validate_rate(rate):
            raise AssertionError("Rate is not valid")
        return rate

    def __repr__(self):
        return f"Movie(id={self.id!r}, title={self.title!r}, release_date={self.release_date!r}, " \
               f"description={self.description}, poster={self.poster!r}, user_id={self.user_id!r})"
