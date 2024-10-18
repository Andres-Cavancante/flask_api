from typing import Dict, Any
from flask import Flask, request, jsonify
from functools import wraps
from src.api.reports import Reports
from src.api.authentication import Auth
from src.exceptions import ApiException
from util.assert_values import assert_values
from util import util

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
        }), 401

@app.route("/reports/<account_id>", methods=["GET"])
@assert_payload
def get_data(account_id, payload: Dict[str, Any]): #REVISAR - O account id chega aqui com o wrapper?
    data = Reports().get_basic_data(payload)
    return jsonify(data), 200 #REVISAR - se eu retornar o code no exception, ele vai fazer jsonfy no code

@app.route("/token", methods=["POST"])
@assert_payload
def issue_token(payload: Dict[str, Any]):
    authorization = Auth(payload["refresh_token"])
    if authorization.is_token_valid():
        return jsonify({"access_token": authorization.generate_access_token()}), 200
    return jsonify({"error": "Invalid refresh token"}), 401


# def token_required(f):
#     def wrapper(*args, **kwargs):
#         # Code to check token validity
#         token = request.headers.get('Authorization').split("Bearer ")[1]
        
#         if not token:
#             return jsonify({"error": "Token is missing"}), 401
        
#         try:
#             # Decode and validate token (for example, using JWT)
#             jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         except jwt.ExpiredSignatureError:
#             return jsonify({"error": "Token has expired"}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({"error": "Invalid token"}), 401

#         # Call the original function if token is valid
#         return f(*args, **kwargs)
    
#     return wrapper

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) #REVISAR - o que é o debug?
