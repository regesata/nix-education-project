"""Model for user table """
from flask_login import UserMixin
from sqlalchemy.orm import validates
from flaskr import db, log_manager
from flaskr.model.validators import Validators


# pylint: disable=R0201
# pylint: disable=unused-argument
class User(UserMixin, db.Model):
    """
    Class describes user entity
    Methods
    -------
    validate_email(self, key, email) -> str: sqlalchemy validator for email

    Attributes
    ----------
    id: int index for record, autoincrement
    first_name: str must be between 2 and 100 characters
    last_name: str must be between 1 and 100 character
    email: str must be valid email (example@example.com)
    password: str with hashed password
    role_id: int index of user role
    created_at: datetime date and time of creation a record
    """
    id = db.Column(db.Integer, db.Sequence("user_id_seq"), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    created_at = db.Column(db.DateTime)
    movies = db.relationship("Movie", backref="user", lazy=True)


    @validates('email')
    def validate_email(self, key, email) -> str:
        """
        Validator for email
        :raise AssertionError
        """
        if not Validators.validate_email(email):
            raise AssertionError("Email not valid")
        return email

    def __repr__(self):
        return f"User(id={self.id!r}, first_name={self.first_name}," \
               f" last_name={self.last_name}," \
               f" email={self.email}, password={self.password}," \
               f" role_id={self.role_id}, created_at={self.created_at})"


@log_manager.user_loader
def load_user(user_id):
    """Function for flask-login"""
    return User.query.get(user_id)
