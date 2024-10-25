from typing import List
from datetime import datetime, timezone, timedelta
import jwt
from src.exceptions import ApiException
from src.database_connect import database

SECRET_KEY = "flask_api"

class Auth:
    def __init__(self, refresh_token: str=None):
        self.__table_name = "authorization"
        self.__flask_database = database("flask_api")
        self.refresh_token = refresh_token
        self.accounts = []

    def __query_table(self, columns: List[str], custom_filter: str=None):
        try:
            return self.__flask_database.query_columns(
                self.__table_name,
                columns,
                custom_filter=custom_filter
            )
        except Exception as error:
            return ApiException(error.msg, 500).get_return_msg()

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
                ["refresh_token", "accounts"],
                custom_filter=f"refresh_token = '{self.refresh_token}'"
            )
        except ApiException as error:
            return error.get_return_msg()
        self.accounts = response["accounts"].split(",")
        return bool(response)

    def generate_access_token(self):
        expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        payload = {
            "exp": expiration,
            "accounts_with_access": self.accounts
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    def check_token_validity(self, access_token: str):
        token = access_token.replace("Bearer", "").strip()
        try:
            self.accounts = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]).get("accounts_with_access", [])
        except jwt.ExpiredSignatureError:
             raise ApiException("Token has expired", 401)
        except jwt.InvalidTokenError:
            raise ApiException("Invalid token", 401)
