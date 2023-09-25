import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Подключение к базе данных
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="111",
    host="postgres",
    port="5432"
)

# Создание таблицы для задач
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        due_date DATE
    )
''')
conn.commit()

# Функция для добавления новой задачи
def add_task(title, description, due_date):
    cursor.execute("INSERT INTO tasks (title, description, due_date) VALUES (%s, %s, %s)", (title, description, due_date))
    conn.commit()

# Функция для получения списка задач
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

# Функция для удаления задачи по ID
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()

# API эндпоинт для получения списка задач
@app.route('/tasks', methods=['GET'])
def get_tasks_api():
    tasks = get_tasks()
    return jsonify(tasks)

# API эндпоинт для добавления задачи
@app.route('/tasks', methods=['POST'])
def add_task_api():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    add_task(title, description, due_date)
    return "Task added successfully", 201

# API эндпоинт для удаления задачи по ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_api(task_id):
    delete_task(task_id)
    return "Task deleted successfully", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
