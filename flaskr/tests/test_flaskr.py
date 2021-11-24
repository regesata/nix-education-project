import pytest
import json

import res


def test_genre_post(client, auth_admin):
    rv = client.post('/genre', data=json.dumps(res.genre_1), content_type='application/json')
    assert rv.json.get("title") == res.genre_1.get("title")
    rv = client.post('/genre', data=json.dumps(res.genre_2), content_type='application/json')
    assert rv.status == "400 BAD REQUEST"
    rv = client.post('/genre', data=json.dumps(res.genre_3), content_type='application/json')
    assert rv.status == "400 BAD REQUEST"
    rv = client.post('/genre', data=json.dumps(res.genre_4), content_type='application/json')
    assert rv.status == "400 BAD REQUEST"


def test_genre_get(client, auth_admin):
    client.post('/genre', data=json.dumps(res.genre_1), content_type='application/json')
    client.post('/genre', data=json.dumps(res.genre_5), content_type='application/json')
    rs = client.get('/genre')
    assert rs.json[0].get("title") == "Action"
    assert rs.json[1].get("title") == "comedy"
    assert rs.status == "200 OK"
    rs = client.get('/genre?genre_id=1')
    assert rs.json.get("title") == "Action"
    assert rs.status == "200 OK"
    rs = client.get('/genre?genre_id=23')
    assert rs.json.get("error") == "Not found"
    assert rs.status == "404 NOT FOUND"


def test_genre_put(client, auth_admin):
    client.post('/genre', data=json.dumps(res.genre_5), content_type='application/json')
    rs = client.get('/genre')
    assert rs.json[0].get("title") == "comedy"
    rs = client.put('/genre', data=json.dumps(res.genre_6), content_type='application/json')
    assert rs.json.get("title") == res.genre_6.get("title")
    rs = client.put('/genre', data=json.dumps(res.genre_4), content_type='application/json')
    assert rs.status == "404 NOT FOUND"
    rs = client.put('/genre', data=json.dumps(res.genre_7), content_type='application/json')
    assert rs.status == "400 BAD REQUEST"
    rs = client.put('/genre', data=json.dumps(res.genre_8), content_type='application/json')
    assert rs.status == "400 BAD REQUEST"


def test_genre_delete(client, auth_admin):
    rs = client.delete('/genre?genre_id=1')
    assert rs.status == "404 NOT FOUND"
    rv = client.post('/genre', data=json.dumps(res.genre_1), content_type='application/json')
    rs = client.delete('/genre?genre_id=1')
    assert rs.status == "204 NO CONTENT"
    rs = client.delete('/genre?genre_id=1')
    assert rs.status == "404 NOT FOUND"


def test_director_post(client, auth_admin):
    rs = client.post('/director', data=json.dumps(res.director_1), content_type='application/json')
    assert rs.json.get("first_name") == "Katsu"
    rs = client.post('/director', data=json.dumps(res.director_4), content_type='application/json')
    assert rs.status == "400 BAD REQUEST"
    rs = client.post('/director', data=json.dumps(res.director_2), content_type='application/json')
    assert rs.status == "400 BAD REQUEST"
    rs = client.post('/director', data=json.dumps(res.director_5), content_type='application/json')
    assert rs.status == "400 BAD REQUEST"
    rs = client.post('/director', data=json.dumps(res.director_8), content_type='application/json')
    assert rs.status == "400 BAD REQUEST"


def test_director_get(client, auth_admin):
    client.post('/director', data=json.dumps(res.director_1), content_type='application/json')
    rs = client.get('/director')
    assert rs.json[0].get("first_name") == "unknown"
    assert rs.json[1].get("last_name") == "Shintaro"
    rs = client.get('/director?director_id=1')
    assert rs.json.get("first_name") == "unknown"
    rs = client.get('/director?director_id=10')
    assert rs.status == "404 NOT FOUND"


def test_director_put(client, auth_admin):
    client.post('/director', data=json.dumps(res.director_1), content_type='application/json')
    client.put('/director', data=json.dumps(res.director_3), content_type='application/json')
    rs = client.get('/director')
    assert rs.status == "200 OK"
    assert rs.json[1].get("first_name") == "Kastu-sin"
    rs = client.put('/director', data=json.dumps(res.director_6), content_type='application/json')
    assert rs.status == "403 FORBIDDEN"
    rs = client.put('/director', data=json.dumps(res.director_7), content_type='application/json')
    assert rs.status == "404 NOT FOUND"


def test_director_delete(client, auth_admin):
    rs = client.delete('/director?director_id=1')
    assert rs.status == "403 FORBIDDEN"
    client.post('/director', data=json.dumps(res.director_1), content_type='application/json')
    client.put('/director', data=json.dumps(res.director_3), content_type='application/json')
    rs = client.get('/director')
    assert rs.status == "200 OK"
    assert rs.json[1].get("first_name") == "Kastu-sin"
    rs = client.delete('/director?director_id=2')
    assert rs.status == "204 NO CONTENT"
    rs = client.delete('/director?director_id=41')
    assert rs.status == "404 NOT FOUND"


def test_role_get(client, auth_admin):
    rs = client.get('/role')
    assert rs.status == "200 OK"
    assert rs.json[0].get("title") == "Admin"
    assert rs.json[1].get("title") == "User"
    rs = client.get('/role?role_id=1')
    assert rs.json.get("title") == "Admin"


def test_role_post(client, auth_admin):
    rs = client.post('/role', data=json.dumps(res.role_1), content_type='application/json')
    assert rs.json.get("title") == res.role_1.get("title")
    rs = client.post('/role', data=json.dumps(res.role_2), content_type='application/json')
    assert rs.status == "400 BAD REQUEST"
    rs = client.post('/role', data=json.dumps(res.role_3), content_type='application/json')
    assert rs.status == "400 BAD REQUEST"


def test_role_put(client, auth_admin):
    rs = client.post('/role', data=json.dumps(res.role_1), content_type='application/json')
    assert rs.json.get("title") == res.role_1.get("title")
    client.put('/role', data=json.dumps(res.role_4), content_type='application/json')
    rs = client.get('/role?role_id=3')
    assert rs.json.get("title") == res.role_4.get("title")


def test_role_delete(client, auth_admin):
    client.post('/role', data=json.dumps(res.role_1), content_type='application/json')
    rs = client.get('/role?role_id=3')
    assert rs.json.get("title") == res.role_1.get("title")
    client.delete('/role?role_id=3')
    rs = client.get('/role?role_id=3')
    assert rs.status == "404 NOT FOUND"
    rs = client.delete('/role?role_id=2')
    assert rs.status == "403 FORBIDDEN"
    rs = client.delete('/role?role_id=1')
    assert rs.status == "403 FORBIDDEN"


def test_movie_get_all(client, auth_user, add_movie):

    rs = client.get('/movie')
    assert rs.json[0].get("title") == "Interstellar"
    for item in rs.json[0].get("genre"):
        assert item in [{'title': 'Drama'}, {'title': 'Adventure'}, {'title': 'Sci-fi'}]
    assert rs.json[0].get("rate") == 8
    assert rs.json[1].get("title") == "Mad Max"
    for item in rs.json[1].get("genre"):
        assert item in [{'title': 'Action'}, {'title': 'Adventure'}, {'title': 'Sci-fi'}]
    assert rs.json[1].get("rate") == 7


def test_movie_search(client, auth_user, add_movie):
    rs = client.get('/movie?search=ste')
    assert rs.json[0].get("title") == "Interstellar"
    rs = client.get('/movie?search=ax')
    assert rs.json[0].get("title") == "Mad Max"


def test_movie_filer(client, auth_user, add_movie):

    rs = client.get("/movie?genre_filter=Drama")
    assert rs.json[0].get("title") == "Interstellar"
    rs = client.get("/movie?genre_filter=Action")
    assert rs.json[0].get("title") == "Mad Max"


def test_movie_year_filter(client, auth_user, add_movie):
    rs = client.get('/movie?release_date_start_filter=1970&release_date_end_filter=1990')
    assert rs.json[0].get("title") == "Mad Max"
    rs = client.get('/movie?release_date_start_filter=1990&release_date_end_filter=2020')
    assert rs.json[0].get("title") == "Interstellar"
    rs = client.get('/movie?release_date_start_filter=1970&release_date_end_filter=2020')
    assert rs.json[0].get("title") == "Interstellar"
    assert rs.json[1].get("title") == "Mad Max"


def test_movie_director_filter(client, add_movie, auth_admin):
    rs = client.get('/movie?director_filter=Nolan')
    assert rs.json[0].get("title") == "Interstellar"
    rs = client.get('/movie?director_filter=Miller')
    assert rs.json[0].get("title") == "Mad Max"
    rs = client.get('/movie?director_filter=Smith')
    assert rs.json == []


def test_movie_ordering(client, auth_user, add_movie):
    rs = client.get('/movie?rate_order=True')
    assert rs.json[0].get("title") == "Mad Max"
    rs = client.get('/movie?date_order=True')
    assert rs.json[0].get("title") == "Mad Max"


def test_movie_put(client, add_movie, auth_user):
    client.put('/movie', data=json.dumps({"id": 1, "title": "new Interstellar"}),
               content_type='application/json')
    rs = client.get('/movie')
    assert rs.json[0].get("title") == "new Interstellar"
    rs = client.put('/movie', data=json.dumps({"id": 10, "title": "new Interstellar"}),
               content_type='application/json')
    assert rs.json.get("error") == "Not found"
    rs = client.put('/movie', data=json.dumps({"id": 1, "director": [{"id": 10}]}),
                    content_type='application/json')
    assert rs.json.get("error") == "Director not found"

    rs = client.put('/movie', data=json.dumps({"id": 1, "title": "n"}),
               content_type='application/json')
    assert rs.json.get("error") == "Data in user request is not valid"
    rs = client.put('/movie', data=json.dumps({"id": 1, "release_date": "1900-13-01"}),
                    content_type='application/json')
    assert rs.json.get("error") == "Data in user request is not valid"


def test_movies_put(client, add_movie_adm, auth_user):
    rs = client.put('/movie', data=json.dumps({"id": 1, "title": "new Interstellar"}),
               content_type='application/json')
    assert rs.json.get("error") == "Cant edit. This record added by another user"


def test_delete_movie(client, add_movie, auth_user):
    rs = client.delete('/movie?movie_id=1')
    assert rs.status == "204 NO CONTENT"
    rs = client.delete('/movie?movie_id=10')
    assert rs.status == "404 NOT FOUND"
    assert rs.json.get("error") == "Not found"


def test_movie_delete_user_restriction(client, add_movie_adm, auth_user):
    rs = client.delete('/movie?movie_id=1')
    assert rs.json.get("error") == "Cant delete. Record added by another user"


def test_user_login(client):
    rs = client.post('/login', data=json.dumps(res.user_admin),
                     content_type='application/json')
    assert rs.json.get("message") == "Authorized successfully"
    assert rs.status == "200 OK"

    rs = client.post('/login', data=json.dumps(res.invalid_user),
                     content_type='application/json')
    assert rs.json.get("error") == "Invalid email or password"
    assert rs.status == "404 NOT FOUND"


def test_logout(client, auth_admin):
    rs = client.get('/logout')
    assert rs.json.get("message") == "Logout Successfully"
    assert rs.status == "200 OK"


def test_signup(client):
    rs = client.post('/signup', data=(json.dumps(res.user)),
                     content_type='application/json')
    assert rs.json.get("message") == "User create"
    assert rs.status == "201 CREATED"
    client.get('/logout')
    client.post('/login', data=(json.dumps(res.user_admin)),
                content_type='application/json')
    rs = client.post('/signup', data=(json.dumps(res.user_admin)),
                     content_type='application/json')
    assert rs.json.get("error") == "Authorized user cant signup"
    assert rs.status == "400 BAD REQUEST"
    client.get('/logout')

    rs = client.post('/signup', data=(json.dumps(res.invalid_user_2)),
                     content_type='application/json')
    assert rs.json.get("error") == "User with this email already exists"
    assert rs.status == "400 BAD REQUEST"

    rs = client.post('/signup', data=(json.dumps(res.invalid_user_3)),
                     content_type='application/json')
    assert rs.json.get("error") == "Empty password"
    assert rs.status == "400 BAD REQUEST"



























































