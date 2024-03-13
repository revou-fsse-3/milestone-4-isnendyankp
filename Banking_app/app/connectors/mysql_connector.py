from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

username = os.getenv('DATABASE_USERNAME')
password = os.getenv('DATABASE_PASSWORD')
host = os.getenv('DATABASE_URL')
database = os.getenv('DATABASE_NAME')


try:
    print(f"Connecting to the database: {host}")
    engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}/{database}")
    connection = engine.connect()
    Session = sessionmaker(connection)

    print("Connected to the database")

except Exception as e:
    print(f"Error connecting to the database: {e}")