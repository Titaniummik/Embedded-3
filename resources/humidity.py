from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import Humidity
from mongoengine.errors import FieldDoesNotExist

class HumiditiesApi(Resource):
    def get(self):
        try:
            humidities = Humidity.objects().to_json()
            return Response(humidities, mimetype="application/json", status=200)
        except Exception:
            return "An unexpected error has occurred", 500

    @jwt_required()
    def post(self):  
        try:
            body = request.get_json()
            humidity = Humidity(**body, user=get_jwt_identity()).save()
            return {'id': str(humidity.id)}, 200
        
        except FieldDoesNotExist as e:
            return str(e), 400 
        except Exception:
            return "An unexpected error has occurred", 500

class HumidityApi(Resource):
    def get(self, id):
        try:
            humidity = Humidity.objects.get(id=id).to_json()
            return Response(humidity, mimetype="application/json", status=200)
        except Exception as e:
            return f"An Error Orccured: {e}", 500

    @jwt_required()
    def put(self, id):
        try:
            body = request.get_json()
            Humidity.objects.get(id=id).update(**body)
            return 'OK', 200
        
        except FieldDoesNotExist as e:
            return str(e), 400 
        except Exception:
            return "An unexpected error has occurred", 500
            
    @jwt_required()
    def delete(self, id):
        try:
            Humidity.objects.get(id=id).delete()
            return 'OK', 200
        except Exception:
            return "An unexpected error has occurred", 500