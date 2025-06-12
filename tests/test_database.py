import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tempfile
import sqlite3
from utils import database

def test_db_sync_order():
    # Utilise une base temporaire pour ne pas polluer la vraie base
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'test_sync_local.db')
        database.DB_PATH = db_path
        database.init_db()
        order_id = 'test-123'
        assert not database.is_order_already_synced_db(order_id)
        database.mark_order_as_synced_db(order_id)
        assert database.is_order_already_synced_db(order_id)
        # Test idempotence
        database.mark_order_as_synced_db(order_id)
        assert database.is_order_already_synced_db(order_id)
        # Vérifie qu'il n'y a qu'une seule entrée
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM synced_orders WHERE order_id = ?', (order_id,))
            count = c.fetchone()[0]
            assert count == 1
