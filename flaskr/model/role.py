"""Model for role table"""
from flaskr import db
from sqlalchemy.orm import validates
from flaskr.model.validators import Validators


# pylint: disable=R0201
# pylint: disable=unused-argument
class Role(db.Model):
    """
    Class describes role entity
    Attributes
    ---------
        id: int id for record in table, autoincrement
        title: str Role title. Table has Admin(id=1) and User(id=2) roles by default
        description: str Description for role. Can be empty
    """
    id = db.Column(db.Integer, db.Sequence("role_id_seq"), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user = db.relationship("User", backref="role", lazy=True)

    def __repr__(self):
        return f"Role(id={self.id!r}, title={self.title!r}, description={self.description!r})"


    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise AssertionError("Title not provided")
        if not Validators.validate_name(title):
            raise AssertionError("Title is not valid")
        return title
