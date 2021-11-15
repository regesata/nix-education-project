from flask_restx import Resource, Namespace, fields
from flask import request
from flaskr.model.user_schema import UserSchema
from flaskr.model.user import User
from flaskr.model import db

user_schm = UserSchema()

api = Namespace('Users', path='//')

user_m = api.model('User', {
    'id': fields.Integer(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'password': fields.String(),
    'role': fields.Integer(),
    'created_at': fields.DateTime()
})
# TODO next functionality should be realized with Flask-login


