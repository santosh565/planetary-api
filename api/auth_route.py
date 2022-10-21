from flask import Blueprint
from services.auth_service import login_user,register_user
auth_route = Blueprint('auth_route', __name__)


@auth_route.route('/login',methods=['POST'])
def login():
    return login_user()

@auth_route.route('/register',methods=['POST'])
def register():
    return register_user()
   
        