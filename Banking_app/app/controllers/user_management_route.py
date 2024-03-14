from app.models.user import User
from flask import Blueprint, request, jsonify
from app.connectors.mysql_connector import engine
from sqlalchemy.orm import sessionmaker
from app import bcrypt

# Create a blueprint
user_route = Blueprint('user_route', __name__)

# register with get method

@user_route.route('/register', methods=['GET'])
def register():
    return {'message': 'Register a new user'}, 200

# register with post method
@user_route.route('/register', methods=['POST'])
def register():

    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    # Get the request data
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password_hash')

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)

    # try and catch block

    try:
        # Add the new user to the database
        session.add(new_user)
        session.commit()

        # Return the new user
        return {'message': 'User created successfully'}, 201
    
    except Exception as e:
        # Rollback the session
        session.rollback()
        return {'error': f'An error occurred: {e}'}, 500
    

# Add the login route
@user_route.route('/login', methods=['GET'])
def get_login():
    return {'message': 'Login page'}, 200