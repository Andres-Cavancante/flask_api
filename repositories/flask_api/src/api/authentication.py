from datetime import datetime, timezone, timedelta
import jwt
from src.exceptions import ApiException
from src.database_connect import database

SECRET_KEY = "your_secret_key"

class Auth:
    def __init__(self, refresh_token: str=None):
        self.__flask_database = database("flask_api")
        self.refresh_token = refresh_token

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
                ["refresh_token"],
                custom_filter=f"refresh_token = '{self.refresh_token}'"
            )
        except ApiException as error:
            return error.get_return_msg()
        return bool(response)

    def generate_access_token(self):
        expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        token = jwt.encode({"exp": expiration}, SECRET_KEY, algorithm="HS256")
        return token