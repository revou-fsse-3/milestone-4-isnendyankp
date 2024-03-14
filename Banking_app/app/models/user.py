from app.models.base import Base
from app.models.account import Account
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class User(Base):
    
    # Define the table name
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(255), unique=True)
    email = mapped_column(String(255), unique=True)
    password_hash = mapped_column(String(255))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    accounts = relationship('Account', back_populates='user')
    
    # Add a method to return the user as a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    # Add a method to return the user as a string
    def __repr__(self):
        return f'<User {self.username}>'