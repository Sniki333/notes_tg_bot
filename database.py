import os.path
import sqlite3


class DB:
    def __init__(self):
        if not os.path.exists('database.sqlite'):
            f = open('database.sqlite', 'w')
            f.close()

        self.con = sqlite3.connect('database.sqlite')
        self.cur = self.con.cursor()

        query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_user_id INTEGER NOT NULL,
                telegram_user_name TEXT NOT NULL,
                join_date DATETIME NOT NULL DEFAULT ( (DATETIME('now') ) ) 
            );
        '''
        self.cur.execute(query)

    def telegram_user_exists(self, user_id):
        query = "SELECT * FROM users WHERE telegram_user_id = ?"
        result = self.cur.execute(query, (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, telegram_user_id, telegram_user_name):
        query = "INSERT INTO users (telegram_user_id, telegram_user_name) VALUES (?, ?)"
        self.cur.execute(query, (telegram_user_id, telegram_user_name))
        self.con.commit()
