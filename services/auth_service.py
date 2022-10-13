from model.user_model import User
from flask import jsonify,request
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def login_user():
    email = request.form['email']
    password = request.form['password']    
    test = User.query.filter_by(email=email,password= password).first()
    if test:
        token = create_access_token(identity=email,fresh=True)
        return jsonify(message='Login successful', token=token)
    else:
        return jsonify(message='Login failed'),401
    
def register_user():
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
    
