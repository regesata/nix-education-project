"""Model for role table"""
from . import db


class Role(db.Model):
    """Class describes role entity"""
    id = db.Column(db.Integer, db.Sequence("role_id_seq"), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user = db.relationship("User", backref="role", lazy=True)

    def __repr__(self):
        return f"Role(id={self.id!r}, title={self.title!r}, description={self.description!r})"
