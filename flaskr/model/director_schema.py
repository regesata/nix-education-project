"""Module realize autoschema for model"""
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import director


class DirectorSchema(SQLAlchemyAutoSchema):
    """Autoschema for model"""
    class Meta:
        """Meta class for model"""
        model = director.Director
        include_relationships = True
        load_instance = True
