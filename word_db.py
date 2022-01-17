import pymysql

host = 'localhost'
user = 'root'
password = '22081991'
db_name = 'VK_BOT'

connection = pymysql.connect(host=host, user=user, password=password, database=db_name,
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

# print(get_goods('category1'))