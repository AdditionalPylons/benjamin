# Standardlib Imports
from contextlib import contextmanager
import datetime as dt
import os

# 3rd Party Module Imports
import pymysql

# Project File Imports
#

database = 'expense_history'
table = 'expenses'
table_columns = '(user_id, date, cost, item, location)'
today = str(dt.date.today())
this_week = f"DATE_SUB('{today}', INTERVAL 1 WEEK) AND '{today}'"
this_month = f"DATE_SUB('{today}', INTERVAL 1 MONTH) AND '{today}'"
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

@contextmanager
def connect():
    connection = pymysql.connect(
        host=instance1_host,
        port=instance1_port,
        user=instance1_user,
        password=instance1_password,
        database=database)
    try:
        yield connection
    finally:
        connection.commit()
        connection.close()

def query_all():
    with connect() as con:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM expenses")
            print(cursor.fetchall())

def query_all_today():
    with connect() as con:
        with con.cursor() as cursor:
            cursor.execute(f"SELECT * FROM expenses WHERE date = '{today}'")
            print(cursor.fetchall())

def query_spent(user_id, date=today):
    with connect() as con:
        with con.cursor() as cursor:
            cursor.execute(f"""SELECT SUM(cost) FROM expenses
                            WHERE user_id = {user_id} AND date = '{date}'""")
            result = cursor.fetchone()[0]
            if result is None:
                return 0
            else:
                return result

def query_spent_range(user_id, range):
    with connect() as con:
        with con.cursor() as cursor:
            cursor.execute(f"""SELECT SUM(cost) FROM expenses
                            WHERE user_id = {user_id} AND date BETWEEN {range}""")
            result = cursor.fetchone()[0]
            if result is None:
                return 0
            else:
                return result

def add_entry(user_id, date, cost, item='NULL', location='NULL'):
    with connect() as con:
        with con.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {table}{table_columns}
                 VALUES('{user_id}','{date}', {cost}, '{item}', '{location}')""")

# Returns a list for easy concat with parse_expense
def get_user_id(phone_number):
    with connect() as con:
        with con.cursor() as cursor:
            cursor.execute(f"SELECT user_id FROM users WHERE phone_number = '{phone_number}'")
            result = cursor.fetchone()
            if result is None:
                raise Exception(f"No user ID found for phone number '{phone_number}'")
            else:
                return list(result)

def get_budget(user_id,period):
    with connect() as con:
        with con.cursor() as cursor:
            cursor.execute(
                f"""SELECT {period}_budget FROM users WHERE user_id = {user_id}""")
            result = cursor.fetchone()[0]
            #arbitrarily large non-infinite number used for non-existent budget
            if result is None:
                return 100**100
            else:
                return result

def set_budget(user_id,period,amount):
    with connect() as con:
        with con.cursor() as cursor:
            cursor.execute(
                f"""UPDATE users SET {period}_budget = {amount}
                 WHERE user_id = {user_id}""")

def custom_query(query):
    with connect() as con:
        with con.cursor() as cursor:
            cursor.execute(query)
            print(cursor.fetchall())
