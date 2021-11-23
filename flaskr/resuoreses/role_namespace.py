"""Module realize access to roles resource"""
import logging
from flask_restx import Resource, Namespace, fields
from marshmallow import ValidationError
from flask import request
from flask_login import login_required
from flaskr.utils import LOGGER_NAME, INVALID_DATA_STR, INVALID_DATA_JSON
from flaskr.model.role_schema import RoleSchema
from flaskr.model.role import Role
from flaskr.resuoreses.user_namespace import is_admin
from flaskr import db

role_schm = RoleSchema()

log = logging.getLogger(LOGGER_NAME)
api = Namespace('roles', path="//")
add_role_m = api.model('Add role', {
    'title': fields.String(),
    'description': fields.String()
})

role_m = api.inherit('Role', add_role_m, {
    'id': fields.Integer()
})

update_role = api.model('Update', {
    'id': fields.Integer()
})


# pylint: disable=R0201
@api.route('/role')
class AllRoles(Resource):
    """Class realize routing for get and
     post methods """

    @api.param("role_id", "Id for single record")
    @api.marshal_with(role_m)
    @api.response(200, "OK")
    @api.response(404, "Not found")
    @api.response(401, "Unauthorized")
    @api.response(403, "Forbidden")
    @login_required
    def get(self):
        """
        Get record from table Roles
        Only administrator can perform it
        """
        log.info("User tries to get role instances")
        if not is_admin():
            log.info("Current user hasn't enough rights ")
            return {"error": "Only admin can perform it"}, 403
        roles = None
        r_id = int(request.args.get("role_id")) if request.args.get("role_id") \
            else False
        if r_id:
            roles = Role.query.get(r_id)
            if not roles:
                log.info("Role id=%d not found" % r_id)
                return {"error": "Not Found"}, 404
            log.info("Successfully return role id=%d" % r_id)
            return role_schm.dump(roles), 200

        roles = Role.query.all()
        log.info("Successfully return all roles instances")
        return role_schm.dump(roles, many=True), 200

    @api.expect(add_role_m)
    @api.marshal_with(role_m)
    @login_required
    @api.response(400, INVALID_DATA_STR)
    @api.response(401, "Unauthorized")
    @api.response(201, "Add new record")
    @api.response(403, "Forbidden")
    def post(self):
        """Creates a new record using json in request"""
        log.info("User tries to add new role")
        if not is_admin():
            log.info("Current user hasn't enough rights ")
            return {"error": "Only admin can perform it"}, 403
        try:
            role = role_schm.load(request.get_json(), session=db.session)
            db.session.add(role)
            db.session.commit()
            log.info("Successfully added %s role", role.title)
            return role_schm.dump(role), 201
        except ValidationError:
            log.exception(INVALID_DATA_STR)
            return INVALID_DATA_JSON, 400

    @api.marshal_with(role_m)
    @api.expect(update_role)
    @login_required
    @api.response(400, INVALID_DATA_JSON)
    @api.response(403, "Forbidden")
    @api.response(401, "Unauthorized")
    @api.response(404, "Not found")
    def put(self):
        """
        Updates record using JSON data
        """
        log.info("User tries to update role")
        if not is_admin():
            log.info("Current user hasn't enough rights ")
            return {"error": "Only admin can perform it"}, 403
        r_id = request.json.get("id")
        if r_id == 1:
            log.info("Cant update Admin role")
        role = Role.query.get(r_id)
        try:
            role_new = role_schm.load(request.get_json(), session=db.session, instance=role,
                                      partial=True)
            db.session.add(role_new)
            db.session.commit()
            log.info("Successfully update role id=%d" % role.id)
            return role_schm.dump(role), 200
        except ValidationError:
            log.exception(INVALID_DATA_STR)
            return INVALID_DATA_JSON, 400

    @api.response(403, "Forbidden")
    @api.response(401, "Unauthorized")
    @api.response(404, "Not found")
    @api.response(204, "Deleted")
    @api.param("role_id", "Id for single record")
    def delete(self):
        """Deletes record by id"""
        if not is_admin():
            log.info("Current user hasn't enough rights ")
            return {"error": "Only admin can perform it"}, 403
        r_id = int(request.args.get("role_id")) if request.args.get("role_id") \
            else False
        role = Role.query.get(r_id)
        if r_id in (1, 2):
            log.info("Cant delete basic roles")
            return {"error": "Cant delete"}, 403
        if role is None:
            log.info("Role not found id=%d" % r_id)
            return {"error": f"Role:{r_id} not found"}, 404
        db.session.delete(role)
        db.session.commit()
        log.info("Successfully delete role id=%d" % role.id)
        return '', 204
