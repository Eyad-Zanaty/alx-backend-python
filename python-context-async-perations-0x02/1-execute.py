import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

with sqlite3.connect('test.db') as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    c.execute("DELETE FROM users")
    c.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
        ('Alice', 22),
        ('Bob', 30),
        ('Charlie', 28),
        ('David', 20)
    ])
    conn.commit()

query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery('test.db', query, params) as results:
    for row in results:
        print(row)