import sqlite3

class BotDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id, ))
        return bool(len(result.fetchall())

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ?", (user_id, ))
        return result.fetchone()[0]

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id, ))
        return self.conn.commit()

    def add_personage(self, user_id, type_personage, name_personage):
        self.cursor.execute("INSERT INTO 'personages' ('user_id','type_personage','name_personage') VALUES (?,?,?)", (self.get_user_id(user_id), type_personage, name_personage))
        return self.conn.commit()

    def get_personage(self, user_id, period):

        if period == 'day':
            result = self.cursor.execute("SELECT * FROM 'personage' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY 'date'", (self.get_user_id(user_id)))

        elif period == 'week':
            result = self.cursor.execute("SELECT * FROM 'personage' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY 'date'", (self.get_user_id(user_id)))

        elif period == 'month':
            result = self.cursor.execute("SELECT * FROM 'personage' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY 'date'", (self.get_user_id(user_id)))

        elif period == 'year':
            result = self.cursor.execute("SELECT * FROM 'personage' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', 'start of year') AND datetime('now', 'localtime') ORDER BY 'date'", (self.get_user_id(user_id)))

        else:
            result = self.cursor.execute("SELECT * FROM 'personage' WHERE 'user_id' = ? ORDER BY 'date'",(self.get_user_id(user_id)))

        return result.fetchall()



    def close(self):
            self.conn.close()