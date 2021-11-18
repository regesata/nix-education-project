from flask_restx import Api
from .role_namespace import api as role_ns
from .genre_namespace import api as genre_ns
from .director_namespace import api as director_ns
from .user_namespace import api as user_ns
from .movie_namespace import api as movie_ns
api = Api(title='Movies DB')
api.add_namespace(role_ns)
api.add_namespace(genre_ns)
api.add_namespace(director_ns)
api.add_namespace(movie_ns)
api.add_namespace(user_ns)

