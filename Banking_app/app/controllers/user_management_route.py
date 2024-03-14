from app.models.user import User
from flask import Blueprint, request, jsonify
from app.connectors.mysql_connector import engine
from sqlalchemy.orm import sessionmaker

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