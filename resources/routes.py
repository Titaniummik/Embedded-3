from .auth import SignupApi, LoginApi
from .humidity import HumidityApi, HumiditiesApi
from .light import LightsApi, LightApi
from .temperature import TemperaturesApi, TemperatureApi

def initialize_routes(api):
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    
    api.add_resource(HumiditiesApi, '/api/humidity')
    api.add_resource(HumidityApi, '/api/humidity/<id>')
    
    api.add_resource(LightsApi, '/api/light')
    api.add_resource(LightApi, '/api/light/<id>')
    
    api.add_resource(TemperaturesApi, '/api/temperature')
    api.add_resource(TemperatureApi, '/api/temperature/<id>')