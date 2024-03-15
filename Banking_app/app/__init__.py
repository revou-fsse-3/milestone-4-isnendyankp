from flask import Flask
from dotenv import load_dotenv
from app.controllers.user_management_route import user_routes
from app.controllers.account_management_route import account_routes
from app.controllers.transaction_management_route import transaction_routes


load_dotenv()

app = Flask(__name__)

#register blueprints
app.register_blueprint(user_routes)
app.register_blueprint(account_routes)
app.register_blueprint(transaction_routes)

@app.route('/')
def index():
    return 'Hello, World!'