"""Auto schema for movie model"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import fields
from .genre_schema import GenreSchema
from .director_schema import DirectorSchema
from . import movie


class MovieSchema(SQLAlchemyAutoSchema):
    """Auto schema class"""
    class Meta:
        """Meta class for auto schema"""
        model = movie.Movie
        include_relationship = True
        include_fk = True
        load_instance = True
    genre = fields.Nested(GenreSchema, many=True)
    director = fields.Nested(DirectorSchema, many=True)
