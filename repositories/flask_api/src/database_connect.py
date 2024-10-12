import mysql.connector
import os
from typing import List, Tuple
from mysql.connector import Error, InterfaceError

class database:
    def __init__(self):
        self.config = {
            "host": os.getenv("DB_HOST", "mysql"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASS", "pass"),
            "database": os.getenv("MYSQL_DATABASE", "my_database")
        }
        self.database = os.getenv("DB_database", "sakila")

    def __interact(self, query: str, data: str = None): #REVISAR - mandar só o query
        response = None
        status_message = {
            "code": 503 #REVISAR
        }

        try:
            connection = mysql.connector.connect(**self.config)
            cursor = connection.cursor(buffered=True) #REVISAR - o que é o buffered?
            cursor.execute(f"USE {self.database};")
            cursor.execute(query) if not data else cursor.execute(query, data)
            if cursor.rowcount:
                response = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
        except InterfaceError as interface_error:
            status_message["message"] = interface_error.msg
            return status_message

        return response

    def __get_table_columns(self, table_name: str):
        query = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE"
                 f" TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table_name}';")
        return self.__interact(query)

    def __check_columns_availability(self, request_columns: List[str], table: str) -> List[str | None]:
        table_columns = self.__get_table_columns(table)
        if isinstance(table_columns, dict):
            return table_columns
        table_columns = [column[0] for column in table_columns]
        check = list(set(request_columns)-set(table_columns))
        if check:
            return {
                "code": 304, #REVISAR
                "message": f"Requested columns {check} do not exist on table '{table}'"
            }

    def query_film(self, columns: List[str]):
        check = self.__check_columns_availability(columns, "film")
        if check:
            return check
        query = f"SELECT {', '.join(columns)} FROM film"
        data = self.__interact(query)
        if isinstance(data, dict):
            return data
        return [dict(zip(columns, row)) for row in data]
