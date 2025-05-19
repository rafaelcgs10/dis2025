from flask import Flask, render_template, request
import sqlite3

def db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db_connection()
    # We have a new table for the todo categories
    conn.execute('''CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, category_name TEXT NOT NULL UNIQUE)''')
    # Now we have a foreign key to the categories
    conn.execute('''CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, todo_text TEXT NOT NULL UNIQUE, category_id INTEGER NOT NULL, FOREIGN KEY(category_id) REFERENCES categories(id))''')

    c = conn.cursor()
    categories = ['DIS', 'House chores']
    for category in categories:
        c.execute('INSERT OR IGNORE INTO categories (category_name) VALUES (?)', (category,))

    todos = [('Assignment 1', 'DIS'), ('Groceries', 'House chores'), ('Assignment 2', 'DIS'), ('Project', 'DIS')]
    for (todo, category) in todos:
        c.execute('INSERT OR IGNORE INTO todos (todo_text, category_id) VALUES (?, (SELECT id FROM categories WHERE category_name = ?))', (todo, category))

    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# We have a new route to /todo
@app.route('/todo', methods=['GET', 'POST'])
def list_todo():
    conn = db_connection()
    # This route has to functions: GET and POST.
    # If there is a POST, we do the insert in the database
    if request.method == 'POST':
        new_todo = request.form['new_todo']
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO todos (todo_text) VALUES (?)', (new_todo,))
        conn.commit()

    db_categories = conn.execute('SELECT id, category_name FROM categories').fetchall()
    categories = []
    for db_category in db_categories:
        categories.append((db_category['id'], db_category['category_name']))

    db_todos = conn.execute('SELECT todo_text, category_name FROM todos JOIN categories ON todos.category_id = categories.id').fetchall()
    todos = []
    for db_todo in db_todos:
        todos.append((db_todo['todo_text'], db_todo['category_name']))

    conn.close()
    return render_template('todo.html', todos=todos, categories=categories)
