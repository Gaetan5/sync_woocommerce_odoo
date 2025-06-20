"""
Tests d'intégration pour la synchronisation WooCommerce ↔ Odoo.
Ce module teste le processus complet de synchronisation en utilisant
des mocks pour simuler les API externes.
"""

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
    """
    Test d'intégration du processus de synchronisation des commandes.
    
    Ce test vérifie que :
    1. Les commandes sont correctement récupérées de WooCommerce
    2. Les commandes sont correctement créées dans Odoo
    3. Les commandes sont marquées comme synchronisées
    4. Les logs d'audit sont correctement générés
    
    Utilise des mocks pour simuler :
    - L'API WooCommerce
    - L'API Odoo
    - La base de données locale
    - Les fonctions de logging
    """
    # Configuration du mock WooCommerce
    mock_wc = MagicMock()
    mock_wc.get_orders.return_value = [
        {"id": 42, "customer_id": 1, "total": 20.0, "line_items": [
            {"product_id": 1, "quantity": 2, "price": 10.0, "total": 20.0}
        ]}
    ]
    mock_wc_cls.return_value = mock_wc

    # Configuration du mock Odoo
    mock_odoo = MagicMock()
    mock_odoo.create_order.return_value = 123
    mock_odoo_cls.return_value = mock_odoo

    # Création d'un répertoire temporaire pour la base de données de test
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'test_sync_local.db')
        
        # Mock des fonctions de base de données et de logging
        with patch('utils.database.DB_PATH', db_path), \
             patch('core.sync_manager.is_order_already_synced_db', return_value=False), \
             patch('core.sync_manager.mark_order_as_synced_db') as mark_synced, \
             patch('core.sync_manager.log_audit') as log_audit:
            
            # Exécution de la synchronisation
            sync = SyncManager()
            sync.sync_orders()
            
            # Vérifications
            # 1. La commande a été créée dans Odoo
            mock_odoo.create_order.assert_called_once()
            
            # 2. La commande a été marquée comme synchronisée
            mark_synced.assert_called_once_with(42)
            
            # 3. L'audit a été loggé avec succès
            log_audit.assert_any_call(42, 'success', 'Synchronisation OK')
