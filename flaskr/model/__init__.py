"""Module contain function for db initializations"""

from datetime import date
import logging
from flaskr import utils
from flaskr import db
from flaskr.model import director
from flaskr.model import genre
from flaskr.model import role
from flaskr.model import user
from flaskr.model import movie




log = logging.getLogger(utils.LOGGER_NAME)


def init_db():
    """Creates tables in db"""
    db.create_all()
    log.info("Database table created")
    init_data()


def init_data():
    """Adds initial data in table"""

    if user.User.query.first() or role.Role.query.first() or director.Director.query.first():
        return
    log.info("Database seed begin")
    init_user = user.User()
    init_user.email = "admin@admin.com"
    init_user.password = "pbkdf2:sha256:260000$9gtt930HqsTDK7z6$3f562f64fb5ed9" \
                         "02a3221245ebb726b9f8479884d067501f3531ac1864f69fda"
    init_role = role.Role()
    init_role.title = "Admin"
    init_user.role_id = 1
    init_director = director.Director()
    init_director.first_name = "unknown"
    init_director.last_name = "unknown"
    init_director.date_of_birth = date(year=1800, month=1, day=1)
    db.session.add(init_role)
    db.session.commit()
    init_role = role.Role()
    init_role.id = 2
    init_role.title = "User"
    db.session.add(init_role)
    db.session.add(init_user)
    db.session.add(init_director)
    db.session.commit()
    for i in range(1, 31):
        genre_ = genre.Genre()
        genre_.title = "genre" + str(i)
        db.session.add(genre_)
        director_ = director.Director()
        director_.first_name = "First name " + str(i)
        director_.last_name = "Last name " + str(i)
        director_.date_of_birth = date(year=2000, month=1, day=1+i)
        db.session.add(director_)
        movie_ = movie.Movie()
        movie_.title = f"Title {i + 1}"
        movie_.genre.append(genre_)
        movie_.director.append(director_)
        movie_.release_date = date(year=2000, month=10, day=i)
        movie_.poster = "Poster"
        movie_.rate = i % 11 if i % 11 != 0 else 10
        movie_.description = f"Description {i}"
        movie_.user_id = 1
        db.session.add(movie_)
    db.session.commit()
    log.info("Seeding done")
