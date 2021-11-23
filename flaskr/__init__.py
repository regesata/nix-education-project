"""
Initializing of flask app and db connection
"""
from flask import Flask
from utils import AppConfig, get_logger_fact, LOGGER_NAME
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

log = get_logger_fact(LOGGER_NAME)

app = Flask(__name__)
app.config.from_object(AppConfig)


db = SQLAlchemy(app)
log_manager = LoginManager()
log_manager.init_app(app)


from flaskr.model import director
from flaskr.model import genre
from flaskr.model import role
from flaskr.model import user
from flaskr.model import movie


@log_manager.user_loader
def load_user(user_id):
    return user.User.query.get(user_id)


db.create_all()
db.session.commit()
log.info("Database table created")
migrate = Migrate()
migrate.init_app(app, db)
log.info("Application started")


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
    db.session.add(init_role)
    init_role.description = "User"
    init_role.id = 2
    db.session.add(init_role)
    db.session.add(init_user)
    db.session.add(init_director)
    db.session.commit()
    log.info("Database initial data added")



