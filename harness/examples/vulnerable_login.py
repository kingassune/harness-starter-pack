"""Deliberately vulnerable sample — the Level 2 agent's verification target.

Do NOT use any of this in real code. It exists so the harness has something
concrete to inspect and report on.
"""
import sqlite3


def authenticate(username, password):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    # VULNERABLE: user input is string-formatted straight into SQL.
    # e.g. username = "admin' --" bypasses the password check (SQL injection).
    query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (
        username,
        password,
    )
    cur.execute(query)
    return cur.fetchone() is not None
