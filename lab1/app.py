import os

from flask import Flask, request

from storage import TaskStore


app = Flask(__name__)
store = TaskStore(os.environ.get("TASKS_DB", "/data/tasks.sqlite3"))
store.initialize()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return store.list_tasks()


@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("title"), str):
        return {"error": "title must be a non-empty string"}, 400

    title = data["title"].strip()
    if not title:
        return {"error": "title must be a non-empty string"}, 400

    return store.create_task(title), 201


@app.patch("/tasks/<int:task_id>/complete")
def complete_task(task_id):
    if task_id > 2**63 - 1:
        return {"error": "task not found"}, 404

    task = store.complete_task(task_id)
    if task is None:
        return {"error": "task not found"}, 404
    return task
