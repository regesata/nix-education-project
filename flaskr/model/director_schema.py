from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import director


class DirectorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = director.Director
        include_relationships = True
        load_instance = True
