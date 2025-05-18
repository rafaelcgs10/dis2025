from flask import Flask, render_template
import sqlite3

def db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, todo_text TEXT NOT NULL UNIQUE) ''')

    c = conn.cursor()
    todos = ['Study', 'Groceries', 'DIS project']
    for todo in todos:
        c.execute('INSERT OR IGNORE INTO todos (todo_text) VALUES (?)', (todo,))

    conn.commit()
    conn.close()

init_db()
app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/todo')
def list_todo():
    conn = db_connection()
    db_todos = conn.execute('SELECT todo_text FROM todos').fetchall()
    conn.close()
    todos = []
    for db_todo in db_todos:
        todos.append(db_todo['todo_text'])
    return render_template('todo.html', todos=todos)
