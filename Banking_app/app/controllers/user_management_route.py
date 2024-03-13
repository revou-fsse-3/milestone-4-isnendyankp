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

