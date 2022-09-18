from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from database.models import Temperature
from mongoengine.errors import FieldDoesNotExist


class TemperaturesApi(Resource):
    def get(self):
        try:
            temperatures = Temperature.objects().to_json()
            return Response(temperatures, mimetype="application/json", status=200)
        except Exception:
            return "An unexpected error has occurred", 500

    @jwt_required()
    def post(self):  
        try:
            body = request.get_json()
            
            if 'celcius' in body and 'fahrenheit' in body:
                return "Both celcius and fahrenheit cannot be set", 400
            
            if 'celcius' in body:
                c = int(body.get("celcius"))
                f = (c * 1.8) + 32 
                body.pop("celcius")
            elif 'fahrenheit' in body:
                f = int(body.get("fahrenheit"))
                c = (f - 32)  / 1.8
                body.pop("fahrenheit")
                
            temperature = Temperature(**body, fahrenheit=f, celcius=c).save()
            return {'id': str(temperature.id)}, 200
        
        except FieldDoesNotExist as e:
            return str(e), 400 
        except Exception:
            return "An unexpected error has occurred", 500

class TemperatureApi(Resource):
    def get(self, id):
        try:
            temperature = Temperature.objects.get(id=id).to_json()
            return Response(temperature, mimetype="application/json", status=200)
        except Exception as e:
            return f"An Error Orccured: {e}", 500

    @jwt_required()
    def put(self, id):
        try:
            body = request.get_json()
            Temperature.objects.get(id=id).update(**body)
            return 'OK', 200
        
        except FieldDoesNotExist as e:
            return str(e), 400 
        except Exception:
            return "An unexpected error has occurred", 500
            
    @jwt_required()
    def delete(self, id):
        try:
            Temperature.objects.get(id=id).delete()
            return 'OK', 200
        except Exception:
            return "An unexpected error has occurred", 500