import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('HOST')
USER_DB = os.getenv('USER_DB')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')

connection = pymysql.connect(host=HOST,
                             user=USER_DB,
                             password=PASSWORD,
                             database=DB_NAME,
                             cursorclass=pymysql.cursors.DictCursor)


def get_category(*args, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute("SELECT * FROM category")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
    return result


def get_goods(category, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(
            f"SELECT * FROM goods "
            f"JOIN category ON category.id = goods.category_id "
            f"WHERE category.name = '{category}'")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
    return result


def get_info_good(name, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"SELECT * FROM goods WHERE name = '{name}'")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
    return result[0]


def get_category_photo(category_name, connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(
            f"SELECT photo FROM category WHERE name = '{category_name}'")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
    return result[0]['photo']


def get_all_name(connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute("SELECT name FROM goods ")
        goods_name = cursor.fetchall()
        cursor.execute("SELECT name FROM category")
        category_name = cursor.fetchall()
        connection.commit()
        connection.close()
    return [name['name'] for name in goods_name + category_name]
