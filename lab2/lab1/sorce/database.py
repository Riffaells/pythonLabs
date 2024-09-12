import sqlite3


class Database:
    def __init__(self, db_path='tracker.db'):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        conn = self._connect()
        cursor = conn.cursor()

        # Таблица для задач
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                description TEXT NOT NULL,
                due_date TEXT,
                is_completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')

        # Таблица для привычек
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                description TEXT NOT NULL,
                frequency TEXT,
                last_completed_date TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def add_task(self, user_id, description, due_date):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (user_id, description, due_date) VALUES (?, ?, ?)',
                       (user_id, description, due_date))
        conn.commit()
        conn.close()

    def get_tasks(self, user_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE user_id=? AND is_completed=0', (user_id,))
        tasks = cursor.fetchall()
        conn.close()
        return tasks

    def complete_task(self, task_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET is_completed=1 WHERE id=?', (task_id,))
        conn.commit()
        conn.close()

    def add_habit(self, user_id, description, frequency):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO habits (user_id, description, frequency) VALUES (?, ?, ?)',
                       (user_id, description, frequency))
        conn.commit()
        conn.close()

    def get_habits(self, user_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM habits WHERE user_id=?', (user_id,))
        habits = cursor.fetchall()
        conn.close()
        return habits
