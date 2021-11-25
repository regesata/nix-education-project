"""Module realize login/logout/signup functionality """
import json
from datetime import datetime
import logging

from marshmallow import ValidationError
from flask_restx import Resource, Namespace, fields, marshal
from flask_restx.errors import abort
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user
from flask_login import current_user, logout_user, AnonymousUserMixin
from  flaskr.utils import LOGGER_NAME, INVALID_DATA_JSON, INVALID_DATA_STR
from flaskr.model.user_schema import UserSchema
from flaskr.model.role import Role

from flaskr.resuoreses.movie_namespace import movie_m
from flaskr.model.user import User
from flaskr import db

USER_ROLE_ADMIN = 1
USER_ROLE_USER = 2

user_schm = UserSchema()

api = Namespace('users', path='//')
log = logging.getLogger(LOGGER_NAME)

# model for marshalling
user_m = api.model('User', {
    'id': fields.Integer(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'password': fields.String(),
    'role': fields.Integer(),
    'created_at': fields.DateTime(),
    'movies': fields.List(fields.Nested(movie_m))
})

# model for expect decorator
user_exp_model = api.model('Add User', {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'password': fields.String()
})
user_exp_model_admin = api.inherit('Add by admin', user_exp_model, {
    'role': fields.Integer()
})

login_exp_model = api.model('Login', {
    'email': fields.String(),
    'password': fields.String(),
    'remember': fields.Boolean()
})
update_user_m = api.model('Update',{
    'email': fields.String()
})

login_success =api.model('Return message', {'message': fields.String()})


def is_admin() -> bool:
    """
    Checks current user role.
    If admin returns True
    """
    if current_user.role_id == USER_ROLE_ADMIN:
        return True

    return False


# pylint: disable=R0201
@api.route('/user')
class AllUsers(Resource):
    """Class realize routing for /user endpoint """

    @login_required
    @api.marshal_with(user_exp_model)
    @api.doc('Method returns user profile info or all users '
             "if admin is current user")
    @api.response(401, "Not authorized")
    @api.response(200, "OK")
    def get(self):
        """
        Returns user to user profile information .
        If current user is Admin returns all user
        """
        log.info("User tries to get all users")
        if is_admin():
            log.info("Current user is Admin. Get all users")
            return user_schm.dump(User.query.join(Role).all(), many=True), 200
        log.info("Current user role_id=%d get only own data" % current_user.role_id)
        return user_schm.dump(User.query.join(Role, Role.id == User.role_id)
                              .filter(User.id == current_user.id).first()), 200

    @api.expect(user_exp_model_admin)
    @api.marshal_with(user_exp_model)
    @api.response(400, INVALID_DATA_STR)
    @api.response(401, "Not Authorized")
    @api.response(201, "User added")
    @login_required
    def post(self):
        """Method that allows Admin add new user"""
        log.info("User tries to add new user")
        if not is_admin():
            log.info("User has not enough rights")
            return abort(401, error="Not authorized")
        user_json = request.get_json()
        user = User.query.filter(User.email == user_json.get('email')).first()
        if user:
            log.info("Email %s is already uses" % user_json.get('email'))
            return abort(400, error=f'User with email {user_json.get("email")}'
                             f' already exists')
        try:
            user = User()
            user_new = user_schm.load(user_json, session=db.session, instance=user)
            user_new.password = generate_password_hash(user_json.get('password'), method='sha256')
            user.created_at = datetime.now()
            db.session.add(user)
            db.session.commit()
            return user_schm.dump(user), 201
        except ValidationError:
            log.exception(INVALID_DATA_STR)
            return INVALID_DATA_JSON, 400


    @login_required
    @api.marshal_with(update_user_m)
    @api.expect(user_exp_model)
    @api.response(401, "Not authorized")
    @api.response(200, "OK")
    @api.response(403, "Administrator rights required")
    @api.response(400, "Bad request")
    def put(self):
        """
        Method allows user to change profile information
        """
        log.info("User tries to update some data in its profile")
        try:
            if current_user.email != request.get_json().get("email"):
                log.info("Can update own profile only")
                abort(403, error="Can update own profile only")
            user = user_schm.load(request.get_json(), session=db.session, instance=current_user)
            role = request.get_json().get("role")
            if not is_admin() and role:
                log.info("User tries to change role without admin rights ")
                return abort(403, error="Only administrator can change roles")
            password = request.get_json().get('password')
            if password:
                if len(password) < 8:
                    log.info("User tries to change password. Password too short")
                    return abort(400, error="Password too short")
                user.password = generate_password_hash(request.get_json().get('password'),
                                                   method='sha256')
            db.session.add(user)
            db.session.commit()
            log.info("Successfully updated")
            return user_schm.dump(user), 200
        except ValidationError:
            log.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)
        except AssertionError:
            log.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)


# pylint: disable=R0201
@api.route('/login')
class Login(Resource):
    """Class realizes login process"""
    @api.marshal_with(login_success)
    @api.expect(login_exp_model)
    @api.response(404, "Invalid login or password")
    @api.response(200, "OK")
    def post(self):
        """
        Login user using email and password
        """
        log.info("User tries to login")
        user_email = request.get_json().get("email")
        user_pass = request.get_json().get("password")
        user_remember = request.get_json().get("remember")
        user = User.query.filter(User.email == user_email).first()
        if user and check_password_hash(user.password, user_pass):
            login_user(user, remember=user_remember)
            log.info("Authorized email=%s" % user_email)
            return {"message": "Authorized successfully"}
        log.info("Invalid password o email")
        return abort(404, error="Invalid email or password")


# pylint: disable=R0201
@api.route('/logout')
class UserLogout(Resource):
    """Class realized logout for user"""

    @api.marshal_with(login_success)
    @login_required
    @api.response(200, "Logout Successfully" )
    def get(self):
        """Logout for current user"""
        log.info("User tries to logout")
        email = current_user.email
        logout_user()
        log.info("Successfully logout, email=%s" % email)
        return {"message": "Logout Successfully"}, 200


# pylint: disable=R0201
@api.route('/signup')
class UserSignUp(Resource):
    """Realized signup for user"""
    @api.marshal_with(login_success)
    @api.response(400, "User exists")
    @api.response(201, "User created")
    @api.response(403, "Authorized user cant signup")
    @api.expect(user_exp_model)
    def post(self):
        """Sign up a user and login"""
        if isinstance(current_user, User):
            log.info("Authorized user tries to signup again")
            return abort(400, error="Authorized user cant signup")
        user_email = request.get_json().get("email")
        if User.query.filter(User.email == user_email).first():
            log.info("Email already used")
            return abort(400, error="User with this email already exists")
        if not request.get_json().get("password"):
            log.info("Empty password")
            return abort(400, error="Empty password")
        try:
            user = user_schm.load(request.get_json(), session=db.session)
            user.password = generate_password_hash(
                request.get_json().get("password"), method="sha256")
            user.role_id = USER_ROLE_USER
            user.created_at = datetime.now()
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return {"message": "User create"}, 201
        except ValidationError:
            log.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)
        except AssertionError:
            log.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)

