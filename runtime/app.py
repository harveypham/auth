import os
import boto3
from chalice import Chalice
from chalicelib.resources import UserDB
from chalicelib.handlers import Users


def get_user_controller():
    endpoint = os.environ.get("ENDPOINT")
    dynamodb = boto3.resource('dynamodb') if not endpoint else boto3.resource('dynamodb', endpoint_url=endpoint)
    table_name = os.environ.get('USER_TABLE_NAME', "Users")
    user_db = UserDB(dynamodb, table_name)
    return Users(user_db)

app = Chalice(app_name='auth')
users = get_user_controller()

@app.route("/", methods=["GET"])
def doc():
    return {
        "name": "Auth service",
        "routes": {
            "/register": [{
                "method": "POST",
                "args": ["email", "password"],
                "description": "Register user",
                "success": {"code": 200}
            }],
            "/login": [{
                "method": "POST",
                "args": ["email", "password"],
                "description": "Login user",
                "success": {"code": 200, "data": ["email", "access_token"]}
            }],
            "/password": [{
                "method": "PUT",
                "headers": {"Authorization": "<access_token>"},
                "args": ["old_password", "new_password"],
                "description": "Change user password",
                "success": {"code": 200}
            }]
        }
    }

@app.route('/register', methods=['POST'])
def create_user():
    request = app.current_request.json_body
    users.register_user(**request)

@app.route("/login", methods=["POST"])
def login_user():
    request = app.current_request.json_body
    return users.authenticate(**request)

@app.route("/verify", methods=["GET"])
def user_email_from_token():
    app.current_request.headers.get("Authorization")
    return users.verify_token(app.current_request.headers.get("Authorization"))

@app.route("/password", methods=["PUT"])
def change_password():
    token = app.current_request.headers.get("Authorization")
    request = app.current_request.json_body

    claims = users.verify_token(token)
    return users.change_password(claims["sub"], **request)