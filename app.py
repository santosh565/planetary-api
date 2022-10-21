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
   

if __name__ == '__main__':
    app.run(debug=True)

