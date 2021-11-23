
from resuoreses import api
from flaskr import app
from flaskr import init_data

api.init_app(app)
init_data()
app.run()