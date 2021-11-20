"""Module realize routing for genre resource"""
from flask_restx import Resource, Namespace, fields
from flask import request
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


# pylint: disable=R0201
@api.route('/genre')
class AllGenres(Resource):
    """
    Class realize GET and POST method
    """
    @api.response(200, "Ok")
    @api.response(404, "Not found")
    @api.param('genre_id', "Id for genre single record")
    @api.marshal_with(genre_m)
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
            if not genre:
                return {"message": "Not found"}, 404
            return genre_schm.dump(genre), 200
        else:
            genres = Genre.query.all()
            return genre_schm.dump(genres, many=True), 200

    @login_required
    @api.response(401, "Unauthorized")
    @api.response(201, "Successfully added")
    @api.marshal_with(add_genre)
    @api.expect(add_genre)
    def post(self):
        """
        Adds record to genre table using data from
        request JSON
        """
        genre = genre_schm.load(request.get_json(), session=db.session)
        db.session.add(genre)
        db.session.commit()
        return genre_schm.dump(genre), 201

    @login_required
    @api.marshal_with(genre_m)
    @api.expect(genre_update)
    @api.response(200, "Successfully update")
    @api.response(404, "Not found")
    @api.response(401, "Unauthorized")
    def put(self):
        """
        Method updates record using id from JSON
        and additional data
        """
        genre = Genre.query.get(request.get_json().get("id"))
        if genre is None:
            return {"error": f"Genre: {request.get_json().get('id')} not found"}, 404
        genre = genre_schm.load(request.get_json(), session=db.session, instance=genre,
                                partial=True)
        db.session.add(genre)
        db.session.commit()
        return genre_schm.dump(genre), 200

    @login_required
    @api.response(404, "Not found")
    @api.response(204, "Successfully deleted")
    @api.param('genre_id', "Id for genre single record")
    def delete(self):
        """
        Deletes record where id equals director_id
        Only admin can perform it
        """
        genre = Genre.query.get(request.args.get("genre_id"))
        if genre is None:
            return {"error": f"Genre: {request.args.get('genre_id')} not found"}, 404
        db.session.delete(genre)
        db.session.commit()
        return '', 204
