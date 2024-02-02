from utils import create_connection


def add_constraint(table_id, column_id, constraint_type, reference_table_id=None, reference_column_id=None,
                   check_condition=None):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO Constraints (TableID, ColumnID, ConstraintType, ReferenceTableID, ReferenceColumnID, CheckCondition) 
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query,
                       (table_id, column_id, constraint_type, reference_table_id, reference_column_id, check_condition))
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_all_constraints():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Constraints")
        constraints = cursor.fetchall()
        return constraints
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_constraints_by_table(table_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Constraints WHERE TableID = %s", (table_id,))
        constraints = cursor.fetchall()
        return constraints
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

def update_constraint(constraint_id, new_table_id=None, new_column_id=None, new_constraint_type=None, new_reference_table_id=None, new_reference_column_id=None, new_check_condition=None):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        query = """
        UPDATE Constraints 
        SET TableID = COALESCE(%s, TableID), 
            ColumnID = COALESCE(%s, ColumnID), 
            ConstraintType = COALESCE(%s, ConstraintType), 
            ReferenceTableID = COALESCE(%s, ReferenceTableID), 
            ReferenceColumnID = COALESCE(%s, ReferenceColumnID), 
            CheckCondition = COALESCE(%s, CheckCondition)
        WHERE ConstraintID = %s;
        """
        cursor.execute(query, (new_table_id, new_column_id, new_constraint_type, new_reference_table_id, new_reference_column_id, new_check_condition, constraint_id))
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

def delete_constraint(constraint_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM Constraints WHERE ConstraintID = %s", (constraint_id,))
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()
