from utils import create_connection


def add_column(table_id, column_name, data_type, is_nullable, default_value):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Columns (TableID, ColumnName, DataType, IsNullable, DefaultValue) VALUES (%s, %s, %s, %s, %s)",
                   (table_id, column_name, data_type, is_nullable, default_value))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_columns():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Columns")
    columns = cursor.fetchall()
    cursor.close()
    conn.close()
    return columns

def update_column(column_id, new_name, new_data_type, new_is_nullable, new_default_value):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Columns SET ColumnName = %s, DataType = %s, IsNullable = %s, DefaultValue = %s WHERE ColumnID = %s",
                   (new_name, new_data_type, new_is_nullable, new_default_value, column_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_column(column_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Columns WHERE ColumnID = %s", (column_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Add more functions as needed
