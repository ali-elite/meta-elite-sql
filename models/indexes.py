from utils import create_connection


def add_index(table_id, column_id, index_name, index_type):
    conn = create_connection()
    cursor = conn.cursor()

    if index_type == "PRIMARY KEY":
        index_type = "PRIMARY"

    try:
        # SQL command to insert a new index record
        query = """
        INSERT INTO Indexes (TableID, ColumnID,IndexName, IndexType)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (table_id, column_id, index_name, index_type))
        conn.commit()

    except Exception as e:
        raise e

    finally:
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
