import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.sync_manager import SyncManager

print("Test print tout en haut du fichier")
print("Début de la synchronisation...")

if __name__ == "__main__":
    try:
        sync = SyncManager()
        sync.sync_orders()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Erreur inattendue : {e}")