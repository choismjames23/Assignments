import mysql.connector
from faker import Faker
import random # 파이썬 기본 모듈

# (1) MYSQL 연결 설정
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='jssd23!!',
    database='testdatabase'
)

# (2) MYSQL 연결
cursor = db_connection.cursor()
faker = Faker()

for _ in range(100):
    username = faker.user_name()
    email = faker.email()

    sql = "INSERT INTO user(username, email) VALUES(%s, %s)"
    values = (username, email)
    #print(sql, values)
    cursor.execute(sql, values)

cursor.execute("SELECT user_id FROM user")
valid_user_id = [row[0] for row in cursor.fetchall()]

for _ in range(100):
    user_id = random.choice(valid_user_id)
    product_name = faker.word()
    quantity = random.randint(1,10)

    sql = "INSERT INTO orders(user_id, product_name, quantity) VALUES(%s, %s, %s)"
    values = (user_id, product_name, quantity)
    cursor.execute(sql, values)

db_connection.commit()
cursor.close()
db_connection.close()