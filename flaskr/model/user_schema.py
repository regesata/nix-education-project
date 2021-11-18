from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import fields
from .movie_schema import MovieSchema
from . import user


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = user.User
        include_relationships = True
        load_instance = True
    movies = fields.Nested(MovieSchema, many=True)
