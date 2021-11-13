from flask_restx import Resource, Namespace, fields
from flask import request
from flaskr.model.director_schema import DirectorSchema
from flaskr.model.director import Director
from flaskr.model import db
from flaskr.model import movie_schema

director_schm = DirectorSchema()

api = Namespace('directors', path='//')
# TODO nested field for movies relation

director_m = api.model('Director', {
    'id': fields.Integer(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'date_of_birth': fields.Date(),

})


@api.route('/director')
class AllDirectors(Resource):

    @api.marshal_with(director_m)
    def get(self):
        director = Director.query.all()
        return director_schm.dump(director, many=True)

    def post(self):
        director = director_schm.load(request.get_json(), session=db.session)
        db.session.add(director)
        db.session.commit()
        return director_schm.dump(director), 201


@api.route('/director/<int:director_id>')
class SingleDirector(Resource):

    @api.marshal_with(director_m)
    def get(self, director_id):
        director = Director.query.get(director_id)
        if director is None:
            return {"error": f"Director: {director_id} not found"}, 404
        return director_schm.dump(director), 200

    @api.marshal_with(director_m)
    def put(self, director_id):
        director = Director.query.get(director_id)
        if director is None:
            return {"error": f"Director: {director_id} not found"}, 404
        director = director_schm.load(request.get_json(), session=db.session,
                                      instance=director)
        db.session.add(director)
        db.session.commit()
        return director_schm.dump(director)

    def delete(self, director_id):
        director = Director.query.get(director_id)
        if director is None:
            return {"error": f"Director: {director_id} not found"}, 404
        db.session.delete(director)
        db.session.commit()
        return '', 204



