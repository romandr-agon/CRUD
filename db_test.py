import sqlite3

conn = sqlite3.connect("todos.db")

# Create: 할 일 두 개 넣기
conn.execute("INSERT INTO todos (content) VALUES (?)", ("우유 사기",))
conn.execute("INSERT INTO todos (content) VALUES (?)", ("운동하기",))
conn.commit()

# Read: 전부 꺼내 읽기
rows = conn.execute("SELECT * FROM todos").fetchall()
for row in rows:
    print(row)

conn.close()