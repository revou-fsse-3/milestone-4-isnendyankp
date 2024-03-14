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
    

# Add the login route with get method
@user_route.route('/login', methods=['GET'])
def get_login():
    return {'message': 'Login page'}, 200

# Add the login route with post method
@user_route.route('/login', methods=['POST'])
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
        

# Add the get users route with get method       
@user_route.route('/users', methods=['GET'])
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