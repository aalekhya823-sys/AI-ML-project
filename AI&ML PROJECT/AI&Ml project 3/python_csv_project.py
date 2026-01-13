import csv
import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
)
""")

with open("user.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (row["name"], row["email"])
        )

conn.commit()

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

print("Users in database:")
print(rows)  

conn.close()
