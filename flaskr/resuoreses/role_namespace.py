"""Module realize access to roles resource"""
from flask_restx import Resource, Namespace, fields
from flask import request
from flaskr.model.role_schema import RoleSchema
from flaskr.model.role import Role
from flaskr.model import db

role_schm = RoleSchema()

# TODO add nested field for user relation
api = Namespace('roles', path="//")
role_m = api.model('Role', {
    'id': fields.Integer(),
    'title': fields.String(),
    'description': fields.String()
})


# pylint: disable=R0201
@api.route('/role')
class AllRoles(Resource):
    """Class realize routing for get and
     post methods """

    @api.doc('Get all roles')
    @api.marshal_with(role_m)
    def get(self):
        """Get all records from table Roles"""
        roles = Role.query.all()
        return role_schm.dump(roles, many=True), 200


    @api.doc('Create role')
    def post(self):
        """Creates a new record using json in request"""
        role = role_schm.load(request.get_json(), session=db.session)
        db.session.add(role)
        db.session.commit()
        return role_schm.dump(role), 201


# pylint: disable=R0201
@api.route('/role/<int:role_id>')
class SingleRole(Resource):
    """Class realizes  routing for single record"""

    @api.marshal_with(role_m)
    def get(self, role_id):
        """Returns record by id if not found returns JSON
        with Not found message
        :param role_id int primary key for record
        :return JOSN with record content or JSON with Not found message"""
        role = Role.query.get(role_id)
        if role is None:
            return {"error": f"Role:{role_id} not found"}, 404
        return role_schm.dump(role, many=False), 200


    @api.marshal_with(role_m)
    def put(self, role_id):
        """Updates record by id
        :param role_id int id of record
        :return JSON with updated record or Not found"""
        role = Role.query.get(role_id)
        if role is None:
            return {"error": f"Role:{role_id} not found"}, 404
        new_role = role_schm.load(request.get_json(force=True),
                                  session=db.session, instance=role)
        db.session.add(new_role)
        db.session.commit()
        return role_schm.dump(new_role), 200

    def delete(self, role_id):
        """Deletes record by id"""
        role = Role.query.get(role_id)
        if role is None:
            return {"error": f"Role:{role_id} not found"}, 404
        db.session.delete(role)
        db.session.commit()
        return '', 204
