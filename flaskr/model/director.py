"""
Model for director table and helper table
for m-to-m relation with movie table
"""

from sqlalchemy.orm import validates
from flaskr.model.validators import Validators
from flaskr import db

# helper table for movie-director m-to-m relationship
movies_directors = db.Table("movies_directors",
                            db.Column("director_id", db.Integer,
                                      db.ForeignKey("director.id"), primary_key=True),
                            db.Column("movie_id", db.Integer,
                                      db.ForeignKey("movie.id"), primary_key=True))


# pylint: disable=R0201
# pylint: disable=unused-argument
class Director(db.Model):
    """
    Class describes director entity of database

    Methods
    -------
        validate_first_name(self, key, first_name): sqlalchemy validator for first name
        validate_last_name(self, key, last_name): sqlalchemy validator for last name
        validate_date_of_birth(self, key, date_of_birth): sqlalchemy validator
                                                                for date of birth
    Attributes
    ---------
        id: int index for record, autoincrement
        first_name: str must be between 2 and 100 characters
        last_name: str must be between 2 and 100 characters
        date_of_birth: str should be valid date
    """
    id = db.Column(db.Integer, db.Sequence("director_id_seq"), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)


    @validates('first_name')
    def validate_first_name(self, key, first_name) -> str:
        """Validator for first name"""
        if not Validators.validate_name(first_name):
            raise AssertionError("First name is not valid")
        return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name) -> str:
        """Validator for last name"""
        if not Validators.validate_name(last_name):
            raise AssertionError("Last name is not valid")
        return last_name

    @validates('date_of_birth')
    def validate_date_of_birth(self, key, date_of_birth) :
        """Validator for date of birth"""
        if not Validators.validate_date_of_birth(date_of_birth):
            raise AssertionError("Date of birth not valid date")
        return date_of_birth

    def __repr__(self):
        return f"Director(id={self.id!r}, first_name={self.first_name!r}, " \
               f"last_name={self.last_name!r}, date_of_birth={self.date_of_birth!r})"
