from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, DECIMAL, Column
from sqlalchemy.sql import func
from app.models.base import Base

class Account(Base):
    
    # Define the table name
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    account_type = Column(String(255))
    account_number = Column(String(255), unique=True)
    balance = Column(DECIMAL(10, 2), default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Add a relationship to the User model
    user = relationship('User', back_populates='accounts')
    
    # Add a method to return the account as a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'account_type': self.account_type,
            'account_number': self.account_number,
            'balance': str(self.balance),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    # Add a method to return the account as a string
    def __repr__(self):
        return f'<Account {self.account_number}>'