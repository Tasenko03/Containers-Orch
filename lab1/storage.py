import sqlite3
from contextlib import closing


class TaskStore:
    def __init__(self, database_path):
        self.database_path = database_path

    def connect(self):
        connection = sqlite3.connect(self.database_path, isolation_level=None)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self):
        with closing(self.connect()) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0
                )
                """
            )

    def list_tasks(self):
        with closing(self.connect()) as connection:
            rows = connection.execute(
                "SELECT id, title, completed FROM tasks ORDER BY id"
            ).fetchall()
            return [self.serialize(row) for row in rows]

    def create_task(self, title):
        with closing(self.connect()) as connection:
            row = connection.execute(
                "INSERT INTO tasks (title) VALUES (?) RETURNING id, title, completed",
                (title,),
            ).fetchone()
            return self.serialize(row)

    def complete_task(self, task_id):
        with closing(self.connect()) as connection:
            row = connection.execute(
                "UPDATE tasks SET completed = 1 WHERE id = ? RETURNING id, title, completed",
                (task_id,),
            ).fetchone()
            if row is not None:
                return self.serialize(row)
            return None

    @staticmethod
    def serialize(row):
        return {"id": row["id"], "title": row["title"], "completed": bool(row["completed"])}
