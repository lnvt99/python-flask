import json
import os
import jwt

from flask import Flask, request
from flask_cors import CORS
from datetime import timedelta

from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt,
    create_access_token
)

from common.logger import Logger
from common.ret import Ret
from common import utilities

app = Flask(__name__)
CORS(app)

# Logger
logger = Logger().setup_logging()

SECRET_KEY = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = SECRET_KEY
ACCESS_EXPIRES = timedelta(minutes=15)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

jwt = JWTManager(app)

BLOCKLIST = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@app.route('/', methods=["GET"])
def hello_world():
    ret: Ret = Ret()
    try:
        ret.data = {"response":"Hello world!"}
    except Exception as err:
        ret = utilities.catchEx(logger, err)
    return json.dumps(ret.__dict__)

@app.route('/login', methods=["POST"])
def login():
    ret: Ret = Ret()
    try:
        data_request = request.json
        if not data_request:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        user_list = utilities.load_json_file("user_list.json")
        user_info = next(item for item in user_list['userList'] if item["username"] == data_request['username'])
        if user_info:
            try:
                ret.data = {
                    'access_token': create_access_token(identity=user_info)
                }
                return json.dumps(ret.__dict__)
            except Exception as e:
                ret = utilities.catchEx(logger, err)
        else:
            return {
                "message": "Invalid username or password!",
            }, 500
    except Exception as err:
        ret = utilities.catchEx(logger, err)
    return json.dumps(ret.__dict__)

@app.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return {"message": "Successfully logged out"}, 200


@app.route('/user-list', methods=["GET"])
@jwt_required()
def user_list():
    ret: Ret = Ret()
    try:
        current_user = get_jwt()
        print(current_user)
        ret.data = utilities.load_json_file("user_list.json")
    except Exception as err:
        ret = utilities.catchEx(logger, err)
    return json.dumps(ret.__dict__)

@app.route('/role-list', methods=["GET"])
@jwt_required()
def role_list():
    ret: Ret = Ret()
    try:
        current_user = get_jwt()
        print(current_user)
        data = utilities.load_json_file("role_list.json")
        ret.data= data['roleList']
    except Exception as err:
        ret = utilities.catchEx(logger, err)
    return json.dumps(ret.__dict__)

if __name__ == "__main__":
    _logger = Logger()
    logger = _logger.setup_logging()

    # app.debug = True
    app.run(host="0.0.0.0", port=8000)