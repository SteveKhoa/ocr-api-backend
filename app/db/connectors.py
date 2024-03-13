import sqlite3
import os

connector = sqlite3.connect(os.environ.get("DB_URL"))
