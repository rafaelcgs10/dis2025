from flask import Flask, render_template, request
from database import init_db, db_connection
from models.todo import Todo, list_todos, insert_todo
from models.category import Category, list_categories, insert_category

init_db()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/todo', methods=['GET', 'POST'])
def todos():
    if request.method == 'POST':
        todo_text = request.form['new_todo']
        category_id = request.form['category_todo']
        insert_todo(todo_text, category_id)

    categories = list_categories()

    todos = list_todos()

    return render_template('todo.html', todos=todos, categories=categories)

@app.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        category_name = request.form['category_name']
        insert_category(category_name)

    categories = list_categories()

    return render_template('category.html', categories=categories)
