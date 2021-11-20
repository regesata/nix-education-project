"""Module realize routing for movie resource"""
import datetime
from flask_restx import Resource, Namespace, fields
from flask import request
from sqlalchemy import desc
from flask_login import login_required, current_user
from flaskr.model.movie import Movie
from flaskr.model.genre import Genre
from flaskr.model.director import Director
from flaskr import db
from flaskr.model.movie_schema import MovieSchema
from .genre_namespace import add_genre, genre_update
from .director_namespace import director_update, add_director

PAGE_DEFAULT = 1
PER_PAGE_DEFAULT = 10

movie_schm = MovieSchema()

api = Namespace('movies', path='//')

movie_m = api.model('Movie', {
    'id': fields.Integer(),
    'title': fields.String(),
    'genre': fields.List(fields.Nested(add_genre)),
    'release_date': fields.Date(),
    'director': fields.List(fields.Nested(add_director)),
    'description': fields.String(),
    'rate': fields.Integer(),
    'poster': fields.String(),
    'user_id': fields.Integer()
})

movie_add_model = api.model('Add movie', {
    'title': fields.String(),
    'genre': fields.List(fields.Nested(genre_update )),
    'release_date': fields.Date(),
    'director': fields.List(fields.Nested(director_update)),
    'description': fields.String(),
    'rate': fields.Integer(),
    'poster': fields.String()
})

put_model = api.model('Update movie', {
    'id': fields.Integer()
})


# pylint: disable=R0201
@api.route('/movie/')
class AllMovies(Resource):
    """
    Class realize routing GET and POST methods
    """
    @api.param('rate_order', "Boolean value for ordering by rate")
    @api.param('date_order', "Boolean value for ordering by date")
    @api.param('genre_filter', "Value for genre filter.")
    @api.param('release_date_end_filter', "End value for release year filter")
    @api.param('release_date_start_filter', "Start value for release year filter")
    @api.param('director_filter', "Director last_name value for filter. Case sensitive")
    @api.param('search', "Keyword for search, partial matches included. Search on title")
    @api.param('page', "Page number. 10 records per page.")
    @api.response(200, "Returns movies", movie_m)
    @api.response(401, "Bad request")
    @api.marshal_with(movie_m)
    def get(self):
        """
        Returns JSON with all records from movie table
        Uses pagination from flask-sqlalchemy
        """
        page = int(request.args.get("page")) \
            if request.args.get("page") else PAGE_DEFAULT
        per_page = PER_PAGE_DEFAULT
        movie = Movie.query

        search_key_word = request.args.get("search")
        if search_key_word:
            movie = movie.filter(Movie.title.like("%"+search_key_word+"%"))


        genre_filter = request.args.get("genre_filter")
        if genre_filter:

            movie = movie.join(Movie.genre).filter(Genre.title == genre_filter)

        date_start = request.args.get("release_date_start_filter")
        if date_start:
            date_start = datetime.date(int(date_start), 1, 1)
        date_end = request.args.get("release_date_end_filter")
        if date_end:
            date_end = datetime.date(int(date_end), 1, 1)
        if bool(date_end) and bool(date_start):
            movie = movie.filter(Movie.release_date.between(date_start, date_end))

        director_filter = request.args.get("director_filter")
        if director_filter:
            movie = movie.join(Movie.director).filter(
             Director.last_name == director_filter)

        rate_order = request.args.get("rate_order")
        date_order = request.args.get("date_order")
        if rate_order and date_order:
            movie = movie.order_by(Movie.rate, Movie.release_date)
        elif rate_order:
            movie = movie.order_by(Movie.rate)
        elif date_order:
            movie = movie.order_by(Movie.release_date)


        paginator = movie.paginate(page, per_page)
        return movie_schm.dump(paginator.items, many=True)

    @login_required
    @api.expect(movie_add_model)
    @api.response(400, "Genre or director not found")
    @api.response(401, "Unauthorized user cant add movie")
    @api.response(201, "Movie added successfully")
    @api.response(404, "Error in director or genre fields")
    def post(self):
        """
        Adds record to movie table from request JSON
        """
        json = request.get_json()
        title = json.get("title")
        year = json["release_date"]
        desc = json["description"]
        poster = json["poster"]
        rate = json["rate"]
        genre = []
        for gen in json["genre"]:
            g = Genre.query.get(gen.get("id"))
            if not g:
                return {"error": "Error in genre"}, 404
            genre.append(g)
        director = []
        for drctr in json["director"]:
            d = Director.query.get(drctr.get("id"))
            if not g:
                return {"error": "Error in director"}, 404
            director.append(d)

        movie = Movie()
        movie.title = title
        movie.genre = genre
        movie.director = director
        movie.user_id = current_user.id
        movie.poster = poster
        movie.description = desc
        movie.release_date = datetime.datetime.strptime(year, "%Y-%m-%d")
        movie.rate = rate
        db.session.add(movie)
        db.session.commit()
        return movie_schm.dump(movie), 201

    @login_required
    @api.expect(put_model)
    @api.response(401, "Unauthorized")
    @api.response(200, "Updated successfully")
    def put(self):
        """
        Update model using JSON data
        Add data in JSON that needed to update
        """
        movie = Movie.query.filter(Movie.id == request.get_json().get("id")).first()
        if movie.user_id != current_user.id:
            return {"error": "Cant edit."
                             "This record added by another user"}, 403
        movie_schm.load(request.get_json(), session=db.session, instance=movie, partial=True)
        db.session.add(movie)
        db.session.commit()
        return {"message": "Successfully updated"}, 200
