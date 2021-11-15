"""Model for user table """
from flaskr import db


class User(db.Model):
    """Class describes user entity"""
    id = db.Column(db.Integer, db.Sequence("user_id_seq"), primary_key=True)
    firs_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    created_at = db.Column(db.DateTime)
    movies = db.relationship("Movie", backref="user", lazy=True)

    def __repr__(self):
        return f"User(id={self.id!r}, first_name={self.firs_name}," \
               f" last_name={self.last_name}" \
               f"email={self.email}, password={self.password}," \
               f" role_id={self.role_id}, created_at={self.created_at})"
