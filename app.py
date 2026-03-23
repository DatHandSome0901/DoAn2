# from flask import Flask, render_template, request, jsonify, send_file
# from question_generator import generate_exam
# import os

# app = Flask(__name__)
# OUTPUT_DIR = "output"

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/generate", methods=["POST"])
# def gen():
#     data = request.json
#     topic = data["topic"]
#     n = int(data.get("n", 10))

#     questions, filename = generate_exam(topic, n, OUTPUT_DIR)

#     return jsonify({
#         "questions": questions,
#         "file": filename
#     })

# @app.route("/download/<filename>")
# def download(filename):
#     return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, jsonify, send_file, redirect, session
from question_generator import generate_exam
import os, sqlite3

app = Flask(__name__)
app.secret_key = "secret123"
OUTPUT_DIR = "output"
DB = "database.db"

# ================= DB =================
def get_db():
    return sqlite3.connect(DB)

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        content TEXT,
        filename TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, password))
        u = cur.fetchone()

        if u:
            session["user"] = u[0]
        else:
            cur.execute("INSERT INTO users(username, password) VALUES(?,?)", (user, password))
            conn.commit()
            session["user"] = cur.lastrowid

        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= HOME =================
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")

# ================= GENERATE =================
@app.route("/generate", methods=["POST"])
def gen():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    topic = data["topic"]
    n = int(data.get("n", 10))

    questions, filename = generate_exam(topic, n, OUTPUT_DIR)

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO topics(user_id, title, content, filename) VALUES(?,?,?,?)",
        (session["user"], topic, questions, filename)
    )
    conn.commit()

    return jsonify({
        "questions": questions,
        "file": filename
    })

# ================= GET TOPICS =================
@app.route("/topics")
def get_topics():
    if "user" not in session:
        return jsonify([])

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, title, content, filename FROM topics WHERE user_id=? ORDER BY id DESC", (session["user"],))
    data = cur.fetchall()

    return jsonify([
        {"id": r[0], "title": r[1], "content": r[2], "file": r[3]}
        for r in data
    ])

# ================= DELETE =================
@app.route("/delete_topic", methods=["POST"])
def delete_topic():
    tid = request.json["id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM topics WHERE id=? AND user_id=?", (tid, session["user"]))
    conn.commit()

    return jsonify({"ok": True})

# ================= DOWNLOAD =================
@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)