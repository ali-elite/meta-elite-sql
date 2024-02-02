from utils import create_connection  # Ensure this returns a psycopg2 connection object for PostgreSQL


def add_database(database_name, description=''):
    """Add a new database record to the Databases table."""
    global cursor
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Databases (DatabaseName, Description) VALUES (%s, %s)",
                (database_name, description)
            )
            conn.commit()
            print("Database added successfully.")
        except Exception as e:
            print(f"An error occurred while adding the database: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to create database connection.")


def get_all_databases():
    """Retrieve all database records from the Databases table."""
    global cursor
    conn = create_connection()
    databases = []
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Databases")
            databases = cursor.fetchall()
        except Exception as e:
            print(f"An error occurred while fetching databases: {e}")
        finally:
            cursor.close()
            conn.close()
    return databases


def update_database(database_id, new_name=None, new_description=None):
    """Update a database record in the Databases table."""
    global cursor
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            if new_name and new_description:
                cursor.execute(
                    "UPDATE Databases SET DatabaseName = %s, Description = %s WHERE DatabaseID = %s",
                    (new_name, new_description, database_id)
                )
            elif new_name:
                cursor.execute(
                    "UPDATE Databases SET DatabaseName = %s WHERE DatabaseID = %s",
                    (new_name, database_id)
                )
            elif new_description:
                cursor.execute(
                    "UPDATE Databases SET Description = %s WHERE DatabaseID = %s",
                    (new_description, database_id)
                )
            conn.commit()
            print("Database updated successfully.")
        except Exception as e:
            print(f"An error occurred while updating the database: {e}")
        finally:
            cursor.close()
            conn.close()


def delete_database(database_id):
    """Delete a database record from the Databases table."""
    global cursor
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM Databases WHERE DatabaseID = %s",
                (database_id,)
            )
            conn.commit()
            print("Database deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting the database: {e}")
        finally:
            cursor.close()
            conn.close()

