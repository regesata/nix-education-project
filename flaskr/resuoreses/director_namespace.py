"""Module realize routing for director resource"""

from flask_restx import Resource, Namespace, fields
from flask import request
from flaskr.model.director_schema import DirectorSchema
from flaskr.model.director import Director
from flaskr import db


director_schm = DirectorSchema()

api = Namespace('directors', path='//')

director_m = api.model('Director', {
    'id': fields.Integer(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'date_of_birth': fields.Date(),

})

# pylint: disable=R0201
@api.route('/director')
class AllDirectors(Resource):
    """Class realize routing for GET and POST request methods"""

    @api.marshal_with(director_m)
    def get(self):
        """
        Returns JSON with all records from
        director table
        """
        director = Director.query.all()
        return director_schm.dump(director, many=True)

    def post(self):
        """
        Creates record from request JSON and adds it to
        director table
        """
        director = director_schm.load(request.get_json(), session=db.session)
        db.session.add(director)
        db.session.commit()
        return director_schm.dump(director), 201

# pylint: disable=R0201
@api.route('/director/<int:director_id>')
class SingleDirector(Resource):
    """Class realize GET and POST methods """

    @api.marshal_with(director_m)
    def get(self, director_id):
        """
        Method returns JSON with record from director table
        where id equals director_id
        :param director_id: int id for record from table
        :return: JSON with record
        """
        director = Director.query.get(director_id)
        if director is None:
            return {"error": f"Director: {director_id} not found"}, 404
        return director_schm.dump(director), 200

    @api.marshal_with(director_m)
    def put(self, director_id):
        """
        Method updates record using director_id
        parameter and data from request JSON
        """
        director = Director.query.get(director_id)
        if director is None:
            return {"error": f"Director: {director_id} not found"}, 404
        director = director_schm.load(request.get_json(), session=db.session,
                                      instance=director)
        db.session.add(director)
        db.session.commit()
        return director_schm.dump(director)

    def delete(self, director_id):
        """Deletes record where id equals director_id"""
        director = Director.query.get(director_id)
        if director is None:
            return {"error": f"Director: {director_id} not found"}, 404
        db.session.delete(director)
        db.session.commit()
        return '', 204
