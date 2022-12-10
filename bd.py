import psycopg2

class DatabaseConnection:
    def __init__(self, name):
        self.conn = psycopg2.connect(dbname=name, user="postgres")
        self.cur = self.conn.cursor()

    def connection(self):
        return self.conn

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def close(self):
        self.cur.close()
        self.conn.close()
