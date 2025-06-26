"""
Script de monitoring simple : vérifie la taille de la base, le nombre d'erreurs, etc.
Peut être lancé en cron ou intégré à un dashboard.
"""
import os
import glob

def check_db_size(db_path):
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"Taille de la base : {size/1024:.1f} Ko")

def count_errors(log_path):
    if os.path.exists(log_path):
        with open(log_path) as f:
            errors = [l for l in f if 'ERROR' in l]
        print(f"Nombre d'erreurs dans les logs : {len(errors)}")

def main():
    db = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sync_local.db'))
    log = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs/errors.log'))
    check_db_size(db)
    count_errors(log)

if __name__ == '__main__':
    main()
