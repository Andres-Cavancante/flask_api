import mysql.connector
import os
from typing import List, Tuple
from mysql.connector import Error
from src.exceptions import ApiException

class database:
    def __init__(self, database_name: str):
        self.__config = {
            "host": os.getenv("DB_HOST", "mysql"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASS", "pass")
        }
        self.__database = database_name

    def __interact(self, query: str, data: str = None): #REVISAR - mandar só o query
        try:
            connection = mysql.connector.connect(**self.__config)
            cursor = connection.cursor(buffered=True) #REVISAR - o que é o buffered?
            cursor.execute(f"USE {self.__database};")
            cursor.execute(query) if not data else cursor.execute(query, data)
            response = cursor.fetchall() if cursor.rowcount else []
            connection.commit()
            cursor.close()
            connection.close()
        except Error as error:
            raise ApiException(error.msg, 500)

        return response

    def __get_table_columns(self, table_name: str) -> List[Tuple[str]]:
        query = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE"
                 f" TABLE_SCHEMA = '{self.__database}' AND TABLE_NAME = '{table_name}';")
        table_columns = self.__interact(query)
        return [column[0] for column in table_columns]

    def __check_columns_availability(self, request_columns: List[str], table: str) -> List[str | None]:
        table_columns = self.__get_table_columns(table)
        check = list(set(request_columns)-set(table_columns))
        if check:
            raise ApiException(f"Requested columns {check} do not exist on table '{table}'", 400)

    def query_all(self, table_name: str):
        table_columns = self.__get_table_columns(table_name)
        data = self.__interact(f"SELECT * FROM {table_name}")
        return [dict(zip(table_columns, row)) for row in data]

    def query_columns(self,
                    table_name: str,
                    columns: List[str],
                    start_date: str=None,
                    end_date: str=None,
                    custom_filter: str=None
                    ):
        self.__check_columns_availability(columns, table_name)
        if start_date and end_date:
            query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE date BETWEEN '{start_date}' AND '{end_date}'"
        else:
            query = f"SELECT {', '.join(columns)} FROM {table_name}"

        if custom_filter:
            query += " WHERE " if not "WHERE" in query else "AND"
            query += custom_filter

        data = self.__interact(query)

        if not data:
            return {}
        if len(data) == 1:
            return dict(zip(columns, data[0]))
        return [dict(zip(columns, row)) for row in data]
