from flask_restx import Resource, Namespace, fields
from flask import request
from flaskr.model.genre_schema import GenreSchema
from flaskr.model.genre import Genre
from flaskr.model import db

genre_schm = GenreSchema()

api = Namespace('genres', path="//")

# TODO add nested field for movie relation
genre_m = api.model('Genre', {
    'id': fields.Integer(),
    'title': fields.String()
})


@api.route('/genre')
class AllGenres(Resource):
    @api.marshal_with(genre_m)
    def get(self):
        genres = Genre.query.all()
        return genre_schm.dump(genres, many=True), 200

    def post(self):
        genre = genre_schm.load(request.get_json(), session=db.session)
        db.session.add(genre)
        db.session.commit()
        return genre_schm.dump(genre), 201


@api.route('/genre/<int:genre_id>')
class SingleGenre(Resource):

    @api.marshal_with(genre_m)
    def get(self, genre_id):
        genre = Genre.query.get(genre_id)
        if genre is None:
            return {"error": f"Genre: {genre_id} not found"}, 404
        return genre_schm.dump(genre), 200

    @api.marshal_with(genre_m)
    def put(self, genre_id):
        genre = Genre.query.get(genre_id)
        if genre is None:
            return {"error": f"Genre: {genre_id} not found"}, 404
        genre = genre_schm.load(request.get_json(), session=db.session, instance=genre)
        db.session.add(genre)
        db.session.commit()
        return genre_schm.dump(genre), 200

    def delete(self, genre_id):
        genre = Genre.query.get(genre_id)
        if genre is None:
            return {"error": f"Genre: {genre_id} not found"}, 404
        db.session.delete(genre)
        db.session.commit()
        return '', 204
