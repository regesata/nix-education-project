"""Module realize login/logout/signup functionality """
from datetime import datetime
from flask_restx import Resource, Namespace, fields
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user
from flask_login import current_user, logout_user, AnonymousUserMixin
from flaskr.model.user_schema import UserSchema
from flaskr.resuoreses.movie_namespace import movie_m
from flaskr.model.user import User
from flaskr import db

USER_ROLE_ADMIN = 1
USER_ROLE_USER = 2

user_schm = UserSchema()

api = Namespace('users', path='//')

# model for marshalling
user_m = api.model('User', {
    'id': fields.Integer(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'password': fields.String(),
    'role_id': fields.Integer(),
    'created_at': fields.DateTime(),
    'movies': fields.List(fields.Nested(movie_m))
})

# model for expect decorator
user_exp_model = api.model('Add User', {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'password': fields.String(),
})
user_exp_model_admin = api.inherit('Add by admin', user_exp_model, {
    'role': fields.Integer()
})

login_exp_model = api.model('Login', {
    'email': fields.String(),
    'password': fields.String(),
    'remember': fields.Boolean()
})


# pylint: disable=R0201
@api.route('/user')
class AllUsers(Resource):
    """Class realize routing for /user endpoint """
    @login_required
    @api.marshal_with(user_exp_model)
    @api.doc('Method returns user profile info or all users '
             "if admin is current user")
    @api.doc(responses={401: "Not authorized", 200: "OK"})
    def get(self):
        """
        Returns user to user profile information .
        If current user is Admin returns all user
        """
        if not isinstance(current_user, AnonymousUserMixin) and \
                current_user.role_id == USER_ROLE_ADMIN:
            return user_schm.dump(User.query.all(), many=True), 200
        return user_schm.dump(User.query.filter(User.id == current_user.id).first()), 200

    @api.expect(user_exp_model_admin)
    @api.marshal_with(user_m)
    @api.doc(responses={401: "Not Authorized", 201: "User added"})
    @api.doc("Method allows to Admin add new user")
    @login_required
    def post(self):
        """Method that allows Admin add new user"""
        if not isinstance(current_user, AnonymousUserMixin) and \
                current_user.role_id != USER_ROLE_ADMIN:
            return {"error": "Not authorized"}, 401
        user_json = request.get_json()
        user = User.query.filter(User.email == user_json.get('email')).first()
        if user:
            return {'error': f'User with email {user_json.get("email")}'
                             f' already exists'}, 409
        user = User()
        user_new = user_schm.load(user_json, session=db.session, instance=user)
        user_new.password = generate_password_hash(user_json.get('password'), method='sha256')
        user.created_at = datetime.now()
        db.session.add(user)
        db.session.commit()
        return user_schm.dump(user), 201


    @login_required
    @api.expect(user_exp_model)
    @api.doc(responses={401: "Not authorized", 200: "Ok", 403: "Administrator rights required"})
    def put(self):
        """
        Method allows user to change profile information
        """

        user = user_schm.load(request.get_json(), session=db.session, instance=current_user)
        role = request.get_json().get("role")
        if role == USER_ROLE_ADMIN and current_user.role.id != USER_ROLE_ADMIN:
            return {"error": "Only administrator can change roles"}, 403
        user.password = generate_password_hash(request.get_json().get('password'),
                                               method='sha256')
        db.session.add(user)
        db.session.commit()
        return user_schm.dump(user), 200


# pylint: disable=R0201
@api.route('/login')
class Login(Resource):
    """Class realizes login process"""

    @api.expect(login_exp_model)
    @api.doc(responses={404: "Invalid login or password", 200: "OK"})
    def post(self):
        """
        Login user using email and password
        """
        user_email = request.get_json().get("email")
        user_pass = request.get_json().get("password")
        user_remember = request.get_json().get("remember")
        user = User.query.filter(User.email == user_email).first()
        if user and check_password_hash(user.password, user_pass):
            login_user(user, remember=user_remember)
            return {"message": "Authorized successfully"}, 200
        return {"error": "Invalid email or password"}, 404


# pylint: disable=R0201
@api.route('/logout')
class UserLogout(Resource):
    """Class realized logout for user"""

    @login_required
    @api.doc(responses={401: "Not authorized", 200: "OK"})
    def get(self):
        """Logout for current user"""
        logout_user()
        return {"message": "Logout Successfully"}, 200


# pylint: disable=R0201
@api.route('/signup')
class UserSignUp(Resource):
    """Realized signup for user"""
    @api.doc(responses={400: "User exists", 201: "User created",
                        403: "Authorized user cant signup"})
    @api.expect(user_exp_model)
    def post(self):
        """Sign up a user"""
        if isinstance(current_user, User):
            return {"error": "Authorized user cant signup"}, 403
        user_email = request.get_json().get("email")
        if User.query.filter(User.email == user_email).first():
            return {"error": "User with this email already exists"}, 400
        if not request.get_json().get("password"):
            return {"error": "Empty password"}, 400
        user = user_schm.load(request.get_json(), session=db.session)
        user.password = generate_password_hash(
            request.get_json().get("password"), method="sha256")
        user.role_id = USER_ROLE_USER
        user.created_at = datetime.now()
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return {"message": "User create"}, 201
