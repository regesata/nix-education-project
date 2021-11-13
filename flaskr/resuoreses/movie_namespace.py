from flask_restx import Resource, Namespace, fields
from flask import request
from flaskr.model.movie_schema import MovieSchema
from .genre_namespace import genre_m
from .director_namespace import director_m
from flaskr.model.movie import Movie
from flaskr.model.genre import Genre
from flaskr.model.director import Director
from flaskr.model import db

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


@api.route('/movie')
class AllMovies(Resource):

    @api.marshal_with(movie_m)
    def get(self):
        movie = Movie.query.all()
        return movie_schm.dump(movie, many=True)

    def post(self):
        json = request.get_json()
        title = json.get("title")
        year = json["release_year"]
        desc = json["description"]
        poster = json["poster"]
        rate = json["rate"]
        genres_list = json["genre"]
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
        print(movie)
        db.session.add(movie)
        db.session.commit()
        return movie_schm.dump(movie), 200



        # db.session.add(movie)
        # db.session.commit()
        # return movie_schm.load(movie), 201
