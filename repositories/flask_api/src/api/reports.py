from typing import Dict, Any, List
from datetime import date
# import uuid
# import hashlib
# import jwt
# from datetime import datetime, timezone, timedelta
from src.exceptions import ApiException
from src.database_connect import database

class Reports():
    def __init__(self, account_id: str) -> None:
        self.__flask_database = database("flask_api")
        self.__account_id = account_id

    def get_basic_data(self, payload: Dict[str, Any]):
        try:
            return self.__flask_database.query_columns(
                "basic",
                payload["columns"],
                payload["start_date"],
                payload["end_date"],
                custom_filter = f"account_id = '{self.__account_id}'"
            )
        except ApiException as error:
            return error.get_return_msg()
