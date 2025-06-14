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

if __name__ == "__main__":
    print("=== Synchronisation WooCommerce → Odoo ===")
    try:
        # Initialisation du gestionnaire de synchronisation
        sync = SyncManager()
        # Lancement de la synchronisation des commandes
        sync.sync_orders()
        print("Synchronisation terminée.")
    except Exception as e:
        # Gestion des erreurs non prévues avec traceback complet
        import traceback
        traceback.print_exc()
        print(f"Erreur inattendue : {e}")