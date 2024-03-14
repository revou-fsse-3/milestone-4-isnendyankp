from flask import Blueprint, request, jsonify
from app.models.user import User
from app.connectors.mysql_connector import engine
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies
import bcrypt

# Create the user routes blueprint
user_routes = Blueprint('user_routes', __name__)

# Add the register route
@user_routes.route('/register', methods=['GET'])
def get_register():
    return {'message': 'Register page'}, 200

# Add the register route
@user_routes.route('/register', methods=['POST'])
def register():
    
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()
    
    # Get the data from the request
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password_hash')
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)
    
    try:
        # Add the new user to the database
        session.add(new_user)
        session.commit()
        
        return {'message': 'User created successfully'}, 201
    
    except Exception as e:
        # If there is an error adding the user to the database
        session.rollback()
        return {'error': f'An error occurred: {e}'}, 500

# Add the login route
@user_routes.route('/login', methods=['GET'])
def get_login():
    return {'message': 'Login page'}, 200

# Add the login route
@user_routes.route('/login', methods=['POST'])
def login():
        
        # Connect to the database
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        
        # Get the data from the request
        data = request.json
        email = data.get('email')
        password = data.get('password_hash')
        
        # Get the user from the database
        user = session.query(User).filter_by(email=email).first()
        
        try:
            # Check if the user exists and the password is correct
            if user:
                if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                    access_token = create_access_token(identity=user.id)
                    return {'access_token': access_token}, 200
                else:
                    return {'message': 'Invalid password'}, 401
            else:
                return {'message': 'User not found'}, 404
        
        except Exception as e:
            return {'error': f'An error occurred: {e}'}, 500

# Add the get users route        
@user_routes.route('/users', methods=['GET'])
def get_users():
    
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    
    try:
        # Fetch all the users from the database
        users = session.query(User).all()
        
        # Convert the users to a dictionary
        user_data = [user.to_dict() for user in users]
        
        return {'users': user_data}, 200
    
    except Exception as e:
        # If there is an error getting the users
        return {'error': f'An error occurred: {e}'}, 500

# Add the get user by id route
@user_routes.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    
    try:
        # Fetch the user from the database
        user = session.query(User).filter_by(id=user_id).first()
        
        if user:
            # If the user exists
            return user.to_dict(), 200
        else:
            # If the user does not exist
            return {'message': 'User not found'}, 404
        
    except Exception as e:
        # If there is an error getting the user
        return {'error': f'An error occurred: {e}'}, 500

# Add the update user route    
@user_routes.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
        
        # Connect to the database
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()
        
        # Get the data from the request
        data = request.json
        username = data.get('username')
        email = data.get('email')
        
        try:
            # Fetch the user from the database
            user = session.query(User).filter_by(id=user_id).first()
            
            if user:
                # If the user exists
                user.username = username
                user.email = email
                session.commit()
                return {'message': 'User updated successfully'}, 200
            else:
                # If the user does not exist
                return {'message': 'User not found'}, 404
            
        except Exception as e:
            # If there is an error updating the user
            session.rollback()
            return {'error': f'An error occurred: {e}'}, 500

# for deleting a user by id        
@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
        
        # Connect to the database
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()
        
        try:
            # Fetch the user from the database
            user = session.query(User).filter_by(id=user_id).first()
            
            if user:
                # If the user exists
                session.delete(user)
                session.commit()
                return {'message': 'User deleted successfully'}, 200
            else:
                # If the user does not exist
                return {'message': 'User not found'}, 404
            
        except Exception as e:
            # If there is an error deleting the user
            session.rollback()
            return {'error': f'An error occurred: {e}'}, 500
        
# Logout route
@user_routes.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response