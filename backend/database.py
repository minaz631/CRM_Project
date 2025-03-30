import sqlite3
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), "crm_database.sqlite")

def connect():
    """Connect to SQLite database and return the connection."""
    return sqlite3.connect(DB_PATH)

def create_tables():
    """Create Customers table if it doesn't exist."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT,
            email TEXT UNIQUE,
            telephone TEXT,
            notes TEXT,
            follow_up_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_customer(name, company, email, telephone, notes, follow_up_date):
    conn = connect()
    cursor = conn.cursor()

    # Check if the email already exists
    cursor.execute("SELECT * FROM Customers WHERE email = ?", (email,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        conn.close()
        return {"error": "Email already exists!"}  # Return error message

    # Insert new customer
    cursor.execute('''
        INSERT INTO Customers (name, company, email, telephone, notes, follow_up_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, company, email, telephone, notes, follow_up_date))

    conn.commit()
    conn.close()


def get_customers():
    """Retrieve all customers from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    conn.close()
    return customers

def update_customer(customer_id, name, company, email, telephone, notes, follow_up_date):
    """Update customer details."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Customers
        SET name = ?, company = ?, email = ?, telephone = ?, notes = ?, follow_up_date = ?
        WHERE id = ?
    ''', (name, company, email, telephone, notes, follow_up_date, customer_id))
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    """Delete a customer by ID."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Customers WHERE id = ?', (customer_id,))
    conn.commit()
    conn.close()

# Run this only once to create the database table
if __name__ == "__main__":
    create_tables()
    print("Database and table created successfully!")


