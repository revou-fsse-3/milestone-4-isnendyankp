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
    
# Create new account for user with POST Method
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
    
# Get all accounts for user with GET Method
@account_routes.route('/account', methods=['GET'])
@jwt_required()
def get_accounts():
    
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    user_id = get_jwt_identity()
    
    # Get the user's accounts
    user = session.query(User).filter_by(id=user_id).first()
    accounts = user.accounts
    
    #
    return jsonify([account.to_dict() for account in accounts])

# Get account by id with GET Method
@account_routes.route('/account/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id):
    
    # Get the user id from the JWT
    user_id = get_jwt_identity()
    
    # Check if the user owns the account
    if check_account_ownership(account_id, user_id):
        
        # Connect to the database
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        
        # Get the account by id
        account = session.query(Account).filter_by(id=account_id).first()
        
        # Return the account as a dictionary
        return jsonify(account.to_dict())
    else:
        return {'error': 'Unauthorized'}, 401
    
# Update account by id with PUT Method
@account_routes.route('/account/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
    
    # Get the user id from the JWT
    user_id = get_jwt_identity()
    
    # Check if the user owns the account
    if check_account_ownership(account_id, user_id):
        
        # Connect to the database
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()
        
        # Get the data from the request
        data = request.json
        account_type = data.get('account_type')
        account_number = data.get('account_number')
        balance = data.get('balance')
        
        # Get the account by id
        account = session.query(Account).filter_by(id=account_id).first()
        
        try:
            # Update the account
            account.account_type = account_type
            account.account_number = account_number
            account.balance = balance
            session.commit()
            return {'message': 'Account updated successfully'}, 200
        
        except Exception as e:
            # If there is an error updating the account
            session.rollback()
            return {'error': f'An error occurred: {e}'}, 500
    else:
        return {'error': 'Unauthorized'}, 401
    
# Delete account by id with DELETE Method 
@account_routes.route('/account/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    
    # Get the user id from the JWT
    user_id = get_jwt_identity()
    
    # Check if the user owns the account
    if check_account_ownership(account_id, user_id):
        connection = engine.connect()
        Session = sessionmaker(connection)
        session = Session()
        session.begin()
        
        # Get the account by id
        account = session.query(Account).filter_by(id=account_id).first()
        
        try:
            # Delete the account
            session.delete(account)
            session.commit()
            return {'message': 'Account deleted successfully'}, 200
        
        except Exception as e:
            # If there is an error deleting the account
            session.rollback()
            return {'error': f'An error occurred: {e}'}, 500
    else:
        return {'error': 'Unauthorized'}, 401