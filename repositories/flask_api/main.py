from typing import Dict, Any, List
from flask import Flask, request, jsonify
from functools import wraps
from src.api.reports import Reports
from src.api.authentication import Auth
from src.exceptions import ApiException
from util.assert_values import assert_values
from util import util

def token_required(f):
    def wrapper(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        if not access_token:
            return jsonify({
                "message": "Access token is missing in Authorization",
                "code": 401
            }), 401

        try:
            auth = Auth(account_id=kwargs["account_id"])
            auth.check_token_validity(access_token)
        except ApiException as error:
            ret_mgs = error.get_return_msg()
            return jsonify(ret_mgs), ret_mgs["code"]

        return f(*args, **kwargs)

    return wrapper

def assert_payload(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            payload = util.get_request_body(request)
            payload = assert_values(f.__name__, payload)
        except ApiException as error:
            return error.get_return_msg(), error.code

        kwargs["payload"] = payload
        return f(*args, **kwargs)

    return wrapper

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World", 200

@app.route("/clients")
def retrieve_clients():
    pass

@app.route("/accounts")
def list_accounts():
    pass

@app.route("/authorize", methods=["GET"])
@assert_payload
def get_refresh_token(payload: Dict[str, Any]):
    authorization = Auth()
    if authorization.is_credential_valid(payload["client_id"], payload["client_secret"]):
        return jsonify({
            "refresh_token": authorization.refresh_token
        }), 200
    return jsonify({
        "message": "'client_id' or 'client_secret' provided are not registered"
        }), 400

@app.route("/reports/<account_id>", methods=["GET"])
@token_required
@assert_payload
def get_data(account_id, payload: Dict[str, Any]):
    data = Reports(account_id).get_basic_data(payload)
    return jsonify(data), 200 #REVISAR - se eu retornar o code no exception, ele vai fazer jsonfy no code

@app.route("/token", methods=["POST"])
@assert_payload
def issue_token(payload: Dict[str, Any]):
    authorization = Auth(refresh_token=payload["refresh_token"])
    if authorization.is_token_valid():
        return jsonify({"access_token": authorization.generate_access_token()}), 200
    return jsonify({"error": "Invalid refresh token"}), 401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) #REVISAR - o que é o debug?
