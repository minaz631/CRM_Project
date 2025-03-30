import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv

# Database setup
def init_db():
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            notes TEXT,
            data_source TEXT,
            follow_up_action TEXT,
            follow_up_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_customer():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    notes = notes_entry.get()
    data_source = data_source_entry.get()
    follow_up_action = follow_up_entry.get()
    follow_up_date = follow_up_date_entry.get()
    
    if name and phone:
        conn = sqlite3.connect("crm.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, phone, email, notes, data_source, follow_up_action, follow_up_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (name, phone, email, notes, data_source, follow_up_action, follow_up_date))
        conn.commit()
        conn.close()
        refresh_table()
    else:
        messagebox.showwarning("Input Error", "Name and Phone are required!")

def delete_customer():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "No customer selected!")
        return
    customer_id = tree.item(selected_item, "values")[0]
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
    conn.commit()
    conn.close()
    refresh_table()

def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()
    conn.close()
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Phone", "Email", "Notes", "Data Source", "Follow-up Action", "Follow-up Date"])
        writer.writerows(data)
    messagebox.showinfo("Export Successful", "Data exported successfully!")

def import_from_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            cursor.execute("INSERT INTO customers (name, phone, email, notes, data_source, follow_up_action, follow_up_date) VALUES (?, ?, ?, ?, ?, ?, ?)", row[1:])
    conn.commit()
    conn.close()
    refresh_table()
    messagebox.showinfo("Import Successful", "Data imported successfully!")

def search_customer():
    search_query = search_entry.get()
    refresh_table(search_query)

def refresh_table(search_query=None):
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    if search_query:
        cursor.execute("SELECT * FROM customers WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR notes LIKE ? OR data_source LIKE ?", 
                       (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute("SELECT * FROM customers")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

# Initialize database
init_db()

# GUI Setup
root = tk.Tk()
root.title("CRM System")

# Input Fields
fields = ["Name", "Phone", "Email", "Notes", "Data Source", "Follow-up Action", "Follow-up Date"]
entries = []
for i, field in enumerate(fields):
    tk.Label(root, text=field).grid(row=i, column=0)
    entry = tk.Entry(root)
    entry.grid(row=i, column=1)
    entries.append(entry)

name_entry, phone_entry, email_entry, notes_entry, data_source_entry, follow_up_entry, follow_up_date_entry = entries

tk.Button(root, text="Add Customer", command=add_customer).grid(row=0, column=2)
tk.Button(root, text="Delete Customer", command=delete_customer).grid(row=1, column=2)

tk.Label(root, text="Search").grid(row=2, column=2)
search_entry = tk.Entry(root)
search_entry.grid(row=2, column=3)
tk.Button(root, text="Search", command=search_customer).grid(row=2, column=4)

tk.Button(root, text="Export to CSV", command=export_to_csv).grid(row=0, column=5)
tk.Button(root, text="Import from CSV", command=import_from_csv).grid(row=1, column=5)

# Table
columns = ("ID", "Name", "Phone", "Email", "Notes", "Data Source", "Follow-up Action", "Follow-up Date")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.grid(row=6, column=0, columnspan=8)

refresh_table()
root.mainloop()

