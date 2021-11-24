
from flaskr import create_app
from resuoreses import api
from flaskr.model import init_db
from flaskr.utils import AppConfig

app = create_app(AppConfig)
api.init_app(app)
with app.app_context():
    init_db()


if __name__ == '__main__':
    app.run()
