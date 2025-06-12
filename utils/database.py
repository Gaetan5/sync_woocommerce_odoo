import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../sync_local.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS synced_orders (
                order_id TEXT PRIMARY KEY,
                synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def is_order_already_synced_db(order_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM synced_orders WHERE order_id = ?', (str(order_id),))
        return c.fetchone() is not None

def mark_order_as_synced_db(order_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO synced_orders(order_id) VALUES (?)', (str(order_id),))
        conn.commit()
