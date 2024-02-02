from utils import create_connection


def add_relationship(foreign_key_table_id, foreign_key_column_id, primary_key_table_id, primary_key_column_id, type, join_table):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO Relationships (ForeignKeyTableID, ForeignKeyColumnID, PrimaryKeyTableID, PrimaryKeyColumnID, RelationshipDegree, JoinTableID) 
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query,
                       (foreign_key_table_id, foreign_key_column_id, primary_key_table_id, primary_key_column_id, type, join_table))
        conn.commit()
    except Exception as err:
        print("Failed to insert relationship: {}".format(err))
        # Optionally, re-raise or handle the error as appropriate for your application
    finally:
        cursor.close()
        conn.close()


def get_all_relationships():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Relationships")
        return cursor.fetchall()  # Returns a list of tuples
    except Exception as err:
        print("Failed to retrieve relationships: {}".format(err))
        return []  # Return an empty list in case of error
    finally:
        cursor.close()
        conn.close()


def update_relationship(relationship_id, new_foreign_key_table_id=None, new_foreign_key_column_id=None,
                        new_primary_key_table_id=None, new_primary_key_column_id=None):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        query = """
        UPDATE Relationships SET 
        ForeignKeyTableID = COALESCE(%s, ForeignKeyTableID), 
        ForeignKeyColumnID = COALESCE(%s, ForeignKeyColumnID), 
        PrimaryKeyTableID = COALESCE(%s, PrimaryKeyTableID), 
        PrimaryKeyColumnID = COALESCE(%s, PrimaryKeyColumnID)
        WHERE RelationshipID = %s;
        """
        cursor.execute(query, (
            new_foreign_key_table_id, new_foreign_key_column_id, new_primary_key_table_id, new_primary_key_column_id,
            relationship_id))
        conn.commit()
    except Exception as err:
        print("Failed to update relationship: {}".format(err))
    finally:
        cursor.close()
        conn.close()


def delete_relationship(relationship_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Relationships WHERE RelationshipID = %s", (relationship_id,))
        conn.commit()
    except Exception as err:
        print("Failed to delete relationship: {}".format(err))
    finally:
        cursor.close()
        conn.close()
