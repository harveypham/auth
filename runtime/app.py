import os
import boto3
from chalice import Chalice
from runtime.chalicelib.resources import UserDB
from runtime.chalicelib.handlers import Users


def get_user_controller():
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ.get('USER_TABLE_NAME', '')
    user_db = UserDB(dynamodb, table_name)
    return Users(user_db)

app = Chalice(app_name='auth')
users = get_user_controller()

@app.route('/register', methods=['POST'])
def create_user():
    request = app.current_request.json_body
    users.register_user(*request)

@app.route("/login", methods=["POST"])
def login_user():
    request = app.current_request.json_body
    return users.authenticate(*request)

@app.route("/verify", method=["GET"])
def user_email_from_token():
    app.current_request.headers.get("Authorization")
    return users.verify_token(app.current_request.headers.get("Authorization"))