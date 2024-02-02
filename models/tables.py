from utils import create_connection


def add_table(table_name, description):
    conn = create_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Tables (TableName, Description) VALUES (%s, %s)"
    cursor.execute(query, (table_name, description))
    conn.commit()
    cursor.close()
    conn.close()


def get_all_tables():
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Tables"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records


def update_table(table_id, new_name, new_description):
    conn = create_connection()
    cursor = conn.cursor()
    query = "UPDATE Tables SET TableName = %s, Description = %s WHERE TableID = %s"
    cursor.execute(query, (new_name, new_description, table_id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_table(table_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = "DELETE FROM Tables WHERE TableID = %s"
    cursor.execute(query, (table_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_all_table_names():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TableName FROM Tables")  # Assuming your table has a 'TableName' column
    table_names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return table_names
