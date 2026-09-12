from fastapi import FastAPI
import sqlite3

app = FastAPI()

def get_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.get("/users")
def read_users():
    users = get_users()
    return {"users": users}
