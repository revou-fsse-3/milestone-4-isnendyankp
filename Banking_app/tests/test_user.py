import pytest
from datetime import datetime
from app.models.user import User
from app.models.account import Account

# Test User model attributes
def test_user_model_attributes():
    user = User(username='john_doe', email='john.doe@example.com', password_hash='password')
    assert user.username == 'john_doe'
    assert user.email == 'john.doe@example.com'
    assert user.password_hash == 'password'

# Test User model to_dict method
def test_user_to_dict_method():
    user = User(username='jane_smith', email='jane.smith@example.com', password_hash='password')
    user_dict = user.to_dict()
    assert user_dict['username'] == 'jane_smith'
    assert user_dict['email'] == 'jane.smith@example.com'

# Test User model __repr__ method
def test_user_repr_method():
    user = User(username='jane_smith', email='jane.smith@example.com', password_hash='password')
    assert repr(user) == '<User jane_smith>'
