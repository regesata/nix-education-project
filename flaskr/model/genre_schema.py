"""Auto schema for model genre"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import genre


class GenreSchema(SQLAlchemyAutoSchema):
    """Auto schema class for model genre"""
    class Meta:
        """Meta class for auto schema"""
        model = genre.Genre
        include_relationships = True
        load_instance = True
