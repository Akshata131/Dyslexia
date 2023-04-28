import sqlite3

conn = sqlite3.connect('users.db')

cursor = conn.cursor()

# Create a table named 'users' with columns 'username' and 'password'
cursor.execute('''CREATE TABLE users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT, password TEXT)''')

# Save the changes and close the connection
conn.commit()
conn.close()
