import sqlite3
import os

class ClientsDB:
    def __init__(self, db_url: str):
        self.url = db_url

    def init(self):
        conn = sqlite3.connect(self.url)
        conn.execute("CREATE TABLE Clients ('uuid', 'username', 'password')")
        conn.commit()
        conn.close()

    def destruct(self):
        conn = sqlite3.connect(self.url)
        conn.execute("DROP TABLE Clients")
        conn.commit()
        conn.close()
        

if __name__ == "__main__":
    db = ClientsDB(os.environ.get("DB_URL"))
    db.init()