"""
Module contains pytest fixtures
and config class
"""

import json
import pytest
import res
from flaskr import create_app, db
from flaskr.resuoreses import api
from flaskr.model import init_data

import logging


class TestConfig:
    """Test app configuration"""
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:test.db"
    TESTING = True
    SECRET_KEY = "too secret"


@pytest.fixture(scope="module")
def app():
    """Creates test app"""
    logging.getLogger("main_logger").setLevel(logging.CRITICAL)
    app = create_app(TestConfig)
    api.init_app(app)

    yield app


@pytest.fixture(scope="function")
def client(app):
    """Returns context and teardown session"""

    db.create_all(app=app)

    with app.app_context():
        init_data()
        with app.test_client() as client:
            yield client
    db.session.remove()
    db.drop_all(app=app)


@pytest.fixture()
def auth_admin(client):
    """Makes login as admin"""
    client.post('/login', data=json.dumps(res.user_admin), content_type='application/json')


@pytest.fixture()
def auth_user(client):
    """Makes login as user"""
    client.post('/signup', data=json.dumps(res.user), content_type='application/json')


@pytest.fixture()
def add_movie(client, auth_user):
    """Adds movie to table as user """
    for dr in res.directors:
        client.post('/director', data=json.dumps(dr), content_type='application/json')
    for gnr in res.genres:
        client.post('/genre', data=json.dumps(gnr), content_type='application/json')
    client.post('/movie', data=json.dumps(res.movies[0]), content_type='application/json')
    client.post('/movie', data=json.dumps(res.movies[1]), content_type='application/json')


@pytest.fixture()
def add_movie_adm(client, auth_admin):
    """Adds movie to table as admin """
    for dr in res.directors:
        client.post('/director', data=json.dumps(dr), content_type='application/json')
    for gnr in res.genres:
        client.post('/genre', data=json.dumps(gnr), content_type='application/json')
    client.post('/movie', data=json.dumps(res.movies[0]), content_type='application/json')
    client.post('/movie', data=json.dumps(res.movies[1]), content_type='application/json')
    client.get('/logout')
