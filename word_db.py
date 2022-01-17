import pymysql
import os
from dotenv import load_dotenv


load_dotenv()
HOST = os.getenv('HOST')
USER_DB = os.getenv('USER_DB')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')

connection = pymysql.connect(host=HOST, user=USER_DB, password=PASSWORD, database=DB_NAME,
                                 cursorclass=pymysql.cursors.DictCursor)


def get_category(*args, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"SELECT * FROM category")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
    return result

def get_goods( category, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"SELECT * FROM goods JOIN category ON category.id = goods.category_id WHERE category.name = '{category}'")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
    return result

def get_price_good(name ,connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"SELECT * FROM goods WHERE name = '{name}'")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
    return result