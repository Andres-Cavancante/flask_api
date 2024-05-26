import os
import mysql.connector
import csv

def __read_csv(file_name:str="marketing.csv"):
    data = []
    file_path = os.path.join(os.getcwd(), file_name)
    # file_path = r"C:\Users\burge\OneDrive\Área de Trabalho\Projetos\flask-api\repositories\mysql_database\marketing.csv"
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

mysql_config = {
    "host": os.getenv("DB_HOST", "mysql"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "pass"),
    "port": int(os.getenv("DB_PORT", 3306))
}

connection = mysql.connector.connect(**mysql_config)
cursor = connection.cursor()

data = __read_csv()

insert_query = ("INSERT INTO basic"
                    "(date,"
                    "campaignName,"
                    "campaignId,"
                    "category,"
                    "impressions,"
                    "clicks,"
                    "leads,"
                    "orders,"
                    "spend,"
                    "revenue)" 
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

cursor.execute(f"USE {os.getenv('DB_database', 'flask_api')};")
for item in data:
    elements = (item["c_date"],
                item["campaign_name"],
                item["campaign_id"],
                item["category"],
                item["impressions"],
                item["clicks"],
                item["leads"],
                item["orders"],
                item["mark_spent"],
                item["revenue"])
    cursor.execute(insert_query, elements)
    connection.commit()

cursor.close()
connection.close()
