import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="library.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            role TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            isbn TEXT PRIMARY KEY,
            title TEXT,
            available INTEGER
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            isbn TEXT,
            action TEXT,
            time TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(isbn) REFERENCES books(isbn)
        )
        """)

        self.conn.commit()

    def execute_transaction(self, user_id, isbn, action):
        cursor = self.conn.cursor()
        try:
            self.conn.execute("BEGIN")

            cursor.execute(
                "INSERT INTO transactions (user_id, isbn, action, time) VALUES (?, ?, ?, ?)",
                (user_id, isbn, action, datetime.now())
            )

            if action == "BORROW":
                cursor.execute(
                    "UPDATE books SET available = 0 WHERE isbn = ?",
                    (isbn,)
                )
            else:
                cursor.execute(
                    "UPDATE books SET available = 1 WHERE isbn = ?",
                    (isbn,)
                )

            self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            raise e


if __name__ == "__main__":
    db = Database()
    cursor = db.conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (id, name, role) VALUES (?, ?, ?)",
        (1, "Alekhya", "Student")
    )
    cursor.execute(
        "INSERT OR IGNORE INTO books (isbn, title, available) VALUES (?, ?, ?)",
        ("101", "Python Basics", 1)
    )
    db.conn.commit()

    db.execute_transaction(1, "101", "BORROW")

    print("Transaction completed successfully")
