import sqlite3
import os

# Quick fix for this issue:
# https://stackoverflow.com/questions/48218065/objects-created-in-a-thread-can-only-be-used-in-that-same-thread
# May be potentially harmful in the future, however, for now leave it as it is.
connector = sqlite3.connect(os.environ.get("DB_URL"), check_same_thread=False)
