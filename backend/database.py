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

def get_user_by_id(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users():
    conn = get_db()
    users = conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(u) for u in users]

def get_all_agents():
    conn = get_db()
    agents = conn.execute("SELECT agents.*, users.email FROM agents JOIN users ON agents.user_id = users.id ORDER BY agents.created_at DESC").fetchall()
    conn.close()
    return [dict(a) for a in agents]

def get_all_usage():
    conn = get_db()
    usage = conn.execute("SELECT usage.*, users.email FROM usage JOIN users ON usage.user_id = users.id ORDER BY usage.created_at DESC LIMIT 500").fetchall()
    conn.close()
    return [dict(u) for u in usage]

def get_all_payments():
    conn = get_db()
    payments = conn.execute("SELECT payments.*, users.email FROM payments JOIN users ON payments.user_id = users.id ORDER BY payments.created_at DESC").fetchall()
    conn.close()
    return [dict(p) for p in payments]

def get_total_stats():
    conn = get_db()
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_agents = conn.execute("SELECT COUNT(*) FROM agents").fetchone()[0]
    total_usage = conn.execute("SELECT COUNT(*) FROM usage").fetchone()[0]
    total_credits = conn.execute("SELECT COALESCE(SUM(credits), 0) FROM users").fetchone()[0]
    total_revenue = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE status = 'completed'").fetchone()[0]
    conn.close()
    return {
        "total_users": total_users,
        "total_agents": total_agents,
        "total_api_calls": total_usage,
        "total_credits_in_system": total_credits,
        "total_revenue_sol": total_revenue
    }

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
