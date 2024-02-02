from utils import create_connection


def add_index(table_id, column_id, index_type):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Indexes (TableID, ColumnID, IndexType) VALUES (%s, %s, %s)",
                   (table_id, column_id, index_type))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_indexes():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Indexes")
    indexes = cursor.fetchall()
    cursor.close()
    conn.close()
    return indexes

def delete_index(index_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Indexes WHERE IndexID = %s", (index_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Add more functions as needed
