import psycopg2

from utils import create_connection


def add_table(schema_name, table_name, description=''):
    """
    Adds a new table with the given name and description to the specified schema.
    Parameters:
    - schema_name: The name of the schema to which the table belongs.
    - table_name: The name of the table to be added.
    - description: A description for the table.
    """
    conn = create_connection()
    try:
        with conn.cursor() as cursor:
            # First, find the SchemaID based on the provided schema_name
            cursor.execute("SELECT SchemaID FROM Schemas WHERE SchemaName = %s", (schema_name,))
            schema_id = cursor.fetchone()
            if not schema_id:
                print(f"No schema found with name: {schema_name}")
                return

            # Insert the new table into the Tables table with the found SchemaID
            cursor.execute(
                "INSERT INTO Tables (SchemaID, TableName, Description) VALUES (%s, %s, %s)",
                (schema_id[0], table_name, description)
            )
            conn.commit()
            print(f"Table '{table_name}' added successfully to schema '{schema_name}'.")
    except psycopg2.Error as e:
        print(f"Error adding table: {e}")
    finally:
        if conn is not None:
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

def get_table_id(table_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TableID FROM Tables WHERE TableName = %s", (table_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return result[0]
    else:
        return None
