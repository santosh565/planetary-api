from sqlalchemy import Column,String,Integer,Float
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String,unique=True)
    password = Column(String)
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','first_name','last_name','email','password')    
        
user_schema =   UserSchema()
users_schema = UserSchema(many=True)  