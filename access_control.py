import os
import secrets
import sqlite3
import time

def authorized(header):
    token = os.getenv("GENERATOR_ACCESS_TOKEN", "")
    if len(token) < 32:
        return False
    return secrets.compare_digest((header or "").encode(), ("Bearer " + token).encode())

def reserve_quota(path, now=None):
    now = time.time() if now is None else now
    with sqlite3.connect(path, timeout=5) as db:
        db.execute("CREATE TABLE IF NOT EXISTS requests (ts REAL NOT NULL)")
        db.execute("BEGIN IMMEDIATE")
        db.execute("DELETE FROM requests WHERE ts <= ?", (now - 86400,))
        daily = db.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
        minute = db.execute("SELECT COUNT(*) FROM requests WHERE ts > ?", (now - 60,)).fetchone()[0]
        if daily >= 100 or minute >= 5:
            return False
        db.execute("INSERT INTO requests VALUES (?)", (now,))
        return True
