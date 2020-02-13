import sqlite3
import datetime


table = 'expenses'
table_columns = '(date, cost, item, location)'
today = str(datetime.date.today())


def query_all():
    connection = sqlite3.connect('expense_history.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    print(cursor.fetchall())
    connection.commit()
    connection.close()

def query_all_today():
    connection = sqlite3.connect('expense_history.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM expenses WHERE date = '{today}'")
    print(cursor.fetchall())
    connection.commit()
    connection.close()

def query_spent_today():
    connection = sqlite3.connect('expense_history.db')
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
    connection = sqlite3.connect('expense_history.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {table}{table_columns} VALUES('{date}', {cost}, '{item}', '{location}')")
    connection.commit()
    connection.close()

def custom_query(query):
    connection = sqlite3.connect('expense_history.db')
    cursor = connection.cursor()
    cursor.execute(query)
    print(cursor.fetchall())
    connection.commit()
    connection.close()
