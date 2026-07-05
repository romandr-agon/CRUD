import sqlite3

conn = sqlite3.connect("todos.db")

conn.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0
    )
""")

conn.commit()
conn.close()

print("데이터베이스 준비 완료!")