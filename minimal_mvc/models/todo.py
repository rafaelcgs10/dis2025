from database import db_connection
from models.category import Category

class Todo:
    def __init__(self, id, text, category_name):
        self.id = id
        self.text = text
        self.category_name = category_name

def list_todos():
    conn = db_connection()
    db_todos = conn.execute('SELECT id, todo_text, category_name FROM todos JOIN categories ON todos.category_id = categories.id').fetchall()
    todos = []
    for db_todo in db_todos:
        todos.append(Todo(db_todo['id'], db_todo['todo_text'], db_todo['category_name']))

    conn.close()
    return todos
