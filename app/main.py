import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/user/new")
def create_user():
    return render_template('create_user.html')

@app.route("/users")
def users():
    conn = get_db_connection()
    _users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('list_users.html', users=_users)

@app.route("/api/v1/user/new", methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form.get('email')
        
        conn = get_db_connection()
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?) ", (name, email))
        conn.commit()
        conn.close()

        print(f"Received form: {name}, {email}")
        return redirect(url_for("users"))

    return "wrong call"