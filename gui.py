import tkinter as tk
from tkinter import ttk, messagebox

from models import databases, schemas, tables, columns, indexes, constraints, relationships


def populate_table_dropdown(dropdown):
    """Populate the table dropdown with available tables."""
    try:
        table_names = tables.get_all_table_names()
        dropdown['values'] = table_names
    except Exception as e:
        messagebox.showerror("Error", "Failed to load table names: " + str(e))


def populate_column_dropdown(column_combobox, table_name):
    try:
        if table_name:
            column_names = columns.get_column_names_for_table(table_name)  # Fetch column names for the selected table
            column_combobox['values'] = column_names
        else:
            column_combobox['values'] = []  # Clear the combobox if no table is selected
    except Exception as e:
        messagebox.showerror("Error", "Failed to load column names: " + str(e))


def create_main_window():
    root = tk.Tk()
    root.title("Meta-Elite SQL Manager")
    root.geometry("1024x550")  # Set the size of the window

    tab_control = ttk.Notebook(root)

    # Initialize tabs
    tab_databases = ttk.Frame(tab_control)
    tab_schemas = ttk.Frame(tab_control)
    tab_tables = ttk.Frame(tab_control)
    tab_columns = ttk.Frame(tab_control)
    tab_indexes = ttk.Frame(tab_control)
    tab_constraints = ttk.Frame(tab_control)
    tab_relationships = ttk.Frame(tab_control)

    # Add tabs to notebook
    tab_control.add(tab_databases, text='Databases')
    tab_control.add(tab_schemas, text='Schemas')
    tab_control.add(tab_tables, text='Tables')
    tab_control.add(tab_columns, text='Columns')
    tab_control.add(tab_indexes, text='Indexes')
    tab_control.add(tab_constraints, text='Constraints')
    tab_control.add(tab_relationships, text='Relationships')

    tab_control.pack(expand=1, fill="both")

    # Call functions to setup each tab
    setup_databases_tab(tab_databases)
    setup_schemas_tab(tab_schemas)
    setup_tables_tab(tab_tables)
    setup_columns_tab(tab_columns)
    setup_indexes_tab(tab_indexes)
    setup_constraints_tab(tab_constraints)
    setup_relationships_tab(tab_relationships)

    return root


def setup_databases_tab(tab):
    # Function to refresh the list of databases
    def refresh_databases_list():
        try:
            databases_list.delete(0, tk.END)  # Clear the existing list
            all_databases = databases.get_all_databases()
            for db in all_databases:
                databases_list.insert(tk.END, db[1])  # Assuming db[1] is the database name
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Function to add a database
    def add_database(database_name):
        if database_name:
            try:
                databases.add_database(database_name)  # Assumes an add_database function in your databases module
                database_name_entry.delete(0, tk.END)
                refresh_databases_list()
                messagebox.showinfo("Success", "Database added successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "Database name cannot be empty")

    # Frame for database operations
    operations_frame = ttk.Frame(tab)
    operations_frame.pack(side='left', fill='y', padx=10, pady=10)

    # Database Name Entry
    tk.Label(operations_frame, text="Database Name:").grid(row=0, column=0, padx=5, pady=5)
    database_name_entry = tk.Entry(operations_frame)
    database_name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Add Database Button
    add_database_button = tk.Button(operations_frame, text="Add Database",
                                    command=lambda: add_database(database_name_entry.get()))
    add_database_button.grid(row=1, column=0, columnspan=2, pady=5)

    # Refresh Databases Button
    refresh_databases_button = tk.Button(operations_frame, text="Refresh Databases", command=refresh_databases_list)
    refresh_databases_button.grid(row=2, column=0, columnspan=2, pady=5)

    # List of Databases
    databases_list_label = tk.Label(tab, text="Databases:")
    databases_list_label.pack(padx=5, pady=5)
    databases_list = tk.Listbox(tab, width=50)
    databases_list.pack(fill='both', expand=True, padx=5, pady=5)

    refresh_databases_list()


def setup_schemas_tab(tab_schemas):
    def populate_schema_database_dropdown():
        """Populate the database dropdown with available databases."""
        try:
            database_names = databases.get_all_databases()  # This function should return a list of database names
            database_dropdown['values'] = [db[1] for db in database_names]  # Assuming db[1] contains the database name
        except Exception as e:
            messagebox.showerror("Error", "Failed to load database names: " + str(e))

    def add_schema(database_name, schema_name):
        """Add a schema to the selected database."""
        if database_name and schema_name:
            try:
                schemas.add_schema(database_name, schema_name)
                schema_name_entry.delete(0, tk.END)
                refresh_schemas_list()
                messagebox.showinfo("Success", "Schema added successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "Both database and schema names are required")

    def refresh_schemas_list():
        """Refresh the list of schemas displayed in the GUI."""
        try:
            schemas_list.delete(0, tk.END)
            all_schemas = schemas.get_all_schemas()
            for schema in all_schemas:
                schemas_list.insert(tk.END,
                                    f"{schema[2]} on the database with id {schema[1]}")
        except Exception as e:
            messagebox.showerror("Error", "Failed to refresh schemas list: " + str(e))

    # Frame for Schema operations
    operations_frame = ttk.Frame(tab_schemas)
    operations_frame.pack(side='left', fill='y', padx=10, pady=10)

    # Database Dropdown for selecting which database the schema belongs to
    tk.Label(operations_frame, text="Select Database:").grid(row=0, column=0, padx=5, pady=5)
    database_dropdown = ttk.Combobox(operations_frame)
    database_dropdown.grid(row=0, column=1, padx=5, pady=5)

    # Schema Name Entry
    tk.Label(operations_frame, text="Schema Name:").grid(row=1, column=0, padx=5, pady=5)
    schema_name_entry = tk.Entry(operations_frame)
    schema_name_entry.grid(row=1, column=1, padx=5, pady=5)

    # Add Schema Button
    add_schema_button = tk.Button(operations_frame, text="Add Schema",
                                  command=lambda: add_schema(database_dropdown.get(), schema_name_entry.get()))
    add_schema_button.grid(row=2, column=0, columnspan=2, pady=5)

    # Refresh Schemas Button
    refresh_schemas_button = tk.Button(operations_frame, text="Refresh Schemas", command=refresh_schemas_list)
    refresh_schemas_button.grid(row=3, column=0, columnspan=2, pady=5)

    # List of Schemas
    schemas_list_label = tk.Label(tab_schemas, text="Schemas:")
    schemas_list_label.pack(padx=5, pady=5)
    schemas_list = tk.Listbox(tab_schemas, width=50)
    schemas_list.pack(fill='both', expand=True, padx=5, pady=5)

    populate_schema_database_dropdown()
    refresh_schemas_list()


def setup_tables_tab(tab_tables):
    def populate_schema_dropdown(dropdown):
        """Populate the schema dropdown with available schemas."""
        try:
            schema_names = schemas.get_all_schemas()  # Assumes a function returning a list of schema names
            dropdown['values'] = [schema[2] for schema in schema_names]  # Assuming schema[1] contains the schema name
        except Exception as e:
            messagebox.showerror("Error", "Failed to load schema names: " + str(e))

    def add_table(schema_name, table_name, description):
        """Add a table to the selected schema."""
        if schema_name and table_name:
            try:
                tables.add_table(schema_name, table_name, description)
                table_name_entry.delete(0, tk.END)
                description_entry.delete(0, tk.END)
                refresh_tables_list()
                messagebox.showinfo("Success", "Table added successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "Schema name and table name are required")

    def refresh_tables_list():
        """Refresh the list of tables displayed in the GUI."""
        try:
            tables_list.delete(0, tk.END)  # Clear the existing list
            all_tables = tables.get_all_tables()  # Assumes a function that returns all tables
            for table in all_tables:
                tables_list.insert(tk.END,
                                   f"{table[2]} - in schema with id {table[1]}")  # Adjust based on your data structure
        except Exception as e:
            messagebox.showerror("Error", "Failed to refresh tables list: " + str(e))

    # Frame for Table operations
    operations_frame = ttk.Frame(tab_tables)
    operations_frame.pack(side='left', fill='y', padx=10, pady=10)

    # Schema Dropdown for selecting which schema the table belongs to
    tk.Label(operations_frame, text="Select Schema:").grid(row=0, column=0, padx=5, pady=5)
    schema_dropdown = ttk.Combobox(operations_frame)
    schema_dropdown.grid(row=0, column=1, padx=5, pady=5)
    populate_schema_dropdown(schema_dropdown)

    # Table Name Entry
    tk.Label(operations_frame, text="Table Name:").grid(row=1, column=0, padx=5, pady=5)
    table_name_entry = tk.Entry(operations_frame)
    table_name_entry.grid(row=1, column=1, padx=5, pady=5)

    # Table Description Entry
    tk.Label(operations_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
    description_entry = tk.Entry(operations_frame)
    description_entry.grid(row=2, column=1, padx=5, pady=5)

    # Add Table Button
    add_table_button = tk.Button(operations_frame, text="Add Table",
                                 command=lambda: add_table(schema_dropdown.get(), table_name_entry.get(),
                                                           description_entry.get()))
    add_table_button.grid(row=3, column=0, columnspan=2, pady=5)

    # Refresh Tables Button
    refresh_tables_button = tk.Button(operations_frame, text="Refresh Tables", command=refresh_tables_list)
    refresh_tables_button.grid(row=4, column=0, columnspan=2, pady=5)

    # List of Tables
    tables_list_label = tk.Label(tab_tables, text="Tables:")
    tables_list_label.pack(padx=5, pady=5)
    tables_list = tk.Listbox(tab_tables, width=50)
    tables_list.pack(fill='both', expand=True, padx=5, pady=5)

    # Initial population of the schema dropdown and tables list
    populate_schema_dropdown(schema_dropdown)
    refresh_tables_list()


def setup_columns_tab(tab_columns):
    def add_column():
        selected_table = table_dropdown.get()
        column_name = column_name_entry.get()
        data_type = data_type_entry.get()
        is_nullable = is_nullable_var.get()
        default_value = default_value_entry.get()

        if not selected_table:
            messagebox.showwarning("Warning", "Please select a table")
            return

        try:
            table_id = tables.get_table_id(selected_table)
            columns.add_column(table_id, column_name, data_type, is_nullable, default_value)
            messagebox.showinfo("Success", "Column added successfully")
            column_name_entry.delete(0, tk.END)
            # Clear other fields similarly
            refresh_columns_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_columns_list():
        try:
            all_columns = columns.get_all_columns()
            columns_list.delete(0, tk.END)
            for col in all_columns:
                columns_list.insert(tk.END, f"table with id {col[1]} - {col[2]} ({col[3]})")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Frame for Column operations
    operations_frame = ttk.Frame(tab_columns)
    operations_frame.pack(side='top', fill='x', padx=10, pady=10)

    # Dropdown to select the table for the column
    tk.Label(operations_frame, text="Select Table:").grid(row=0, column=0, padx=5, pady=5)
    table_dropdown = ttk.Combobox(operations_frame, postcommand=lambda: populate_table_dropdown(table_dropdown))
    table_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    # Column Name Entry
    tk.Label(operations_frame, text="Column Name:").grid(row=1, column=0, padx=5, pady=5)
    column_name_entry = tk.Entry(operations_frame)
    column_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    # Data Type Entry
    tk.Label(operations_frame, text="Data Type:").grid(row=2, column=0, padx=5, pady=5)
    data_type_entry = tk.Entry(operations_frame)
    data_type_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    # Nullable Checkbox
    is_nullable_var = tk.BooleanVar()
    tk.Checkbutton(operations_frame, text="Is Nullable", variable=is_nullable_var).grid(row=3, column=1, padx=5, pady=5,
                                                                                        sticky="w")

    # Default Value Entry
    tk.Label(operations_frame, text="Default Value:").grid(row=4, column=0, padx=5, pady=5)
    default_value_entry = tk.Entry(operations_frame)
    default_value_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

    # Add Column Button
    add_column_button = tk.Button(operations_frame, text="Add Column",
                                  command=lambda: add_column())
    add_column_button.grid(row=5, column=0, columnspan=2, pady=5)

    # List of Columns
    columns_list_label = tk.Label(tab_columns, text="Columns:")
    columns_list_label.pack(padx=5, pady=5)
    columns_list = tk.Listbox(tab_columns, width=50, height=10)
    columns_list.pack(fill='both', expand=True, padx=5, pady=5)
    refresh_columns_list_button = tk.Button(tab_columns, text="Refresh Columns List",
                                            command=lambda: refresh_columns_list())
    refresh_columns_list_button.pack(pady=5)

    populate_table_dropdown(table_dropdown)
    refresh_columns_list()


def setup_indexes_tab(tab_indexes):
    # Function to refresh indexes list
    def refresh_indexes_list():
        try:
            indexes_list.delete(0, tk.END)  # Clear the list
            all_indexes = indexes.get_all_indexes()
            for idx in all_indexes:
                indexes_list.insert(tk.END,
                                    f"{idx[3]} on col-id {idx[2]} on table with id {idx[1]} with type ({idx[4]})")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load indexes: {e}")

    def add_index():
        selected_table = index_table_dropdown.get()
        selected_column = index_column_dropdown.get()
        index_type = index_type_dropdown.get()
        index_name = index_name_entry.get()

        # Validation
        if not all([selected_table, selected_column, index_type, index_name]):
            messagebox.showwarning("Warning", "Please enter all index details")
            return

        try:
            table_id = tables.get_table_id(selected_table)
            if table_id is None:
                messagebox.showerror("Error", f"No table found with name '{selected_table}'")
                return

            column_id = columns.get_column_id(selected_column, table_id)
            if column_id is None:
                messagebox.showerror("Error", f"No column found with name '{selected_column}' in the selected table")
                return

            # Add the index using a function in indexes.py
            indexes.add_index(table_id, column_id, index_name, index_type)
            messagebox.showinfo("Success", "Index added successfully")

            # Clear the form fields here, if necessary
            index_column_dropdown.set('')
            index_type_dropdown.set('')

            refresh_indexes_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Index Add Form
    add_index_frame = ttk.LabelFrame(tab_indexes, text="Add New Index")
    add_index_frame.pack(fill="x", padx=10, pady=5, expand=True)

    # Select Table Dropdown
    tk.Label(add_index_frame, text="Select Table:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    index_table_dropdown = ttk.Combobox(add_index_frame, state="readonly")
    index_table_dropdown.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
    index_table_dropdown.bind("<<ComboboxSelected>>",
                              lambda e: populate_column_dropdown(index_column_dropdown, index_table_dropdown.get()))

    # Select Column Dropdown
    tk.Label(add_index_frame, text="Column Name:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    index_column_dropdown = ttk.Combobox(add_index_frame, state="readonly")
    index_column_dropdown.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

    # Index Name Entry
    tk.Label(add_index_frame, text="Index Name:").grid(row=2, column=0, padx=5, pady=5)
    index_name_entry = tk.Entry(add_index_frame)
    index_name_entry.grid(row=2, column=1, padx=5, pady=5)

    # Index Type Dropdown
    index_types = ["PRIMARY KEY", "UNIQUE", "INDEX"]
    tk.Label(add_index_frame, text="Index Type:").grid(row=3, column=0, sticky="e", padx=5, pady=2)
    index_type_dropdown = ttk.Combobox(add_index_frame, values=index_types, state="readonly")
    index_type_dropdown.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

    # Add Index Button
    add_index_button = tk.Button(add_index_frame, text="Add Index", command=lambda: add_index())
    add_index_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Indexes List Display
    indexes_list_label = ttk.Label(tab_indexes, text="Existing Indexes:")
    indexes_list_label.pack(padx=5, pady=5)
    indexes_list = tk.Listbox(tab_indexes, height=10)
    indexes_list.pack(padx=10, pady=5, fill="x", expand=True)

    refresh_indexes_button = tk.Button(tab_indexes, text="Refresh Indexes", command=refresh_indexes_list)
    refresh_indexes_button.pack(pady=5)

    refresh_indexes_list()
    populate_table_dropdown(index_table_dropdown)


def setup_constraints_tab(tab_constraints):
    def refresh_constraints_list(constraints_listbox):
        constraints_listbox.delete(0, tk.END)  # Clear current items
        all_constraints = constraints.get_all_constraints()

        for constraint in all_constraints:
            constraints_listbox.insert(tk.END, f"table {constraint[1]} on col {constraint[2]} type({constraint[3]}) "
                                               f"with check condition [{constraint[6]}]")

    def add_constraint():
        table_name = table_dropdown.get()
        table_id = tables.get_table_id(table_name)
        column_name = column_dropdown.get()
        column_id = columns.get_column_id(column_name, table_id)
        constraint_type = constraint_type_dropdown.get()
        reference_table_name = ref_table_dropdown.get() or None
        reference_table_id = tables.get_table_id(reference_table_name)
        reference_column_name = ref_column_dropdown.get() or None
        reference_column_id = columns.get_column_id(reference_column_name, reference_table_id)
        check_condition = check_condition_entry.get() or None

        try:
            table_id = int(table_id) if table_id else None
            column_id = int(column_id) if column_id else None
            reference_table_id = int(reference_table_id) if reference_table_id else None
            reference_column_id = int(reference_column_id) if reference_column_id else None

            constraints.add_constraint(table_id, column_id, constraint_type, reference_table_id, reference_column_id,
                                       check_condition)
            messagebox.showinfo("Success", "Constraint added successfully")
            refresh_constraints_list(constraints_listbox)
        except ValueError:
            messagebox.showerror("Error", "Invalid number format in ID fields")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Frame for Adding New Constraint
    add_constraint_frame = ttk.LabelFrame(tab_constraints, text="Add New Constraint")
    add_constraint_frame.pack(fill="x", padx=5, pady=5, expand=True)

    # Dropdown for Selecting Table
    tk.Label(add_constraint_frame, text="Table:").grid(row=0, column=0, padx=5, pady=5)
    table_dropdown = ttk.Combobox(add_constraint_frame, state="readonly", width=50)
    table_dropdown.grid(row=0, column=1, padx=5, pady=5)
    populate_table_dropdown(table_dropdown)  # Function to populate dropdown with table names

    # Dropdown for Selecting Column (for column-specific constraints)
    tk.Label(add_constraint_frame, text="Column:").grid(row=1, column=0, padx=5, pady=5)
    column_dropdown = ttk.Combobox(add_constraint_frame, state="readonly", width=50)
    column_dropdown.grid(row=1, column=1, padx=5, pady=5)
    table_dropdown.bind("<<ComboboxSelected>>",
                        lambda e: populate_column_dropdown(column_dropdown, table_dropdown.get()))

    tk.Label(add_constraint_frame, text="Referenced Table:").grid(row=2, column=0, padx=5, pady=5)
    ref_table_dropdown = ttk.Combobox(add_constraint_frame, state="readonly", width=50)
    ref_table_dropdown.grid(row=2, column=1, padx=5, pady=5)
    populate_table_dropdown(ref_table_dropdown)  # Function to populate dropdown with table names

    # Dropdown for Selecting Column (for column-specific constraints)
    tk.Label(add_constraint_frame, text="Referenced Column:").grid(row=3, column=0, padx=5, pady=5)
    ref_column_dropdown = ttk.Combobox(add_constraint_frame, state="readonly", width=50)
    ref_column_dropdown.grid(row=3, column=1, padx=5, pady=5)
    ref_table_dropdown.bind("<<ComboboxSelected>>",
                            lambda e: populate_column_dropdown(ref_column_dropdown, ref_table_dropdown.get()))

    # Dropdown for Constraint Type
    tk.Label(add_constraint_frame, text="Constraint Type:").grid(row=4, column=0, padx=5, pady=5)
    constraint_type_dropdown = ttk.Combobox(add_constraint_frame, state="readonly",
                                            values=["PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "CHECK"], width=50)
    constraint_type_dropdown.grid(row=4, column=1, padx=5, pady=5)

    # Entry for CHECK condition (optional, shown if CHECK is selected)
    tk.Label(add_constraint_frame, text="CHECK Condition (optional):").grid(row=5, column=0, padx=5, pady=5)
    check_condition_entry = tk.Entry(add_constraint_frame, width=53)
    check_condition_entry.grid(row=5, column=1, padx=5, pady=5)

    # Button to Add Constraint
    add_constraint_button = ttk.Button(add_constraint_frame, text="Add Constraint", command=lambda: add_constraint())
    add_constraint_button.grid(row=6, column=0, columnspan=2, pady=5)

    # Listbox to Show Existing Constraints
    constraints_listbox = tk.Listbox(tab_constraints, height=15, width=100)
    constraints_listbox.pack(fill="both", padx=5, pady=5, expand=True)

    # Button to Refresh List of Constraints
    refresh_constraints_button = ttk.Button(tab_constraints, text="Refresh Constraints",
                                            command=lambda: refresh_constraints_list(constraints_listbox))
    refresh_constraints_button.pack(pady=5)

    # Initial Refresh of Constraints List
    refresh_constraints_list(constraints_listbox)


def setup_relationships_tab(tab_relationships):
    def add_relationship():
        # Fetch the selected values from the dropdowns
        fk_table_name = fk_table_dropdown.get()
        fk_column_name = fk_column_dropdown.get()
        pk_table_name = pk_table_dropdown.get()
        pk_column_name = pk_column_dropdown.get()
        type = relationship_degree_dropdown.get()
        join_table = join_table_dropdown.get()

        # Validate the input
        if not all([fk_table_name, fk_column_name, pk_table_name, pk_column_name]):
            messagebox.showerror("Error", "All fields must be selected")
            return

        try:
            # Convert table names to IDs
            fk_table_id = tables.get_table_id(fk_table_name)
            pk_table_id = tables.get_table_id(pk_table_name)
            join_table_id = tables.get_table_id(join_table) or None

            if fk_table_id is None or pk_table_id is None:
                raise ValueError("One of the tables could not be found.")

            # Convert column names to IDs for the selected tables
            fk_column_id = columns.get_column_id(fk_column_name, fk_table_id)
            pk_column_id = columns.get_column_id(pk_column_name, pk_table_id)

            if fk_column_id is None or pk_column_id is None:
                raise ValueError("One of the columns could not be found.")

            # Call the function to add a relationship
            relationships.add_relationship(fk_table_id, fk_column_id, pk_table_id, pk_column_id, type, join_table_id)
            messagebox.showinfo("Success", "Relationship added successfully")
            refresh_relationships(relationships_list)

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", "Failed to add relationship: " + str(e))

    def refresh_relationships(relationships_list):
        relationships_list.delete(0, tk.END)  # Clear current items
        all_relationships = relationships.get_all_relationships()  # Assume this fetches relationships
        for rel in all_relationships:
            relationships_list.insert(tk.END, f"Rel ID: {rel[0]}, FK Table: {rel[1]}, FK Column: {rel[2]},"
                                              f" PK Table: {rel[3]}, PK Column: {rel[4]} with type{rel[5]}"
                                              f" with Join Table {rel[6] or 'Unavailable'}")

    # Frame for Adding New Relationship
    add_relationship_frame = ttk.LabelFrame(tab_relationships, text="Add New Relationship")
    add_relationship_frame.pack(fill="x", padx=5, pady=5, expand=True)

    # Dropdown for Selecting Foreign Key Table
    tk.Label(add_relationship_frame, text="Foreign Key Table:").grid(row=0, column=0, padx=5, pady=5)
    fk_table_dropdown = ttk.Combobox(add_relationship_frame, state="readonly", width=50)
    fk_table_dropdown.grid(row=0, column=1, padx=5, pady=5)
    populate_table_dropdown(fk_table_dropdown)  # Function to populate dropdown with table names

    # Dropdown for Selecting Foreign Key Column
    tk.Label(add_relationship_frame, text="Foreign Key Column:").grid(row=1, column=0, padx=5, pady=5)
    fk_column_dropdown = ttk.Combobox(add_relationship_frame, state="readonly", width=50)
    fk_column_dropdown.grid(row=1, column=1, padx=5, pady=5)
    fk_table_dropdown.bind("<<ComboboxSelected>>",
                           lambda e: populate_column_dropdown(fk_column_dropdown, fk_table_dropdown.get()))

    # Dropdown for Selecting Primary Key Table
    tk.Label(add_relationship_frame, text="Primary Key Table:").grid(row=2, column=0, padx=5, pady=5)
    pk_table_dropdown = ttk.Combobox(add_relationship_frame, state="readonly", width=50)
    pk_table_dropdown.grid(row=2, column=1, padx=5, pady=5)
    populate_table_dropdown(pk_table_dropdown)  # Similar function to populate PK table dropdown

    # Dropdown for Selecting Primary Key Column
    tk.Label(add_relationship_frame, text="Primary Key Column:").grid(row=3, column=0, padx=5, pady=5)
    pk_column_dropdown = ttk.Combobox(add_relationship_frame, state="readonly", width=50)
    pk_column_dropdown.grid(row=3, column=1, padx=5, pady=5)
    pk_table_dropdown.bind("<<ComboboxSelected>>",
                           lambda e: populate_column_dropdown(pk_column_dropdown, pk_table_dropdown.get()))

    # Dropdown for Relationship Degree (Enum Choices)
    relationship_degree_choices = ['ONE_TO_ONE', 'ONE_TO_MANY', 'MANY_TO_MANY']
    tk.Label(add_relationship_frame, text="Relationship Degree:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    relationship_degree_dropdown = ttk.Combobox(add_relationship_frame, values=relationship_degree_choices, state="readonly")
    relationship_degree_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

    # Dropdown for Join Table (Optional, from existing tables)
    tk.Label(add_relationship_frame, text="Join Table (Optional):").grid(row=5, column=0, padx=5, pady=5, sticky="e")
    join_table_dropdown = ttk.Combobox(add_relationship_frame, state="readonly")
    join_table_dropdown.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
    populate_table_dropdown(join_table_dropdown)  # Reuse the function to populate with table names

    # Button to Add Relationship
    add_relationship_button = ttk.Button(add_relationship_frame, text="Add Relationship",
                                         command=lambda: add_relationship())
    add_relationship_button.grid(row=6, column=0, columnspan=2, pady=5)

    # Relationships List
    relationships_list_frame = ttk.Frame(tab_relationships)
    relationships_list_frame.pack(fill="both", expand=True, padx=10, pady=5)

    relationships_list = tk.Listbox(relationships_list_frame, height=10, width=100)
    relationships_list.pack(side="left", fill="both", expand=True)

    # Scrollbar for Relationships List
    scrollbar = ttk.Scrollbar(relationships_list_frame, orient="vertical", command=relationships_list.yview)
    scrollbar.pack(side="right", fill="y")
    relationships_list.config(yscrollcommand=scrollbar.set)

    # Button to Refresh Relationships List
    refresh_relationships_button = ttk.Button(tab_relationships, text="Refresh Relationships",
                                              command=lambda: refresh_relationships(relationships_list))
    refresh_relationships_button.pack(pady=5)

    # Initial load of relationships
    refresh_relationships(relationships_list)


if __name__ == "__main__":
    root = create_main_window()
    root.mainloop()
