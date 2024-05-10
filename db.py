import sqlite3

def is_database_empty():
    is_empty = True
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    tables = ['Players', 'Matches', 'PlayerStatsMatch']
    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        if count > 0:
            is_empty = False
    conn.close()
    return is_empty

def create_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with open('create_table.txt', 'r') as f:
        sql_create_table = f.read()
    stmt_list = sql_create_table.split('\n\n')
    for stmt in stmt_list:
        cur.execute(stmt)
        conn.commit()
    conn.close()
    if is_database_empty():
        insert_dummy_data()

def insert_dummy_data():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with open('insert_dummy_data.txt', 'r') as f:
        sql_insert_dummy_data = f.read()
    stmt_list = sql_insert_dummy_data.split('\n\n')
    for stmt in stmt_list:
        cur.execute(stmt)
        conn.commit()
    conn.close()

def print_table_schema(table_name=None):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = cur.fetchall()
    print(f"Schema of {table_name}:")
    for column in columns:
        print(f"{column[1]} - {column[2]}")

    conn.close()

def runSql(query):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
    conn.close()
    return result
