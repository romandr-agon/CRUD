from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect("todos.db")
    rows = conn.execute("SELECT * FROM todos").fetchall()
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
        html += f"<li>[{row[0]}] {row[1]} — 완료: {row[2]}</li>"
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

if __name__ == "__main__":
    app.run(debug=True)