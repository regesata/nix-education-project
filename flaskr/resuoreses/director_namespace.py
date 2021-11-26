"""Module realize routing for director resource"""
import logging
from flask_restx import Resource, Namespace, fields
from flask_restx.errors import abort
from marshmallow.exceptions import ValidationError
from flask import request
from flask_login import login_required
from flaskr.model.director_schema import DirectorSchema
from flaskr.model.director import Director
from flaskr.model.movie import Movie
from flaskr.utils import LOGGER_NAME, INVALID_DATA_JSON, INVALID_DATA_STR
from flaskr import db

d_logger = logging.getLogger(LOGGER_NAME)

director_schm = DirectorSchema()

api = Namespace('directors', path='//')

add_director = api.model('Add director', {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'date_of_birth': fields.Date(),
})

director_m = api.inherit('Get director', add_director, {
    'id': fields.Integer()
})

director_update = api.model('Update director', {
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
            director = Director.query.get(d_id)
            d_logger.info("User requests director instance, %d" % d_id)
            if not director:
                d_logger.info("Instance not found")
                return abort(404,error="Not found")
            d_logger.info("Successfully returned director instance ")
            return director_schm.dump(director), 200
        d_logger.info("User requests all director instances")
        director = Director.query.all()
        d_logger.info("Successfully returned")
        return director_schm.dump(director, many=True), 200


    @login_required
    @api.marshal_with(add_director)
    @api.response(401, "Unauthorized")
    @api.response(201, "Successfully added")
    @api.response(400, INVALID_DATA_STR)
    @api.expect(add_director)
    def post(self):
        """
        Creates record from request JSON and adds it to
        director table
        """

        d_logger.info("User tries to add new director")
        try:
            director = director_schm.load(request.get_json(), session=db.session)
            db.session.add(director)
            db.session.commit()
            d_logger.info("Successfully added, %r" % director)
            return director_schm.dump(director), 201
        except ValidationError:
            d_logger.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)
        except AssertionError:
            d_logger.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)


    @api.marshal_with(director_m)
    @api.expect(director_update)
    @api.response(200, "Successfully update")
    @api.response(404, "Not found")
    @api.response(401, "Unauthorized")
    @api.response(403, "Cant modify")
    @login_required
    def put(self):
        """
        Method updates record using id from JSON
        and additional data
        """
        d_logger.info("User tries to update director instance")
        if request.get_json().get("id") == 1:
            d_logger.info("User tries to update unknown director")
            return abort(403, message="Cant modify")
        director = Director.query.get(int(request.get_json().get("id")))
        if director is None:
            d_logger.info("Instance not found")
            return abort(404, error="Not found")
        try:
            director = director_schm.load(request.get_json(), session=db.session,
                                          instance=director, partial=True)
            db.session.add(director)
            db.session.commit()
            d_logger.info("Updated successfully, %r" % director)
            return director_schm.dump(director), 200
        except ValidationError:
            d_logger.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)
        except AssertionError:
            d_logger.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)



    @api.param('director_id', "Id of director for singe record")
    @login_required
    @api.response(404, "Not found")
    @api.response(403, "Cant delete")
    @api.response(204, "Successfully deleted")
    def delete(self):
        """
        Deletes record where id equals director_id
        Only admin can perform it
        """
        d_logger.info("User tries to delete director instance")
        if int(request.args.get("director_id")) == 1:
            d_logger.info("User tries to delete unknown instance")
            return abort(403, message="Cant delete")
        director = Director.query.get(int(request.args.get("director_id")))
        if director is None:
            d_logger.info("Instance not found")
            return abort(404, error="Not found")
        movie_check = Movie.query.join(Movie.director).filter(Director.id == director.id).all()
        for mov in movie_check:
            if len(mov.director) == 1:
                mov.director.append(Director.query.get(1))
                d_logger.info("Movie %d director set to unknown " % mov.id)

        db.session.delete(director)
        db.session.commit()
        d_logger.info("Deleted successfully, %r" % director)
        return '', 204
