from flask import Blueprint
from services.planet_service import *
from flask_jwt_extended import jwt_required


planet_route = Blueprint('planet_route', __name__)


@planet_route.route('/planets',methods=['GET'])
@jwt_required()
def planets():
    return get_planets()


@planet_route.route('/planet_details/<int:id>',methods=['GET'])
def planet_details(id:int):
    return get_singlePlanet(id)


@planet_route.route('/add_planet',methods=['POST'])
@jwt_required()
def add_planet():
    return planet_add()
