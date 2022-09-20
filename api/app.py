from flask import Flask
from database.db import initialize_db
from resources.routes import initialize_routes
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config.from_pyfile('settings.py')

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
    
initialize_db(app)
initialize_routes(api)

app.run(host='0.0.0.0', port=5000)