from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect("todos.db")
    rows = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()

    html = "<h1>할 일 목록</h1><ul>"
    for row in rows:
        html += f"<li>[{row[0]}] {row[1]} — 완료: {row[2]}</li>"
    html += "</ul>"
    return html

if __name__ == "__main__":
    app.run(debug=True)