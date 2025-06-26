"""
Script de sauvegarde automatique des bases et logs.
Copie les fichiers critiques dans un dossier backup avec horodatage.
"""
import os
import shutil
from datetime import datetime

BACKUP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backups'))
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sync_local.db'))
LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))

os.makedirs(BACKUP_DIR, exist_ok=True)

def backup():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Sauvegarde de la base
    if os.path.exists(DB_PATH):
        shutil.copy(DB_PATH, os.path.join(BACKUP_DIR, f'sync_local_{timestamp}.db'))
    # Sauvegarde des logs
    if os.path.exists(LOGS_DIR):
        dest_logs = os.path.join(BACKUP_DIR, f'logs_{timestamp}')
        shutil.copytree(LOGS_DIR, dest_logs)
    print(f"Backup effectué dans {BACKUP_DIR}")

if __name__ == '__main__':
    backup()
