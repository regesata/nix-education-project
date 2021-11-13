from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import user


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = user.User
        include_relationships = True
        load_instance = True
