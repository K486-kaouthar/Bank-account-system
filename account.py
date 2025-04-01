from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Route to get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = [{"id": row[0], "task": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(tasks)

# Route to add a new task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    task = data.get("task")
    if not task:
        return jsonify({"error": "Task content is required"}), 400
    
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task added successfully"}), 201

# Route to delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
