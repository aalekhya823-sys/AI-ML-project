import requests
from database import get_connection


API_URL = "https://openlibrary.org/subjects/python.json?limit=10"

response1 = requests.get(API_URL)
response1.raise_for_status()  

data = response1.json()
books = data["works"]

db_conn = get_connection()
db_cursor =db_conn.cursor()

db_cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    year INTEGER
)
""")

for book in books:
    title = book.get("title", "Unknown")
    author = book["authors"][0]["name"] if book.get("authors") else "Unknown"
    year = book.get("first_publish_year", 0)

    db_cursor.execute(
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        (title, author, year)
    )

db_conn.commit()
db_conn.close()

print(" Books data fetched from API & stored in SQLite successfully")
