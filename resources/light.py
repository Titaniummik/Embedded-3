from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from database.models import Light
from werkzeug.exceptions import HTTPException, Forbidden


class LightsApi(Resource):
    def get(self):
        try:
            lights = Light.objects().to_json()
            return Response(lights, mimetype="application/json", status=200)
        
        except HTTPException as e:
            return e
        except Exception as e:
            return f"An Error Orccured: {e}", 500

    @jwt_required()
    def post(self):  
        try:
            body = request.get_json()
            light = Light(**body).save()
        
            return {'id': str(light.id)}, 200
        except Forbidden as e:
            return e
        except HTTPException as e:
            return e
        except Exception as e:
            return f"An Error Orccured: {e}", 500

class LightApi(Resource):
    def get(self, id):
        try:
            light = Light.objects.get(id=id).to_json()
            return Response(light, mimetype="application/json", status=200)

        except HTTPException as e:
            return e
        except Exception as e:
            return f"An Error Orccured: {e}", 500


    @jwt_required()
    def put(self, id):
        try:
            body = request.get_json()
            Light.objects.get(id=id).update(**body)
            return 'OK', 200
        except Forbidden as e:
            return e
        except HTTPException as e:
            return e
        except Exception as e:
            return f"An Error Orccured: {e}", 500

            
    @jwt_required()
    def delete(self, id):
        try:
            Light.objects.get(id=id).delete()
            return 'OK', 200
        except Forbidden as e:
            return e
        except HTTPException as e:
            return e
        except Exception as e:
            return f"An Error Orccured: {e}", 500
