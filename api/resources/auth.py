from flask import request
from flask_jwt_extended import create_access_token
from database.models import User
from flask_restful import Resource
import datetime
from mongoengine.errors import FieldDoesNotExist, DoesNotExist, ValidationError

class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user =  User(**body)
            user.hash_password()
            user.save()
            return {'id': str(user.id)}, 200
        
        except FieldDoesNotExist as e:
            return str(e), 400 
        except ValidationError:
            return "Email already in use", 400
        except Exception:
            return "An unexpected error has occurred", 500
        
class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                return "Unauthorized", 401
    
            expires = datetime.timedelta(days=60)
            token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': token}, 200
        
        except DoesNotExist:
            return "Unauthorized", 401
        except Exception:
            return "An unexpected error has occurred", 500