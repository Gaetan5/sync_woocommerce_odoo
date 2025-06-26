"""
Gestion de la date de dernière synchronisation pour la sync incrémentale.
Stocke la date dans un fichier texte (last_synced_at.txt).
"""
import os
from datetime import datetime, UTC

SYNC_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../last_synced_at.txt'))


def get_last_synced_at():
    if os.path.exists(SYNC_FILE):
        with open(SYNC_FILE) as f:
            return f.read().strip()
    return None

def set_last_synced_at(dt=None):
    if dt is None:
        dt = datetime.now(UTC).isoformat()
    with open(SYNC_FILE, 'w') as f:
        f.write(dt)
    return dt
