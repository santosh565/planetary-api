from flask import Blueprint,jsonify

simple_route = Blueprint('simple_route', __name__)


@simple_route.route('/super_simple')
def super_simple():
    return jsonify(message='hello from planetary api',data='json')  