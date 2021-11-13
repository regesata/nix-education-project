"""Module realize routing for movie resource"""

from flask_restx import Resource, Namespace, fields
from flask import request
from flaskr.model.movie import Movie
from flaskr.model.genre import Genre
from flaskr.model.director import Director
from flaskr.model import db
from flaskr.model.movie_schema import MovieSchema

from .genre_namespace import genre_m
from .director_namespace import director_m


movie_schm = MovieSchema()

api = Namespace('movies', path='//')

movie_m = api.model('Movie', {
    'id': fields.Integer(),
    'title': fields.String(),
    'genre': fields.List(fields.Nested(genre_m)),
    'release_year': fields.Integer(),
    'director': fields.List(fields.Nested(director_m)),
    'description': fields.String(),
    'rate': fields.Integer(),
    'poster': fields.String(),
    'user_id': fields.Integer()
})

# pylint: disable=R0201
@api.route('/movie/')
class AllMovies(Resource):
    """
    Class realize routing GET and POST methods
    """
    @api.marshal_with(movie_m)
    def get(self):
        """
        Returns JSON with all records from movie table
        Used pagination from flask-sqlalchemy
        """
        try:
            page = request.args.get("page")
        except ValueError:
            page = 1

        per_page = 10
        movie = Movie.query
        paginator = movie.paginate(page, per_page)
        return movie_schm.dump(paginator.items, many=True)

    def post(self):
        """Adds record to movie table from request JSON"""
        json = request.get_json()
        title = json.get("title")
        year = json["release_year"]
        desc = json["description"]
        poster = json["poster"]
        rate = json["rate"]
        genre = Genre.query.filter(Genre.id.in_(request.get_json()["genre"])).all()
        director = Director.query.filter\
            (Director.id.in_(request.get_json()["director"])).all()
        movie = Movie()
        movie.title = title
        movie.genre = genre
        movie.director = director
        movie.user_id = json["user_id"]
        movie.poster = poster
        movie.description = desc
        movie.release_year = year
        movie.rate = rate
        db.session.add(movie)
        db.session.commit()
        return movie_schm.dump(movie), 201
