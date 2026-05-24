import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = os.environ.get("SYNTHARA_DB_PATH", "synthara.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            api_key TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            credits REAL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            system_prompt TEXT NOT NULL,
            model TEXT NOT NULL DEFAULT 'qwen3:latest',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            agent_id INTEGER,
            prompt_tokens INTEGER DEFAULT 0,
            completion_tokens INTEGER DEFAULT 0,
            cost REAL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            tx_signature TEXT UNIQUE,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()

def create_user(email, api_key):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (email, api_key, credits) VALUES (?, ?, ?)",
            (email, api_key, 1.0)
        )
        conn.commit()
        user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_api_key(api_key):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE api_key = ?", (api_key,)
    ).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user(email):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return dict(user) if user else None

def save_agent_to_db(user_id, name, description, system_prompt, model):
    conn = get_db()
    conn.execute(
        "INSERT INTO agents (user_id, name, description, system_prompt, model) VALUES (?, ?, ?, ?, ?)",
        (user_id, name, description, system_prompt, model)
    )
    conn.commit()
    agent_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return agent_id

def get_user_agents(user_id):
    conn = get_db()
    agents = conn.execute(
        "SELECT * FROM agents WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
    ).fetchall()
    conn.close()
    return [dict(a) for a in agents]

def get_agent(agent_id):
    conn = get_db()
    agent = conn.execute("SELECT * FROM agents WHERE id = ?", (agent_id,)).fetchone()
    conn.close()
    return dict(agent) if agent else None

def record_usage(user_id, agent_id, prompt_tokens, completion_tokens, cost):
    conn = get_db()
    conn.execute(
        "INSERT INTO usage (user_id, agent_id, prompt_tokens, completion_tokens, cost) VALUES (?, ?, ?, ?, ?)",
        (user_id, agent_id, prompt_tokens, completion_tokens, cost)
    )
    conn.commit()
    conn.close()

def deduct_credits(user_id, amount):
    conn = get_db()
    conn.execute("UPDATE users SET credits = credits - ? WHERE id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def add_credits(user_id, amount, tx_signature=None):
    conn = get_db()
    conn.execute("UPDATE users SET credits = credits + ? WHERE id = ?", (amount, user_id))
    if tx_signature:
        conn.execute(
            "INSERT INTO payments (user_id, amount, tx_signature, status) VALUES (?, ?, ?, 'completed')",
            (user_id, amount, tx_signature)
        )
    conn.commit()
    conn.close()
