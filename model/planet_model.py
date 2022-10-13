from sqlalchemy import Column,String,Integer,Float
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()




class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer,primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float) 
    
class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id','planet_name','planet_name','home_star','mass','radius','distance') 
        
planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)    