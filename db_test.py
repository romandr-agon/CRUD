from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect("todos.db")
    rows = conn.execute("SELECT * FROM todos WHERE deleted = 0").fetchall()
    conn.close()

    html = "<h1>할 일 목록</h1>"

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
    conn.execute("UPDATE todos SET deleted = 1 WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)