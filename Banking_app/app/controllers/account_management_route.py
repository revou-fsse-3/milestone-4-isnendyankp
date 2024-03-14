from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.account import Account
from app.models.user import User
from app.connectors.mysql_connector import engine
from sqlalchemy.orm import sessionmaker

# Create the account routes blueprint
account_routes = Blueprint('account_routes', __name__)

# Helper function to get the user's accounts
def check_account_ownership(account_id, user_id):
    
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    account = session.query(Account).filter_by(id=account_id).first()
    
    try:
        # Check if the account belongs to the user
        if account.user_id == user_id:
            return True
        else:
            return False
        
    except Exception as e:
        return False
    
# Create new account for user 
@account_routes.route('/account', methods=['POST'])
@jwt_required()
def create_account():
    
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    user_id = get_jwt_identity()
    
    # Get the data from the request
    data = request.json
    account_type = data.get('account_type')
    account_number = data.get('account_number')
    balance = data.get('balance')
    
    # Create a new account
    new_account = Account(user_id=user_id, account_type=account_type, account_number=account_number, balance=balance)
    
    try:
        # Add the new account to the database
        session.add(new_account)
        session.commit()
        return {'message': 'Account created successfully'}, 201
    
    except Exception as e:
        # If there is an error adding the account to the database
        session.rollback()
        return {'error': f'An error occurred: {e}'}, 500