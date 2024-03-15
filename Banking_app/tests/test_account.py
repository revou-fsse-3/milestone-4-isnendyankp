import pytest
from app.models.account import Account


# this test checks if the account model has the correct attributes
def test_account_repr():
    account = Account(account_number='12345')
    assert repr(account) == '<Account 12345>'


