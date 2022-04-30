import os
import sqlite3

class History():
    def __init__(self):
        history_location = os.path.join(os.path.expanduser("~"), '.pancake')
        self.history_file = history_location + '/history.sql'

        self.conn = sqlite3.connect(self.history_file)
        self.conn.row_factory = lambda cursor, row: row[0]

        if not os.path.exists(history_location):
            os.makedirs(history_location)
        self.create_default_table()

    def create_default_table(self):
        default_history_table = """CREATE TABLE IF NOT EXISTS history (location TEXT UNIQUE, weight INT)"""
        cursor = self.conn.cursor()
        cursor.execute(default_history_table)
        cursor.execute("INSERT OR IGNORE INTO history VALUES ('~', '1000')")
        self.conn.commit()
    
    def add_visit(self, folder):
        cursor = self.conn.cursor()
        print(folder)
        sql = """INSERT OR IGNORE INTO history (location, weight) VALUES(?, ?)"""
        cursor.execute(sql, (folder, 1))
        self.conn.commit()

    def get_history(self):
        cursor = self.conn.cursor()
        return cursor.execute("SELECT location FROM history ORDER BY weight DESC").fetchall()
    
    def update_visit_amount(self, folder, amount=1):
        pass
