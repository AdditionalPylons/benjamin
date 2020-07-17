# Standardlib Imports
import datetime
import os

# 3rd Party Module Imports
import pymysql

# Project File Imports
#

database = 'expense_history'
table = 'expenses'
table_columns = '(user_id, date, cost, item, location)'
today = str(datetime.date.today())
instance1_host = os.environ.get('INSTANCE1_HOST')
instance1_port = int(os.environ.get('INSTANCE1_PORT'))
instance1_user = os.environ.get('INSTANCE1_USER')
instance1_password = os.environ.get('INSTANCE1_PASSWORD')

"""expenses table structure is as follows:

TABLE expenses (
transaction_id INTEGER NOT NULL AUTO_INCREMENT,
user_id INTEGER NOT NULL,
date DATE NOT NULL,
cost FLOAT NOT NULL,
item TEXT,
location TEXT,
PRIMARY KEY (transaction_id),
FOREIGN KEY (user_id) REFERENCES users(user_id)
)

"""

"""users table structure is as follows:

TABLE users (
user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
group_id INTEGER,
name TEXT NOT NULL,
phone_number VARCHAR(15) NOT NULL,
email VARCHAR(320) NOT NULL,
monthly_budget MEDIUMINT UNSIGNED,
weekly_budget MEDIUMINT UNSIGNED,
daily_budget MEDIUMINT UNSIGNED,
region VARCHAR(42) DEFAULT 'US/Eastern',
language VARCHAR(5) DEFAULT 'en_US',
local_currency VARCHAR(3) DEFAULT 'USD',
summary_email_day TINYINT CHECK (summary_email_day BETWEEN 1 AND 7) DEFAULT 1,
summary_email_time TIME CHECK (HOUR(summary_email_time) < 24) DEFAULT '8:00'
)

"""


def connect():
    connection = pymysql.connect(
        host=instance1_host, port=instance1_port, user=instance1_user, password=instance1_password, database=database)
    connection.close()


def query_all():
    connection = pymysql.connect(
        host=instance1_host, port=instance1_port, user=instance1_user, password=instance1_password, database=database)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    print(cursor.fetchall())
    connection.commit()
    connection.close()


def query_all_today():
    connection = pymysql.connect(
        host=instance1_host, port=instance1_port, user=instance1_user, password=instance1_password, database=database)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM expenses WHERE date = '{today}'")
    print(cursor.fetchall())
    connection.commit()
    connection.close()


def query_spent_today():
    connection = pymysql.connect(
        host=instance1_host, port=instance1_port, user=instance1_user, password=instance1_password, database=database)
    cursor = connection.cursor()
    cursor.execute(f"SELECT SUM(cost) FROM expenses WHERE date = '{today}'")
    result = cursor.fetchone()[0]
    if result is None:
        return 0
    else:
        return result
    connection.commit()
    connection.close()


def add_entry(user_id, date, cost, item='NULL', location='NULL'):
    connection = pymysql.connect(
        host=instance1_host, port=instance1_port, user=instance1_user, password=instance1_password, database=database)
    cursor = connection.cursor()
    cursor.execute(
        f"""INSERT INTO {table}{table_columns}
         VALUES('{user_id}','{date}', {cost}, '{item}', '{location}')""")
    connection.commit()
    connection.close()

# Returns a list for easy concat with parse_expense
def get_user_id(phone_number):
    connection = pymysql.connect(
        host=instance1_host, port=instance1_port, user=instance1_user, password=instance1_password, database=database)
    cursor = connection.cursor()
    cursor.execute(f"SELECT user_id FROM users WHERE phone_number = '{phone_number}'")
    result = cursor.fetchone()
    if result is None:
        raise Exception(f"No user ID found for phone number '{phone_number}'")
    else:
        return list(result)
    connection.commit()
    connection.close()


def custom_query(query):
    connection = pymysql.connect(
        host=instance1_host, port=instance1_port, user=instance1_user, password=instance1_password, database=database)
    cursor = connection.cursor()
    cursor.execute(query)
    print(cursor.fetchall())
    connection.commit()
    connection.close()
