import json
import os
import jwt

from functools import wraps
from flask import Flask, jsonify, request, current_app
from flask_cors import CORS

from common.logger import Logger
from common.ret import Ret
from common import utilities

app = Flask(__name__)
CORS(app)

# Logger
logger = Logger().setup_logging()

SECRET_KEY = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        current_user = None
        try:
            # JWT is passed in the request header
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            # return 401 if token is not passed
            if not token:
                return jsonify({"message": "Token is missing !!"}), 401
            
            # decoding the payload to fetch the stored details
            # key_text = ""
            # cur_path = os.path.dirname(__file__)
            # public_key = f"{cur_path}\\Keys\\publicKey.pem"
            # with open(public_key, "r", encoding="UTF-8") as key_file:
            #     key_text = key_file.read()
            # key = "\n".join([l.lstrip() for l in key_text.split("\n")])
            # options = {
            #     "verify_exp": False,
            # }
            # data = jwt.decode(token, key, algorithms=["RS256"], options=options)

            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["RS256"], options={"verify_signature": False})

            if data is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401

            current_user = {"user_id": data['user_id']}
        except Exception as ex:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated

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
                # token should expire after 24 hrs
                user_info["token"] = jwt.encode(
                    {"user_id": user_info["id"], "user_name": user_info["username"]},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                ret.data = {
                    "message": "Successfully fetched auth token",
                    "data": user_info
                }
            except Exception as e:
                ret = utilities.catchEx(logger, err)
        else:
            return {
                "message": "Invalid username or password!",
            }, 500
    except Exception as err:
        ret = utilities.catchEx(logger, err)
    return json.dumps(ret.__dict__)

@app.route('/logout', methods=['GET'])
@token_required
def logout(current_user):
    ret: Ret = Ret()
    try:
        ret.data = "Logout success!"
    except Exception as err:
        ret = utilities.catchEx(logger, err)
    return json.dumps(ret.__dict__)

@app.route('/user-list', methods=["GET"])
@token_required
def user_list(current_user):
    ret: Ret = Ret()
    try:
        ret.data = utilities.load_json_file("user_list.json")
    except Exception as err:
        ret = utilities.catchEx(logger, err)
    return json.dumps(ret.__dict__)

@app.route('/role-list', methods=["GET"])
@token_required
def role_list(current_user):
    ret: Ret = Ret()
    try:
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