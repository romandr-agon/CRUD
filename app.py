from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("todos.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            deleted INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    conn = sqlite3.connect("todos.db")
    rows = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()

    html = """
    <style>
        body {
            font-family: sans-serif;
            max-width: 480px;
            margin: 40px auto;
            background: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            background: white;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 8px;
        }
        form {
            margin-bottom: 4px;
        }
        button {
            border: none;
            background: #4a7dff;
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
        }
        input[type="text"] {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 6px;
            width: 60%;
        }
    </style>
    <h1>할 일 목록</h1>
    """

    html += """
        <form action="/add" method="post">
            <input type="text" name="content" placeholder="할 일을 입력하세요">
            <button type="submit">추가</button>
        </form>
    """

    html += "<ul>"
    for row in rows:
        mark = "✅" if row[2] == 1 else "⬜"
        html += f"""
            <li>
                {mark} {row[1]}
                <form action="/toggle/{row[0]}" method="post" style="display:inline">
                    <button type="submit">완료</button>
                </form>
                <form action="/delete/{row[0]}" method="post" style="display:inline">
                    <button type="submit">삭제</button>
                </form>
            </li>
        """
    html += "</ul>"
    return html

@app.route("/add", methods=["post"])
def add():
    content = request.form["content"]
    conn = sqlite3.connect("todos.db")
    conn.execute("INSERT INTO todos (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/toggle/<int:todo_id>", methods=["post"])
def toggle(todo_id):
    conn = sqlite3.connect("todos.db")
    conn.execute("UPDATE todos SET done = 1 - done WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:todo_id>", methods=["post"])
def delete(todo_id):
    conn = sqlite3.connect("todos.db")
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)