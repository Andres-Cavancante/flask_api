import os
from time import sleep
import mysql.connector
from mysql.connector import Error
from generator import Generator

retries = 10
while retries > 0:
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "mysql"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASS", "pass"),
            database=os.getenv("MYSQL_DATABASE", "my_database")
        )
        if connection.is_connected():
            break
        print("Successfuly Connected")
    except Error as e:
        print(f"Error: {e}")
        retries -= 1
        print(f"Retrying 30 seconds... {retries} attempts left")
        sleep(30)

cursor = connection.cursor()
cursor.execute("USE flask_api;")

gen = Generator()

for item in gen.generate_campaign_data():
    cursor.execute((
        "INSERT INTO basic"
        "(date,"
        "campaign_name,"
        "campaign_id,"
        "adset_name,"
        "adset_id,"
        "ad_name,"
        "ad_id,"
        "clicks,"
        "cost,"
        "impressions,"
        "revenue)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    ), item)
    connection.commit()

for item in gen.generate_auth_data():
    cursor.execute((
        "INSERT INTO authorization"
        "(client_id,"
        "client_secret,"
        "refresh_token)"
        "VALUES (%s, %s, %s)"
        ), item)
    connection.commit()

cursor.close()
connection.close()
