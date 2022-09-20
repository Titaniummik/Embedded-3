from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import Light
from mongoengine.errors import FieldDoesNotExist

class LightsApi(Resource):
    def get(self):
        try:
            lights = Light.objects().to_json()
            return Response(lights, mimetype="application/json", status=200)
        except Exception:
            return "An unexpected error has occurred", 500

    @jwt_required()
    def post(self):  
        try:
            body = request.get_json()
            light = Light(**body, user=get_jwt_identity()).save()
            return {'id': str(light.id)}, 200
        
        except FieldDoesNotExist as e:
            return str(e), 400 
        except Exception:
            return "An unexpected error has occurred", 500

class LightApi(Resource):
    def get(self, id):
        try:
            light = Light.objects.get(id=id).to_json()
            return Response(light, mimetype="application/json", status=200)

        except Exception:
            return "An unexpected error has occurred", 500
        
    @jwt_required()
    def put(self, id):
        try:
            body = request.get_json()
            Light.objects.get(id=id).update(**body)
            return 'OK', 200
        
        except FieldDoesNotExist as e:
            return str(e), 400 
        except Exception:
            return "An unexpected error has occurred", 500

    @jwt_required()
    def delete(self, id):
        try:
            Light.objects.get(id=id).delete()
            return 'OK', 200

        except Exception:
            return "An unexpected error has occurred", 500
