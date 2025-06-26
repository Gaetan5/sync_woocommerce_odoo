"""
Script principal de synchronisation des commandes entre WooCommerce et Odoo.
Ce script est exécuté par le conteneur Docker 'sync' et gère la synchronisation
automatique des commandes de WooCommerce vers Odoo.
"""

import sys
import os
# Ajout du répertoire parent au PYTHONPATH pour permettre l'import des modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.sync_manager import SyncManager
from utils.metrics import start_metrics_server, sync_success_counter, sync_error_counter, sync_duration_histogram

if __name__ == "__main__":
    print("=== Synchronisation WooCommerce → Odoo ===")
    # Démarre le serveur Prometheus sur le port 8001
    start_metrics_server(port=8001)
    try:
        # Initialisation du gestionnaire de synchronisation
        sync = SyncManager()
        # Lancement de la synchronisation des commandes avec mesure Prometheus
        with sync_duration_histogram.time():
            sync.sync_orders()
        sync_success_counter.inc()
        print("Synchronisation terminée.")
    except Exception as e:
        sync_error_counter.inc()
        import traceback
        traceback.print_exc()
        print(f"Erreur inattendue : {e}")