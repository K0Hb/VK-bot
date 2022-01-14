import pymysql

host = 'localhost'
user = 'root'
password = '22081991'
db_name = 'VK_BOT'

connection = pymysql.connect(host=host, user=user, password=password, database=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)


def connect_to_database( connection=connection):
    with connection.cursor() as cursor:
        connection.ping()
        cursor.execute(f"SELECT * FROM category")
        # cursor.execute("SELECT VERSION()")
        result = cursor.fetchall()
        connection.commit()
        connection.close()
    return result

print(connect_to_database())