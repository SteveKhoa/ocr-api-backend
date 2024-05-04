import sqlite3
import uuid
from pydantic import BaseModel


class Client(BaseModel):
    db_src: str
    username: str
    password: str

    def create(self):
        conn = sqlite3.connect(self.db_src)
        conn.execute(
            "INSERT INTO Clients ('uuid', 'username', 'password') VALUES (?,?,?)",
            (str(uuid.uuid1()), self.username, self.password),
        )
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect(self.db_src)
        conn.execute(
            "DELETE FROM Clients WHERE username=? and password=?",
            (self.username, self.password),
        )
        conn.commit()
        conn.close()

    def exists(self) -> bool:
        conn = sqlite3.connect(self.db_src)
        retrieved = conn.execute(
            "SELECT username FROM clients where username=?",
            (self.username,),
        ).fetchall()

        return len(retrieved) > 0


if __name__ == "__main__":
    pass
