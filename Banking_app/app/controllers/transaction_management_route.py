from app.controllers.account_management_route import check_account_ownership
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transaction import Transaction
from app.models.account import Account
from app.connectors.mysql_connector import engine
from sqlalchemy.orm import sessionmaker

# Cr8 a blueprint
transaction_routes = Blueprint('transaction_routes', __name__)

# this function checks if the account has enough balance
def check_balance(account_id, amount, session):
    
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    account = session.query(Account).filter_by(id=account_id).first()
    
    try:
        # Check if the account has enough balance
        if account.balance >= amount:
            return True
        else:
            return False
        
    except Exception as e:
        return False

# this function transfers money between accounts
def transfer_money(from_account_id, to_account_id, amount, description, session):
    
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    
    # Get the from and to accounts
    from_account = session.query(Account).filter_by(id=from_account_id).first()
    to_account = session.query(Account).filter_by(id=to_account_id).first()
    
    try:
        # Update the balances
        from_account.balance -= amount
        to_account.balance += amount

        # Create a new transaction
        new_transaction = Transaction(from_account_id=from_account_id, to_account_id=to_account_id, amount=amount, type='transfer', description=description)

        # Add the new transaction to the database
        session.add(new_transaction)
        session.commit()

        return True
    
    except Exception as e:
        # If there is an error transferring the money
        session.rollback()
        return False

# Transfer money between accounts with the same user ID
@transaction_routes.route('/transaction', methods=['POST'])
@jwt_required()
def transfer():
        
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    user_id = get_jwt_identity()
    
    # Get the data from the request
    data = request.json
    from_account_id = data.get('from_account_id')
    to_account_id = data.get('to_account_id')
    amount = data.get('amount')
    description = data.get('description')
    
    # Check if the accounts belong to the user
    if check_account_ownership(from_account_id, user_id) and check_account_ownership(to_account_id, user_id):
        
        # Check if the from account has enough balance
        if check_balance(from_account_id, amount, session):

            try:
                # Transfer the money between accounts
                if transfer_money(from_account_id, to_account_id, amount, description, session):
                    return {'message': 'Money transferred successfully'}, 200
            except Exception as e:
               return jsonify({'error': str(e)}), 500
            
            # else:
                # return {'error': 'An error occurred while transferring money'}, 500
        
        else:
            return {'error': 'The from account does not have enough balance'}, 400
    
    else:
        return {'error': 'The accounts do not belong to the user'}, 400
    
    return {'error': 'error all'}, 500

# Withdrawal money from account
@transaction_routes.route('/transaction/withdrawal', methods=['POST'])
@jwt_required()
def withdrawal():
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    user_id = get_jwt_identity()

    # Get the data from the request
    data = request.json
    from_account_id = data.get('from_account_id')
    amount = data.get('amount')
    description = data.get('description')

    # Check if the account belongs to the user
    if not check_account_ownership(from_account_id, user_id):
        return {'error': 'The account does not belong to the user'}, 400

    # Check if the account has enough balance
    if not check_balance(from_account_id, amount, session):
        return {'error': 'The account does not have enough balance'}, 400

    try:
        # Get the account
        from_account = session.query(Account).filter_by(id=from_account_id).first()

        # Update the balance
        from_account.balance -= amount

        # Create a new transaction
        new_transaction = Transaction(from_account_id=from_account_id, to_account_id=None, amount=amount, type='withdrawal', description=description)  # Indicate withdrawal

        # Add the new transaction and commit 
        session.add(new_transaction)
        session.commit()

        return {'message': 'Money withdrawn successfully'}, 200

    except Exception as e:
        session.rollback()
        return {'error': f'An error occurred while withdrawing money: {e}'}, 500

# Deposit money to account with account ID and amount to deposit
@transaction_routes.route('/transaction/deposit', methods=['POST'])
@jwt_required()
def deposit():
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    user_id = get_jwt_identity()

    # Get the data from the request
    data = request.json
    to_account_id = data.get('to_account_id')
    amount = data.get('amount')
    description = data.get('description')

    # Check if the account belongs to the user
    if not check_account_ownership(to_account_id, user_id):
        return {'error': 'The account does not belong to the user'}, 400

    try:
        # Get the account
        to_account = session.query(Account).filter_by(id=to_account_id).first()

        # Update the balance
        to_account.balance += amount

        # Create a new transaction
        new_transaction = Transaction(from_account_id=None, to_account_id=to_account_id, amount=amount, type='deposit', description=description)  

        # Add the new transaction and commit 
        session.add(new_transaction)
        session.commit()

        return {'message': 'Money deposited successfully'}, 200

    except Exception as e:
        session.rollback()
        return {'error': f'An error occurred while depositing money: {e}'}, 500

# Get all transactions for the user ID that is logged in
@transaction_routes.route('/transaction', methods=['GET'])
@jwt_required()
def get_transactions():
        
    # Connect to the database
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    user_id = get_jwt_identity()
    
    try:
        # Fetch the transactions from the database
        transactions = session.query(Transaction).join(Account, Transaction.from_account_id == Account.id).filter(Account.user_id == user_id).all()
        return {'transactions': [transaction.to_dict() for transaction in transactions]}, 200
    
    except Exception as e:
        # If there is an error getting the transactions
        return {'error': f'An error occurred: {e}'}, 500
        
# Get transactions by account ID
@transaction_routes.route('/transaction/<int:account_id>', methods=['GET'])
@jwt_required()
def get_transactions_by_account(account_id):
            
            # Connect to the database
            connection = engine.connect()
            Session = sessionmaker(connection)
            session = Session()
            user_id = get_jwt_identity()
            
            # Check if the user owns the account
            if check_account_ownership(account_id, user_id):
                
                try:
                    # Fetch the transactions from the database
                    transactions = session.query(Transaction).filter_by(from_account_id=account_id).all()
                    return {'transactions': [transaction.to_dict() for transaction in transactions]}, 200
                
                except Exception as e:
                    # If there is an error getting the transactions
                    return {'error': f'An error occurred: {e}'}, 500
            
            else:
                return {'error': 'The account does not belong to the user'}, 400