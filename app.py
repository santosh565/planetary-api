from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,String,Integer,Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required,create_access_token
import os

app = Flask(__name__)
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
    
    
@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury',
                     planet_type= 'Class D',
                     home_star = 'Sol',
                     mass= 3.258e23,
                     radius = 1516,
                     distance =35.98e6) 
    
    venus = Planet(planet_name='Venus',
                     planet_type= 'Class K',
                     home_star = 'Sol',
                     mass= 4.867e24,
                     radius = 3760,
                     distance =67.24e6) 
    
    earth = Planet(planet_name='Earth',
                     planet_type= 'Class M',
                     home_star = 'Sol',
                     mass= 5.972e24,
                     radius = 3959,
                     distance =92.96e6)   
    
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)
    
    
    test_user = User(first_name='first', last_name='last',
                     email='email@example.com',
                     password='password'
                     )
    
    db.session.add(test_user)
    db.session.commit()
    print('database seeded')  
    
@app.route('/super_simple')
def super_simple():
    return jsonify(message='hello from planetary api',data='json')  


@app.route('/')
def index():
    return 'hello world'


@app.route('/planets',methods=['GET'])
def planets():
    planets = Planet.query.all()
    result = planets_schema.dump(planets)
    return jsonify(result)


@app.route('/register',methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='Email exists'),409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name,email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully')
    
    
@app.route('/login',methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    
    test = User.query.filter_by(email=email,password= password).first()
    if test:
        token = create_access_token(identity=email,fresh=True)
        return jsonify(message='Login successful', token=token)
    else:
        return jsonify(message='Login failed'),401
     
   
@app.route('/planet_details/<int:id>',methods=['GET'])
def planet_details(id:int):
    planet_details = Planet.query.filter_by(planet_id=id).first()
    if planet_details:
        result = planet_schema.dump(planet_details)
        return jsonify(result)
    else:
        return jsonify(message=f"planet with id {id} does not exist"),404    
    
    
@app.route('/add_planet',methods=['POST'])
@jwt_required()
def add_planet():
    planet_name = request.form['planet_name']
    test = Planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify(message='There is already a planet with this name'),409
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])        
        new_planet = Planet(
            planet_name= planet_name,
            planet_type =planet_type,home_star= home_star,mass= mass,radius= radius,distance= distance)
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message = 'You added a new planet'),201    
    
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

if __name__ == '__main__':
    app.run(debug=True)

