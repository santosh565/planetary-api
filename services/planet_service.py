from model.planet_model import Planet,planets_schema,planet_schema
from flask import jsonify,request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_planets():
    planets = Planet.query.all()
    result = planets_schema.dump(planets)
    return jsonify(data=result)

def get_singlePlanet(id:int):
    planet_details = Planet.query.filter_by(planet_id=id).first()
    if planet_details:
        result = planet_schema.dump(planet_details)
        return jsonify(result)
    else:
        return jsonify(message=f"planet with id {id} does not exist"),404  


def planet_add():
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