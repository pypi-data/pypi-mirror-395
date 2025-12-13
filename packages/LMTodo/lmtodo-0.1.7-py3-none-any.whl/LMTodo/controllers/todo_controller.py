from LMTodo.models.todo_db import TodoDB


def update_db_path(new_path):
    TodoDB.DB_PATH = new_path


def init_db(path="todo.db"):
    TodoDB.init_db(path)


### Project Management
def get_projects():
    db = TodoDB()
    return db.fetch_all("SELECT id, name FROM projects")


def add_project(name):
    db = TodoDB()
    db.persist("INSERT INTO projects (name) VALUES (?)", (name,))


def edit_project(project_id, name):
    db = TodoDB()
    db.persist("UPDATE projects SET name=? WHERE id=?", (name, project_id))


def delete_project(project_id):
    db = TodoDB()
    db.persist("DELETE FROM projects WHERE id=?", (project_id,))


### Task Management
def get_tasks(project_id=None):
    db = TodoDB()
    if project_id:
        return db.fetch_all(
            "SELECT id, title, status, creation_date, due_date, close_date, project_id, comments FROM tasks WHERE project_id=?",
            (project_id,),
        )
    else:
        return db.fetch_all(
            "SELECT id, title, status, creation_date, due_date, close_date, project_id, comments FROM tasks"
        )


def add_task(description, due_date, project_id):
    db = TodoDB()
    db.persist(
        "INSERT INTO tasks (title, status, creation_date, due_date, close_date, project_id) VALUES (?, 'open', DATE('now'), ?, ?, ?)",
        (description, due_date, None, project_id),
    )


def edit_task(task_id, name, due_date, project_id):
    db = TodoDB()
    db.persist(
        "UPDATE tasks SET title=?, due_date=?, project_id=? WHERE id=?",
        (name, due_date, project_id, task_id),
    )


def delete_task(task_id):
    db = TodoDB()
    db.persist("DELETE FROM tasks WHERE id=?", (task_id,))


def update_task_status(task_id, new_status):
    db = TodoDB()
    if new_status in ["complete", "cancelled"]:
        db.persist(
            "UPDATE tasks SET status=?, close_date=DATE('now') WHERE id=?",
            (new_status, task_id),
        )
    else:
        # If the current status is the same as the new status, revert to 'open'
        db.persist(
            "UPDATE tasks SET status='open', close_date=NULL WHERE id=?", (task_id,)
        )


def update_task_comments(task_id, comments):
    """Persist comments for a task."""
    db = TodoDB()
    db.persist("UPDATE tasks SET comments=? WHERE id=?", (comments, task_id))
