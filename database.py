import os.path
import sqlite3


class DB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_database()
        self.create_tables()

    def create_database(self):
        if not os.path.exists(self.db_name):
            f = open(self.db_name, 'w')
            f.close()

    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_user_id INTEGER NOT NULL,
                    telegram_user_name TEXT NOT NULL,
                    join_date DATETIME NOT NULL DEFAULT ( DATETIME('now') ) 
                );
            '''
            cursor.execute(query)

            query = '''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    created_at DATETIME NOT NULL DEFAULT ( DATETIME('now') )
                );
            '''
            cursor.execute(query)

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def telegram_user_exists(self, telegram_user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE telegram_user_id = ?"
            cursor.execute(query, (telegram_user_id,))
            return cursor.fetchone() is not None

    def add_user(self, telegram_user_id, telegram_user_name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO users (telegram_user_id, telegram_user_name) VALUES (?, ?)"
            cursor.execute(query, (telegram_user_id, telegram_user_name))
            conn.commit()

    def get_user_id(self, telegram_user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT id FROM users WHERE telegram_user_id = ?"
            cursor.execute(query, [telegram_user_id])
            return cursor.fetchone()[0]

    def add_note(self, telegram_user_id, text):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = 'INSERT INTO notes (user_id, text) VALUES (?, ?)'
            cursor.execute(query, (telegram_user_id, text))
            conn.commit()

    def get_notes(self, telegram_user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            user_id = self.get_user_id(telegram_user_id)
            query = "SELECT id, text FROM notes WHERE user_id = ?"
            cursor.execute(query, (user_id,))
            return cursor.fetchall()

    def delete_note(self, telegram_user_id, note_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            user_id = self.get_user_id(telegram_user_id)
            query = "DELETE FROM notes WHERE id = ? AND user_id = ?"
            cursor.execute(query, (note_id, user_id))
            conn.commit()
