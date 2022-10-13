from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
import os

from api.simple_route import simple_route
from api.planets_route import planet_route
from api.auth_route import auth_route


app = Flask(__name__)

app.register_blueprint(simple_route)
app.register_blueprint(planet_route)
app.register_blueprint(auth_route)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] ='sectet-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('db_create successfully')
    
    
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('db_drop successfully')    
    
    
# @app.cli.command('db_seed')
# def db_seed():
#     mercury = Planet(planet_name='Mercury',
#                      planet_type= 'Class D',
#                      home_star = 'Sol',
#                      mass= 3.258e23,
#                      radius = 1516,
#                      distance =35.98e6) 
    
#     venus = Planet(planet_name='Venus',
#                      planet_type= 'Class K',
#                      home_star = 'Sol',
#                      mass= 4.867e24,
#                      radius = 3760,
#                      distance =67.24e6) 
    
#     earth = Planet(planet_name='Earth',
#                      planet_type= 'Class M',
#                      home_star = 'Sol',
#                      mass= 5.972e24,
#                      radius = 3959,
#                      distance =92.96e6)   
    
#     db.session.add(mercury)
#     db.session.add(venus)
#     db.session.add(earth)
    
    
#     test_user = User(first_name='first', last_name='last',
#                      email='email@example.com',
#                      password='password'
#                      )
    
#     db.session.add(test_user)
#     db.session.commit()
#     print('database seeded')  
    


if __name__ == '__main__':
    app.run(debug=True)

