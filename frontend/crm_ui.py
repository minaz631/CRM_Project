import tkinter as tk
from tkinter import messagebox
import requests

# Function to add a customer
def add_customer():
    data = {
        "name": name_entry.get(),
        "company": company_entry.get(),
        "email": email_entry.get(),
        "telephone": telephone_entry.get(),
        "notes": notes_entry.get(),
        "follow_up_date": follow_up_entry.get()
    }

    try:
        response = requests.post("http://127.0.0.1:5000/customers", json=data)
        
        if response.status_code == 200:
            messagebox.showinfo("Success", "Customer added successfully!")
            clear_fields()
        else:
            messagebox.showerror("Error", "Failed to add customer")
    
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "Could not connect to server")

# Function to clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    company_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    telephone_entry.delete(0, tk.END)
    notes_entry.delete(0, tk.END)
    follow_up_entry.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("CRM System")

# Labels and input fields
tk.Label(root, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Company:").grid(row=1, column=0)
company_entry = tk.Entry(root)
company_entry.grid(row=1, column=1)

tk.Label(root, text="Email:").grid(row=2, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1)

tk.Label(root, text="Telephone:").grid(row=3, column=0)
telephone_entry = tk.Entry(root)
telephone_entry.grid(row=3, column=1)

tk.Label(root, text="Notes:").grid(row=4, column=0)
notes_entry = tk.Entry(root)
notes_entry.grid(row=4, column=1)

tk.Label(root, text="Follow-up Date (YYYY-MM-DD):").grid(row=5, column=0)
follow_up_entry = tk.Entry(root)
follow_up_entry.grid(row=5, column=1)

# Buttons
add_button = tk.Button(root, text="Add Customer", command=add_customer)
add_button.grid(row=6, column=0, columnspan=2, pady=10)

clear_button = tk.Button(root, text="Clear", command=clear_fields)
clear_button.grid(row=7, column=0, columnspan=2, pady=5)

# Run Tkinter event loop
root.mainloop()

