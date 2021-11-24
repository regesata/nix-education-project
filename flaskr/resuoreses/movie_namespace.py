"""Module realize routing for movie resource"""
import datetime
import logging
from flask_restx import Resource, Namespace, fields
from flask_restx.errors import abort
from flask import request
from marshmallow.exceptions import ValidationError
from flaskr.utils import INVALID_DATA_JSON, INVALID_DATA_STR, LOGGER_NAME
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
log = logging.getLogger(LOGGER_NAME)
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
@api.route('/movie')
class AllMovies(Resource):
    """
    Class realize routing GET and POST methods
    """
    @api.param('rate_order', "Boolean value for ordering by rate")
    @api.param('date_order', "Boolean value for ordering by date")
    @api.param('genre_filter', "Genre title for genre filter.")
    @api.param('release_date_end_filter', "End value for release year filter")
    @api.param('release_date_start_filter', "Start value for release year filter")
    @api.param('director_filter', "Director last_name value for filter. Case sensitive")
    @api.param('search', "Keyword for search, partial matches included. Search on title")
    @api.param('page', "Page number. 10 records per page.")
    @api.response(200, "Returns movies", movie_m)
    @api.response(401, "Bad request")
    @api.response(404, "Not found")
    @api.marshal_with(movie_m)
    def get(self):
        """
        Returns JSON with all records from movie table
        Uses pagination from flask-sqlalchemy
        """
        # pagination
        log.info("User tries to get movies")
        page = int(request.args.get("page")) \
            if request.args.get("page") else PAGE_DEFAULT
        per_page = PER_PAGE_DEFAULT
        movie = Movie.query # Basic query
        # movie title search
        search_key_word = request.args.get("search")
        if search_key_word:  # applying search
            movie = movie.filter(Movie.title.like("%"+search_key_word+"%"))
            log.info("Search by title, keyword, %s" % search_key_word)


        genre_filter = request.args.get("genre_filter")
        if genre_filter: # filtering by genre
            movie = movie.join(Movie.genre).filter(Genre.title == genre_filter)
            log.info("Filter by genre, %s" % genre_filter)

        # filtering by release year range
        date_start = request.args.get("release_date_start_filter")
        if date_start:
            date_start = datetime.date(int(date_start), 1, 1)
        date_end = request.args.get("release_date_end_filter")
        if date_end:
            date_end = datetime.date(int(date_end), 12, 31)
        if bool(date_end) and bool(date_start):
            movie = movie.filter(Movie.release_date.between(date_start, date_end))
            log.info("Filter by years, %s - %s" % (date_start.year, date_end.year))

        # filtering by director last name
        director_filter = request.args.get("director_filter")
        if director_filter:
            movie = movie.join(Movie.director).filter(
             Director.last_name == director_filter)
            log.info("Filter by director last name %s" % director_filter)
        # ordering
        rate_order = request.args.get("rate_order")
        date_order = request.args.get("date_order")
        if rate_order and date_order: # both ordering
            movie = movie.order_by(Movie.rate, Movie.release_date)
            log.info("Ordering by rate and date")
        elif rate_order:
            movie = movie.order_by(Movie.rate)
            log.info("Ordering by rate only")
        elif date_order:
            movie = movie.order_by(Movie.release_date)
            log.info("Ordering by date only")
        # paginator object
        paginator = movie.paginate(page, per_page)
        log.info("Return movies, page=%d" % page)
        return movie_schm.dump(paginator.items, many=True)

    @login_required
    @api.expect(movie_add_model)
    @api.response(400, "Genre or director not found")
    @api.response(401, "Unauthorized user cant add movie")
    @api.response(201, "Movie added successfully")
    def post(self):
        """
        Adds record to movie table from request JSON
        """
        log.info("User %d tries to add movie instance", current_user.id)
        json = request.get_json()
        title = json.get("title")
        year = json["release_date"]
        desc = json["description"]
        poster = json["poster"]
        rate = json["rate"]
        genre = []
        for gen in json["genre"]:
            item = Genre.query.get(gen.get("id"))
            if not item:
                log.info("Genre data is invalid")
                return {"error": "Error in genre"}, 400
            genre.append(item)
        director = []
        for director_item in json["director"]:
            director_inst = Director.query.get(director_item.get("id"))
            if not director_inst:
                log.info("Director data is invalid")
                return {"error": "Error in director"}, 400
            director.append(director_inst)

        movie = Movie()
        try:
            movie.title = title
            movie.genre = genre
            movie.director = director
            movie.user_id = current_user.id
            movie.poster = poster
            movie.description = desc
            movie.release_date = datetime.datetime.strptime(year, "%Y-%m-%d").date()
            movie.rate = rate
            db.session.add(movie)
            db.session.commit()
            log.info("Successfully added movie, %s" % movie.title)
            return movie_schm.dump(movie), 201
        except ValidationError:
            log.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)

    @login_required
    @api.marshal_with(movie_add_model)
    @api.expect(put_model)
    @api.response(401, "Unauthorized")
    @api.response(403, "Forbidden")
    @api.response(404, "Not found")
    @api.response(400, INVALID_DATA_STR)
    @api.response(200, "Updated successfully")
    def put(self):
        """
        Update model using JSON data
        Add data in JSON that needed to update
        """
        log.info("User tries to update movie")
        movie = Movie.query.get(request.json.get("id"))
        if not movie:
            log.info("Movie id=%d not found" % request.get_json().get("id"))
            return abort(404, error="Not found")
        if movie.user_id != current_user.id and current_user.role_id != 1 :
            log.info("User id=%d tries to update movie added by id=%d" % (current_user.id,
                     movie.user_id))
            return abort(403, error="Cant edit. This record added by another user")
        directors = request.get_json().get("director")
        if directors:
            for director in directors:
                if not Director.query.get(director.get("id")):
                    return abort(404, error="Director not found")
        try:
            movie_schm.load(request.get_json(), session=db.session, instance=movie, partial=True)

            db.session.add(movie)
            db.session.commit()
            log.info("Successfully updated id=%d" % movie.id)
            return movie_schm.dump(movie), 200
        except ValidationError:
            log.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)
        except AssertionError:
            log.exception(INVALID_DATA_STR)
            return abort(400, **INVALID_DATA_JSON)


    @login_required
    @api.param('movie_id', "Integer value of movie that should be deleted")
    @api.response(404, "Not found")
    @api.response(403, "Forbidden")
    @api.response(401, "Unauthorized")
    @api.response(204, "Deleted")
    def delete(self):
        """Deletes movie record"""
        m_id =  int(request.args.get("movie_id"))
        log.info("User tries to delete movie id=%d" % m_id)
        movie = Movie.query.get(m_id)
        if not movie:
            log.info("Movie not found")
            return abort(404,error="Not found")
        if current_user.id != movie.user_id:
            log.info("User id=%d tries to delete movie added by id=%d" % (current_user.id,
                     movie.user_id))
            return abort(403, error="Cant delete. Record added by another user")
        db.session.delete(movie)
        db.session.commit()
        log.info("Successfully deleted id=%d" % movie.id)
        return '', 204
