import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, List, Tuple


class TodoDB:
    DB_PATH = Path(__file__).parent.parent / "todo.db"

    @staticmethod
    def init_db(db_path=None):
        if db_path is not None:
            TodoDB.DB_PATH = Path(db_path)
        conn = sqlite3.connect(TodoDB.DB_PATH)
        with conn:
            # Enable foreign key constraints
            conn.execute("PRAGMA foreign_keys = ON;")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    status TEXT CHECK(status IN ('complete', 'open', 'cancelled')) NOT NULL DEFAULT 'open',
                    creation_date TEXT NOT NULL,
                    due_date TEXT,
                    close_date TEXT,
                    project_id INTEGER,
                    comments TEXT,
                    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    data BLOB NOT NULL,
                    task_id INTEGER,
                    FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
                    )
                """)
        conn.close()

    @contextmanager
    def _get_conn_cursor(self):
        conn = sqlite3.connect(TodoDB.DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        try:
            yield conn, cursor
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()

    def fetch_all(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple]:
        """Run a SELECT query and return all rows."""
        with self._get_conn_cursor() as (conn, cur):
            cur.execute(query, params)
            return cur.fetchall()

    def persist(self, query: str, params: Tuple[Any, ...] = ()) -> None:
        """Run an INSERT (or any write) query and commit."""
        with self._get_conn_cursor() as (conn, cur):
            cur.execute(query, params)
            conn.commit()
