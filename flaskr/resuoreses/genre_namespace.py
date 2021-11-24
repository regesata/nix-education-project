"""Module realize routing for genre resource"""
import json
import logging

from flask_restx import Resource, Namespace, fields
from flask_restx.errors import abort
from marshmallow import ValidationError
from flask import request
from flaskr.utils import INVALID_DATA_JSON, INVALID_DATA_STR, LOGGER_NAME
from flask_login import login_required
from flaskr.model.genre_schema import GenreSchema
from flaskr.model.genre import Genre
from flaskr import db

genre_schm = GenreSchema()
api = Namespace('genres', path="//")

add_genre = api.model('Add genre', {
    'title': fields.String()
})
genre_m = api.inherit('Genre', add_genre, {
    'id': fields.Integer()
})
genre_update = api.model('Update',{
    'id': fields.Integer()
})
log = logging.getLogger(LOGGER_NAME)


# pylint: disable=R0201
@api.route('/genre')
class AllGenres(Resource):
    """
    Class realize GET and POST method
    """

    @api.marshal_with(genre_m)
    @api.response(200, "Ok")
    @api.response(404, "Not found")
    @api.param('genre_id', "Id for genre single record")
    def get(self):
        """
        Returns JSON with  record or records from genre table
        Accept parameter genre_id for single record
        """
        genre = None
        g_id = int(request.args.get('genre_id')) if request.args.get('genre_id') \
            else 0
        if g_id:
            genre = Genre.query.get(g_id)
            log.info("User tries to get genre instance id=%d" % g_id)
            if not genre:
                log.info("Genre instance not found")
                return abort(404, error="Not found")
            log.info("Genre instance successfully returned")
            return genre_schm.dump(genre), 200
        log.info("User tries to get all genre instances")
        genres = Genre.query.all()
        if genres:
            log.info("Genre instances successfully returned")
        else:
            log.info("Genre has no one instance")
        return genre_schm.dump(genres, many=True), 200

    @api.marshal_with(genre_m)
    @login_required
    @api.response(401, "Unauthorized")
    @api.response(201, "Successfully added")
    @api.response(400, INVALID_DATA_STR)
    @api.expect(add_genre)
    def post(self):
        """
        Adds record to genre table using data from
        request JSON
        """
        log.info("User tries to add new genre instance")
        try:
            genre = genre_schm.load(request.get_json(), session=db.session)
            db.session.add(genre)
            db.session.commit()
            log.info("Successfully added %s", genre.title)
            return genre_schm.dump(genre), 201
        except ValidationError:
            log.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)
        except AssertionError:
            log.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)


    @api.marshal_with(add_genre)
    @login_required
    @api.expect(genre_update)
    @api.response(200, "Successfully update")
    @api.response(404, "Not found")
    @api.response(401, "Unauthorized")
    @api.response(400, INVALID_DATA_STR)
    def put(self):
        """
        Method updates record using id from JSON
        and additional data
        """
        log.info("User tries to update genre")
        genre = Genre.query.get(request.get_json().get("id"))
        if genre is None:
            log.info("Genre instance not found, id=%d", request.get_json().get("id"))
            return abort(404, error="Not found")
        try:
            genre = genre_schm.load(request.get_json(), session=db.session, instance=genre,
                                    partial=True)
            db.session.add(genre)
            db.session.commit()
            return genre_schm.dump(genre), 200
        except ValidationError:
            log.info(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)
        except AssertionError:
            log.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)


    @login_required
    @api.response(404, "Not found")
    @api.response(204, "Successfully deleted")
    @api.response(401, "Unauthorized")
    @api.param('genre_id', "Id for genre single record")
    def delete(self):
        """
        Deletes record where id equals director_id
        Only admin can perform it
        """
        log.info("User tries to delete genre instance")
        genre = Genre.query.get(request.args.get("genre_id"))
        if genre is None:
            log.info("Genre instance not found, id=%d", request.args.get("genre_id"))
            return abort(404, error="Not found")
        db.session.delete(genre)
        db.session.commit()
        log.info("Genre instance successfully deleted, %r", genre)
        return '', 204
