import os.path
import sqlite3


class DB:
    def __init__(self):
        self.db_name = 'database.sqlite'
        self.create_database()
        self.create_tables()

    def create_database(self):
        if not os.path.exists(self.db_name):
            f = open(self.db_name, 'w')
            f.close()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_user_id INTEGER NOT NULL,
                telegram_user_name TEXT NOT NULL,
                join_date DATETIME NOT NULL DEFAULT ( (DATETIME('now') ) ) 
            );
        '''
            cursor.execute(query)

    def telegram_user_exists(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE telegram_user_id = ?"
            cursor.execute(query, (user_id,))
            return cursor.fetchone() is not None

    def add_user(self, telegram_user_id, telegram_user_name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "INSERT INTO users (telegram_user_id, telegram_user_name) VALUES (?, ?)"
            cursor.execute(query, (telegram_user_id, telegram_user_name))
            conn.commit()
