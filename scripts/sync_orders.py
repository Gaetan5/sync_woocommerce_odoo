import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.sync_manager import SyncManager

if __name__ == "__main__":
    print("=== Synchronisation WooCommerce → Odoo ===")
    try:
        sync = SyncManager()
        sync.sync_orders()
        print("Synchronisation terminée.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Erreur inattendue : {e}")