from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import genre


class GenreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = genre.Genre
        include_relationships = True
        load_instance = True
