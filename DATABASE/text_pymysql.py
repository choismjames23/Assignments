import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='jssd23!!',
    db='classicmodels',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
def get_customers():
    cursor = connection.cursor()

    sql = "SELECT * FROM customers"

    cursor.execute(sql)

    customers = cursor.fetchall()

    print("customers : " ,customers)

def add_customer():
    cursor = connection.cursor()
    name = "seungmin"
    family_name = "Choi"
    sql = f"INSERT INTO customers(customerNumber, customerName, contactLastName) VALUES({66666}, '{name}', '{family_name}')"
    cursor.execute(sql)
    connection.commit()
    cursor.close()

# add_customer()

def update_customer():
    cursor = connection.cursor()
    update_name = "update_seungmin"
    contact_LastName = "update_Choi"
    sql = f"UPDATE customers SET customerName='{update_name}',\
            contactLastName='{contact_LastName}' WHERE customerNumber=66666"
    cursor.execute(sql)
    connection.commit()
    cursor.close()

# update_customer()

def delete_customer():
    cursor = connection.cursor()
    sql = "DELETE FROM customers WHERE customerNumber = 10000"
    cursor.execute(sql)
    connection.commit()
    cursor.close()

delete_customer()