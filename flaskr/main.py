from resuoreses import api
from flaskr import app


api.init_app(app)
app.run(debug=True)