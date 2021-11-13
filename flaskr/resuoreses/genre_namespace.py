"""Module realize routing for genre resource"""
from flask_restx import Resource, Namespace, fields
from flask import request
from flaskr.model.genre_schema import GenreSchema
from flaskr.model.genre import Genre
from flaskr.model import db

genre_schm = GenreSchema()
api = Namespace('genres', path="//")

genre_m = api.model('Genre', {
    'id': fields.Integer(),
    'title': fields.String()
})


# pylint: disable=R0201
@api.route('/genre')
class AllGenres(Resource):
    """
    Class realize GET and POST method
    """
    @api.marshal_with(genre_m)
    def get(self):
        """Returns JSON with all records from genre table"""
        genres = Genre.query.all()
        return genre_schm.dump(genres, many=True), 200

    def post(self):
        """
        Adds record to genre table using data from
        request JSON
        """
        genre = genre_schm.load(request.get_json(), session=db.session)
        db.session.add(genre)
        db.session.commit()
        return genre_schm.dump(genre), 201

# pylint: disable=R0201
@api.route('/genre/<int:genre_id>')
class SingleGenre(Resource):
    """Realize GET and POST methods for rout"""
    @api.marshal_with(genre_m)
    def get(self, genre_id):
        """
        Returns JSON with record from genre table
        where id equals genre_id
        :param genre_id int id of record from table
        :return JSON with record or error message
        """
        genre = Genre.query.get(genre_id)
        if genre is None:
            return {"error": f"Genre: {genre_id} not found"}, 404
        return genre_schm.dump(genre), 200

    @api.marshal_with(genre_m)
    def put(self, genre_id):
        """
        Updates record where id equals genre_id
        :param genre_id: int id of updated record
        :return: JSON with updated record or error message
        """
        genre = Genre.query.get(genre_id)
        if genre is None:
            return {"error": f"Genre: {genre_id} not found"}, 404
        genre = genre_schm.load(request.get_json(), session=db.session, instance=genre)
        db.session.add(genre)
        db.session.commit()
        return genre_schm.dump(genre), 200

    def delete(self, genre_id):
        """
        Deletes record where id equals genre_id
        :param genre_id: int id of deleted record
        :return: Empty string or error message
        """
        genre = Genre.query.get(genre_id)
        if genre is None:
            return {"error": f"Genre: {genre_id} not found"}, 404
        db.session.delete(genre)
        db.session.commit()
        return '', 204
