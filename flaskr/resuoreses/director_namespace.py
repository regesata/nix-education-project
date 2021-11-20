"""Module realize routing for director resource"""

from flask_restx import Resource, Namespace, fields
from flask import request
from flask_login import login_required
from flaskr.model.director_schema import DirectorSchema
from flaskr.model.director import Director
from flaskr import db


director_schm = DirectorSchema()

api = Namespace('directors', path='//')

add_director = api.model('Add director', {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'date_of_birth': fields.Date(),
})

director_m = api.inherit('Director', add_director, {
    'id': fields.Integer()
})

director_update = api.model('Update', {
    'id': fields.Integer()
})


# pylint: disable=R0201
@api.route('/director')
class AllDirectors(Resource):
    """Class realize routing for GET and POST request methods"""
    @api.marshal_with(director_m)
    @api.response(200, "Success")
    @api.response(404, "Not found")
    @api.param('director_id', "Id of director for singe record")
    def get(self):
        """
        Returns JSON with  records from
        director table accept id for one record
        """
        director = None
        d_id = int(request.args.get("director_id")) if request.args.get("director_id") else 0
        if d_id:
            director = Director.query.get(d_id).first()
            print(director)
            if not director:
                return {"message": "Not found"}, 404
            return director_schm.dump(director), 200
        else:
            director = Director.query.all()
        return director_schm.dump(director, many=True), 200

    @login_required
    @api.response(401, "Unauthorized")
    @api.response(201, "Successfully added")
    @api.expect(add_director)
    def post(self):
        """
        Creates record from request JSON and adds it to
        director table
        """
        director = director_schm.load(request.get_json(), session=db.session)
        db.session.add(director)
        db.session.commit()
        return director_schm.dump(director), 201

    @api.marshal_with(director_m)
    @api.expect(director_update)
    @api.response(200, "Successfully update")
    @api.response(404, "Not found")
    @api.response(401, "Unauthorized")
    @login_required
    def put(self):
        """
        Method updates record using id from JSON
        and additional data
        """
        director = Director.query.get(int(request.get_json().get("id")))
        if director is None:
            return {"error": f"Director: {request.get_json().get('id')} not found"}, 404
        director = director_schm.load(request.get_json(), session=db.session,
                                      instance=director, partial=True)
        db.session.add(director)
        db.session.commit()
        return director_schm.dump(director), 200

    @api.param('director_id', "Id of director for singe record")
    @login_required
    @api.response(404, "Not found")
    @api.response(204, "Successfully deleted")
    def delete(self):
        """
        Deletes record where id equals director_id
        Only admin can perform it
        """
        director = Director.query.get(int(request.args.get("director_id")))
        if director is None:
            return {"error": f"Director: {request.args.get('director_id')}"
                             f" not found"}, 404
        db.session.delete(director)
        db.session.commit()
        return '', 204
