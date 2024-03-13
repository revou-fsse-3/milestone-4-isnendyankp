from flask import Flask
from dotenv import load_dotenv
from app.controllers.user_management_route import user_route


load_dotenv()

app = Flask(__name__)

#register blueprints
app.register_blueprint(user_route)

@app.route('/')
def index():
    return 'Hello, World!'