"""Marshmallow.SQLAlchemyAutoSchema for role table"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flaskr.model import role


class RoleSchema(SQLAlchemyAutoSchema):
    """Auto schema class"""
    class Meta:
        """Class meta for auto schema"""
        model = role.Role
        include_relationships = True
        load_instance = True
