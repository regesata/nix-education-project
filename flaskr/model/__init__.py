from flaskr import db
from datetime import date
import logging
from flaskr import utils
from flaskr.model import director
from flaskr.model import genre
from flaskr.model import role
from flaskr.model import user
from flaskr.model import movie

log = logging.getLogger(utils.LOGGER_NAME)


def init_db():
    db.create_all()
    log.info("Database table created")
    init_data()


def init_data():
    if user.User.query.first() or role.Role.query.first() or director.Director.query.first():
        return
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
    log.info("Database initial data added")

