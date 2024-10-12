from typing import List
import uuid
import hashlib
import jwt
from datetime import datetime, timezone, timedelta
from src.database_connect import database

class Reports():
    def __init__(self, columns: List[str]) -> None:
        # if columns is None:
        #     return {"message": "Columns is None"}
        # if not isinstance(columns, list):
        #     return {"message": "Columns must be a list"}
        # if not columns:
        #     return {"message": "Columns can not be empty"}
        # if not all(isinstance(field, str) for field in columns): #REVISAR - all
        #     return {"message": "All columns must be of type string"} #REVISAR - criar uma classe/método de valicações (decorator?)
        self.columns = columns
        self.database = database()
        #  self.HASHKEY = "keytohash12345"

    def get_data(self,):
        return self.database.query_film(self.columns)

    # def hash_function(self, info: str):
    #      return hashlib.sha256(info.encode()).hexdigest()
         
    # def write_user(self, user_name: str, password: str):
    #         query = f"INSERT INTO users (appId, appPassword, clientSecret) VALUES (%s, %s, %s);"
    #         hs_pass = hashlib.sha256(password).hexdigest()
    #         client_secret = str(uuid.uuid4())
    #         hashed_secret = self.hash_function(client_secret)
    #         data = (user_name, hs_pass, hashed_secret)
    #         status, res = self.db.interact("SET", query, data)
    #         if status == "Success":
    #              return f"User {user_name} succesfully created. Client secret: {client_secret}", 200
    #         else:
    #              return res, 500
    
    # def generate_token(self, user: str, password: str):
    #     query = f"SELECT appId, appPassword, clientSecret FROM users WHERE appId = '{user}';"
    #     status, secrets = self.db.interact("GET", query)
    #     if status == "Success":
    #         exists = False
    #         for item in secrets:
    #             if item[0] == user and item[1] == self.hash_function(password):
    #                  exists = True
    #     if exists:
    #         return jwt.encode({"clientSecret": item[2], "exp": datetime.now(timezone.utc) + timedelta(minutes=15)}, self.HASHKEY, algorithm='HS256')
    #     else:
    #         return "User not found"
        
    # def check_token(self, token: str):
    #         try:
    #             data = jwt.decode(token.replace("Bearer ", ""), self.HASHKEY, algorithms=['HS256'])
    #         except:
    #             return {"message": "Token is invalid"}
            
    #         if datetime.now(timezone.utc).timestamp() > data["exp"]:
    #              return {"message": "Token expired"}
            
    #         else:
    #             # query = f"SELECT appId, appPassword, clientSecret FROM users WHERE appId = '{self.hash_function(data["clientSecret"])}';"
    #             # code, info = self.db.interact("GET", query, data)
    #             return self.hash_function(data["clientSecret"])
