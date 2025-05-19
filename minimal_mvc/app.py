from flask import Flask, render_template, request
from database import init_db, db_connection
from models.todo import Todo, list_todos
from models.category import Category, list_categories

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
        category_id = request.form['category_todo']
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO todos (todo_text, category_id) VALUES (?, ?)', (new_todo, category_id))
        conn.commit()

    cat = list_categories()
    db_categories = conn.execute('SELECT id, category_name FROM categories').fetchall()
    categories = []
    for db_category in db_categories:
        categories.append((db_category['id'], db_category['category_name']))

    db_todos = conn.execute('SELECT todo_text, category_name FROM todos JOIN categories ON todos.category_id = categories.id').fetchall()
    todos = []
    for db_todo in db_todos:
        todos.append((db_todo['todo_text'], db_todo['category_name']))

    conn.close()
    return render_template('todo.html', todos=todos, categories=cat)
