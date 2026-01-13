
from fastapi import FastAPI
import sqlite3


app = FastAPI()

@app.get("/")

def get_books():
    
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT title, author, year FROM books")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"title": row[0], "author": row[1], "year": row[2]}
        for row in rows
    ]
    
    
    
