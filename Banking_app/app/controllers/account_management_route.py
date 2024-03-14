from flask import Blueprint, request, jsonify
from app.models.account import Account
from app.models.user import User
from sqlalchemy.orm import sessionmaker
from app.connectors.mysql_connector import engine

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