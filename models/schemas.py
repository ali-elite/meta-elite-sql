import psycopg2

from utils import create_connection


def add_schema(database_name, schema_name, description=''):
    """
    Add a new schema to the specified database.
    Assumes a 'Databases' table exists with 'DatabaseName' as one of the columns.
    """
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # First, get the DatabaseID for the given database name
            cursor.execute("SELECT DatabaseID FROM Databases WHERE DatabaseName = %s", (database_name,))
            database_id = cursor.fetchone()
            if not database_id:
                print(f"No database found with name: {database_name}")
                return

            # Insert the new schema linked to the fetched DatabaseID
            cursor.execute(
                "INSERT INTO Schemas (DatabaseID, SchemaName, Description) VALUES (%s, %s, %s)",
                (database_id[0], schema_name, description)
            )
            conn.commit()
            print(f"Schema '{schema_name}' added successfully to database '{database_name}'.")
    except psycopg2.Error as e:
        print(f"Error adding schema: {e}")
    finally:
        conn.close()


def get_all_schemas():
    """Retrieve all schemas from the database."""
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Schemas")
            return cursor.fetchall()  # Returns a list of tuples
    except psycopg2.Error as e:
        print(f"Error fetching schemas: {e}")
        return []
    finally:
        conn.close()

