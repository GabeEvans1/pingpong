import os
import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "board.db")

PAGE = """
<!doctype html>
<title>Message Board</title>
<body style="font-family:sans-serif;max-width:600px;margin:2em auto">
<h1>Message Board</h1>
<form method="post" action="/post">
  <input name="name" placeholder="Name" maxlength="30" required><br><br>
  <textarea name="body" placeholder="Message" maxlength="500" rows="3" cols="50" required></textarea><br>
  <button>Post</button>
</form>
<hr>
{% for m in messages %}
  <p><b>{{ m["name"] }}</b> <small>{{ m["created"] }}</small><br>{{ m["body"] }}</p>
{% else %}
  <p>No messages yet.</p>
{% endfor %}
</body>
"""

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE IF NOT EXISTS messages ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL, body TEXT NOT NULL, "
        "created TEXT DEFAULT CURRENT_TIMESTAMP)"
    )
    return conn

@app.get("/")
def index():
    conn = get_db()
    messages = conn.execute(
        "SELECT * FROM messages ORDER BY id DESC LIMIT 50"
    ).fetchall()
    conn.close()
    return render_template_string(PAGE, messages=messages)

@app.post("/post")
def post():
    name = request.form.get("name", "").strip()[:30]
    body = request.form.get("body", "").strip()[:500]
    if not name or not body:
        return "Name and message required", 400
    conn = get_db()
    conn.execute("INSERT INTO messages (name, body) VALUES (?, ?)", (name, body))
    conn.commit()
    conn.close()
    return redirect("/")

@app.get("/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)