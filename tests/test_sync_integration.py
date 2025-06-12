import sys
import os
import pytest
from unittest.mock import patch, MagicMock
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.sync_manager import SyncManager

@patch('core.sync_manager.WooCommerceClient')
@patch('core.sync_manager.OdooClient')
def test_sync_orders_integration(mock_odoo_cls, mock_wc_cls):
    # Mock WooCommerce orders
    mock_wc = MagicMock()
    mock_wc.get_orders.return_value = [
        {"id": 42, "customer_id": 1, "line_items": [{"product_id": 1, "quantity": 2, "price": 10.0}]}
    ]
    mock_wc_cls.return_value = mock_wc

    # Mock Odoo client
    mock_odoo = MagicMock()
    mock_odoo.create_order.return_value = 123
    mock_odoo_cls.return_value = mock_odoo

    # Patch DB helpers et DB_PATH pour base temporaire
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'test_sync_local.db')
        with patch('utils.database.DB_PATH', db_path), \
             patch('core.sync_manager.is_order_already_synced_db', return_value=False), \
             patch('core.sync_manager.mark_order_as_synced_db') as mark_synced, \
             patch('core.sync_manager.log_audit') as log_audit:
            sync = SyncManager()
            sync.sync_orders()
            # Vérifie que la commande a été créée dans Odoo
            mock_odoo.create_order.assert_called_once()
            # Vérifie que la commande a été marquée comme synchronisée
            mark_synced.assert_called_once_with(42)
            # Vérifie que l'audit a été loggé
            log_audit.assert_any_call(42, 'success', 'Synchronisation OK')
