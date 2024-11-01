import json
import jwt
import base64
from typing import List
from datetime import datetime, timezone, timedelta
from cryptography.fernet import Fernet
from src.exceptions import ApiException
from src.database_connect import database

SECRET_KEY = "flask_api"
CIPHER_KEY = base64.urlsafe_b64encode(b"___________flask__api___________")

class Auth:
    def __init__(self, refresh_token: str=None, account_id = None):
        self.__table_name = "authorization"
        self.__flask_database = database("flask_api")
        self.refresh_token = refresh_token
        self.account_id = account_id
        self.__client_hash = None

    def __query_table(self, columns: List[str], custom_filter: str=None):
        try:
            return self.__flask_database.query_columns(
                self.__table_name,
                columns,
                custom_filter=custom_filter
            )
        except Exception as error:
            return ApiException(str(error), 500).get_return_msg()

    def get_clients(self):
        return self.__query_table(
            ["refresh_token", "accounts"]
        )

    def is_credential_valid(self, client_id: str, client_secret: str):
        try:
            response = self.__flask_database.query_columns(
                "authorization",
                ["refresh_token"],
                custom_filter=f"client_id = '{client_id}' AND client_secret = '{client_secret}'"
            )
        except ApiException as error:
            return error.get_return_msg()

        refresh_token = response.get("refresh_token")
        if refresh_token:
            self.refresh_token = refresh_token
            return True
        return False

    def is_token_valid(self):
        try:
            response = self.__flask_database.query_columns(
                "authorization",
                ["client_id", "client_secret"],
                custom_filter=f"refresh_token = '{self.refresh_token}'"
            )
        except ApiException as error:
            return error.get_return_msg()

        concat_info = f"{response['client_id']}:{response['client_secret']}"
        self.__client_hash = Fernet(CIPHER_KEY).encrypt(concat_info.encode()).decode('utf-8')
        return bool(response)

    def generate_access_token(self):
        expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        payload = {
            "exp": expiration,
            "client_hash": self.__client_hash
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    def check_token_validity(self, access_token: str):
        token = access_token.replace("Bearer", "").strip()
        try:
            jwt_info = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            client_hash = jwt_info.get("client_hash")
            if not client_hash:
                raise ApiException("Token is invalid", 401)
            client_info = Fernet(CIPHER_KEY).decrypt(client_hash).decode().split(":")
            client_id = client_info[0]
            client_secret = client_info[1]
            response = self.__flask_database.query_columns( #REVISAR - isso aqui é usado várias vezes
                "authorization",
                ["accounts"],
                custom_filter=(
                    f"client_id = '{client_id}' "
                    f"AND client_secret = '{client_secret}' "
                    f"AND JSON_CONTAINS(accounts, '\"{self.account_id}\"')"
                )
            )
            if not response:
                raise ApiException((f"Token does not have access to account {self.account_id} or "
                                    "it may not exist"), 401)
        except jwt.ExpiredSignatureError:
             raise ApiException("Token has expired", 401)
        except jwt.InvalidTokenError:
            raise ApiException("Invalid token", 401)
