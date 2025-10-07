import sqlite3
import os
from datetime import datetime
import hashlib
from config import DB_PATH, ADMIN_PASSWORD_DEFAULT

def ensure_db():
    created = False
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                username TEXT,
                password_hash TEXT,
                weak_integer INTEGER,
                ip TEXT,
                user_agent TEXT,
                screen TEXT,
                timezone TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE meta (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        admin_hash = hashlib.sha256(ADMIN_PASSWORD_DEFAULT.encode('utf-8')).hexdigest()
        cur.execute("INSERT INTO meta (key, value) VALUES (?, ?)", ("admin_hash", admin_hash))
        conn.commit()
        conn.close()
        created = True
    return created

def get_conn():
    return sqlite3.connect(DB_PATH)

def record_attempt(username, password_plain, weak_bool, ip, user_agent, screen, timezone):
    h = hashlib.sha256(password_plain.encode('utf-8')).hexdigest()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO attempts (time, username, password_hash, weak_integer, ip, user_agent, screen, timezone)
        VALUES (?,?,?,?,?,?,?,?)
    """, (datetime.utcnow().isoformat(), username, h, int(weak_bool), ip, user_agent, screen, timezone))
    conn.commit()
    conn.close()

def fetch_attempts():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, time, username, password_hash, weak_integer, ip, user_agent, screen, timezone
        FROM attempts ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_admin_hash():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT value FROM meta WHERE key=?", ("admin_hash",))
    r = cur.fetchone()
    conn.close()
    return r[0] if r else None

def set_admin_hash(new_hash_hex):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO meta (key,value) VALUES (?,?)", ("admin_hash", new_hash_hex))
    conn.commit()
    conn.close()
