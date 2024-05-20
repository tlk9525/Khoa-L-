import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('user_bank.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    balance REAL DEFAULT 0.0
)
''')

# Function to add a new user
def add_user(username, password, balance=0.0):
    try:
        cursor.execute('''
        INSERT INTO users (username, password, balance)
        VALUES (?, ?, ?)
        ''', (username, password, balance))
        conn.commit()
        print(f"User '{username}' added successfully with balance {balance}")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists")

# Function to retrieve user information
def get_user(username):
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    if user:
        print(f"User found: ID={user[0]}, Username={user[1]}, Balance={user[3]}")
    else:
        print(f"No user found with username '{username}'")
    return user

# Function to update user balance
def update_balance(username, amount):
    cursor.execute('UPDATE users SET balance = balance + ? WHERE username = ?', (amount, username))
    conn.commit()
    print(f"Updated balance for user '{username}' by {amount}")

# Function to delete a user
def delete_user(username):
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    print(f"User '{username}' deleted successfully")

# Function to list all users
def list_users():
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    print("List of all users:")
    for user in users:
        print(f"ID={user[0]}, Username={user[1]}, Balance={user[3]}")

# Example usage
if __name__ == "__main__":
    add_user('john_doe', 'password123', 100.0)
    add_user('jane_smith', 'password456', 200.0)
    get_user('john_doe')
    update_balance('john_doe', 50.0)
    get_user('john_doe')
    list_users()
    delete_user('john_doe')
    list_users()

# Close the connection
conn.close()