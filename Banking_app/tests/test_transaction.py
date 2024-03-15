from app.models.transaction import Transaction

def test_transaction_to_dict():
    # Create a test transaction object
    transaction = Transaction(id=1, from_account_id=1, to_account_id=2, amount=100.0, type='transfer', description='Test transfer')
    
    # Test the to_dict() method
    expected_dict = {
        'id': 1,
        'from_account_id': 1,
        'to_account_id': 2,
        'amount': '100.0',
        'type': 'transfer',
        'description': 'Test transfer',
        'created_at': transaction.created_at
    }
    assert transaction.to_dict() == expected_dict

def test_transaction_repr():
    # Create a test transaction object
    transaction = Transaction(id=1, from_account_id=1, to_account_id=2, amount=100.0, type='transfer', description='Test transfer')
    
    # Test the __repr__() method
    expected_repr = '<Transaction 1>'
    assert repr(transaction) == expected_repr
