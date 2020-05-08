import sqlite3 

def add_column(database_name, table_name, column_name, data_type):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    base_command = f"ALTER TABLE '{table_name}' ADD column '{column_name}' '{data_type}'"

    cursor.execute(base_command)
    connection.commit()
    connection.close()
    
add_column("usr-api.db", 'users', "avatar", "VARCHAR DEFAULT './static/images/avatars/av/avatar_00.png' ")