#Standardlib Imports
import datetime
import os

#3rd Party Module Imports
import pymysql

#Project File Imports
#

database = 'expense_history'
table = 'expenses'
table_columns = '(date, cost, item, location)'
today = str(datetime.date.today())
instance1 = os.environ.get('awsdb-instance1')
instance1_user = os.environ.get('awsdb-instance1_user')
instance1_password = os.environ.get('awsdb-instance1_password')

"""expenses table structure is as follows:

TABLE expenses (
id INTEGER PRIMARY KEY AUTO_INCREMENT,
date DATE NOT NULL,
cost FLOAT NOT NULL,
item TEXT,
location TEXT
)

"""
def connect():
    connection = pymysql.connect(instance1, instance1_user, instance1_password, database)
    connection.close()

def query_all():
    connection = pymysql.connect(instance1, instance1_user, instance1_password, database)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    print(cursor.fetchall())
    connection.commit()
    connection.close()

def query_all_today():
    connection = pymysql.connect(instance1, instance1_user, instance1_password, database)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM expenses WHERE date = '{today}'")
    print(cursor.fetchall())
    connection.commit()
    connection.close()

def query_spent_today():
    connection = pymysql.connect(instance1, instance1_user, instance1_password, database)
    cursor = connection.cursor()
    cursor.execute(f"SELECT SUM(cost) FROM expenses WHERE date = '{today}'")
    result = cursor.fetchone()[0]
    if result is None:
        return 0
    else:
        return result
    connection.commit()
    connection.close()

def add_entry(date,cost,item='NULL',location='NULL'):
    connection = pymysql.connect(instance1, instance1_user, instance1_password, database)
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {table}{table_columns} VALUES('{date}', {cost}, '{item}', '{location}')")
    connection.commit()
    connection.close()

def custom_query(query):
    connection = pymysql.connect(instance1, instance1_user, instance1_password, database)
    cursor = connection.cursor()
    cursor.execute(query)
    print(cursor.fetchall())
    connection.commit()
    connection.close()
