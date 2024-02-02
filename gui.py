import tkinter as tk
from tkinter import ttk, messagebox
from models import tables, columns, indexes


def add_table():
    table_name = table_name_entry.get()
    description = ""  # Update this if you have a description field
    try:
        tables.add_table(table_name, description)
        messagebox.showinfo("Success", "Table added successfully")
        table_name_entry.delete(0, tk.END)
        refresh_tables_list()  # Refresh the list of tables
    except Exception as e:
        messagebox.showerror("Error", str(e))


def refresh_tables_list():
    try:
        all_tables = tables.get_all_tables()
        tables_list.delete(0, tk.END)  # Clear existing items
        for table in all_tables:
            tables_list.insert(tk.END, table[1])  # Assuming table[1] is the table name
    except Exception as e:
        messagebox.showerror("Error", str(e))


def add_column():
    selected_table = table_dropdown.get()
    column_name = column_name_entry.get()
    data_type = data_type_entry.get()  # Assuming you have an entry field for data type
    is_nullable = is_nullable_var.get()  # Assuming you have a checkbox or similar for nullable
    default_value = default_value_entry.get()  # Assuming an entry field for default value

    if not selected_table:
        messagebox.showwarning("Warning", "Please select a table")
        return

    try:
        # Assuming get_table_id function exists in tables.py to get the table ID based on its name
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
        all_columns = columns.get_all_columns()  # Fetches all columns from the database
        columns_list.delete(0, tk.END)  # Clear the list before adding new items
        for col in all_columns:
            columns_list.insert(tk.END, f"{col[1]} - {col[2]} ({col[3]})")  # Format as needed
    except Exception as e:
        messagebox.showerror("Error", str(e))


def populate_table_dropdown():
    try:
        # Assuming get_all_table_names returns a list of table names
        table_names = tables.get_all_table_names()
        table_dropdown['values'] = table_names
    except Exception as e:
        messagebox.showerror("Error", "Failed to load table names: " + str(e))


# Initialize the main window
root = tk.Tk()
root.title("Meta-Elite SQL Manager")
root.geometry("1024x600")  # Set the size of the window

# Create the tab control
tab_control = ttk.Notebook(root)

tab_tables = ttk.Frame(tab_control)
tab_control.add(tab_tables, text='Tables')
tab_columns = ttk.Frame(tab_control)
tab_control.add(tab_columns, text='Columns')

# Add Table Frame with Left Side Scrollbar
add_table_frame = ttk.Frame(tab_tables)
add_table_frame.pack(fill='x', padx=10, pady=5)

# Add input fields to the add_table_frame
tk.Label(add_table_frame, text="Table Name").pack(side='left', padx=(0, 10))
table_name_entry = tk.Entry(add_table_frame)
table_name_entry.pack(side='left', expand=True, fill='y', padx=(0, 10))
add_table_button = tk.Button(add_table_frame, text="Add Table", command=add_table)
add_table_button.pack(side='left')

# Add Column Frame with Left Side Scrollbar
add_column_frame = ttk.Frame(tab_columns)
add_column_frame.pack(fill='both', expand=True, padx=10, pady=5)

# Add input fields to the add_column_frame
tk.Label(add_column_frame, text="Select Table:").pack(anchor='w', padx=10)
table_dropdown = ttk.Combobox(add_column_frame)
table_dropdown.pack(anchor='w', padx=10)

tk.Label(add_column_frame, text="Column Name:").pack(anchor='w', padx=10)
column_name_entry = tk.Entry(add_column_frame)
column_name_entry.pack(anchor='w', padx=10)

tk.Label(add_column_frame, text="Data Type:").pack(anchor='w', padx=10)
data_type_entry = tk.Entry(add_column_frame)
data_type_entry.pack(anchor='w', padx=10)

is_nullable_var = tk.BooleanVar()
tk.Checkbutton(add_column_frame, text="Is Nullable", variable=is_nullable_var).pack(anchor='w', padx=10)

tk.Label(add_column_frame, text="Default Value:").pack(anchor='w', padx=10)
default_value_entry = tk.Entry(add_column_frame)
default_value_entry.pack(anchor='w', padx=10)

# Add other widgets and buttons as needed

# Tables List Section in Tables Tab
tables_list_frame = ttk.Frame(tab_tables)
tables_list_frame.pack(fill='both', expand=True, padx=10, pady=5)

tables_list = tk.Listbox(tables_list_frame)
tables_list.pack(side='left', fill='both', expand=True)
tables_scrollbar = ttk.Scrollbar(tables_list_frame, orient='vertical', command=tables_list.yview)
tables_scrollbar.pack(side='right', fill='y')
tables_list.config(yscrollcommand=tables_scrollbar.set)

refresh_button = tk.Button(tab_tables, text="Refresh List", command=refresh_tables_list)
refresh_button.pack(pady=(0, 5))

refresh_columns_button = tk.Button(tab_columns, text="Refresh Columns", command=refresh_columns_list)
refresh_columns_button.pack(pady=(0, 5))

# Columns List Section
columns_list_frame = ttk.Frame(tab_columns)
columns_list_frame.pack(fill='both', expand=True, padx=10, pady=5)

columns_list = tk.Listbox(columns_list_frame)
columns_list.pack(side='left', fill='both', expand=True)
columns_scrollbar = ttk.Scrollbar(columns_list_frame, orient='vertical', command=columns_list.yview)
columns_scrollbar.pack(side='right', fill='y')
columns_list.config(yscrollcommand=columns_scrollbar.set)

tab_control.pack(expand=1, fill="both")
root.mainloop()
