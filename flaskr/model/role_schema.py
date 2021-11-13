"""Marshmallow.SQLAlchemyAutoSchema for role table"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import role


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = role.Role
        include_relationships = True
        load_instance = True
