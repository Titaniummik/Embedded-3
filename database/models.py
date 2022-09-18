from .db import db
import mongoengine_goodjson as gj
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime

class User(gj.Document):
    password = db.StringField(required=True, min_length=4)
    email = db.EmailField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField()
    geopoint = db.GeoPointField()
    
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Temperature(gj.Document):
    celcius = db.IntField(required=True)
    fahrenheit = db.IntField(required=True)
    user = db.ReferenceField(User)
    timestamp = db.DateTimeField(default=datetime.utcnow)
    
class Humidity(gj.Document):
    percent = db.IntField(required=True)
    user = db.ReferenceField(User)
    timestamp = db.DateTimeField(default=datetime.utcnow)
    
class Light(gj.Document):
    value = db.IntField(required=True)
    user = db.ReferenceField(User)
    timestamp = db.DateTimeField(default=datetime.utcnow)