"""
Script de purge des données locales.
Ce script supprime les fichiers de données locaux :
- La base de données SQLite (sync_local.db)
- Le fichier d'audit CSV (sync_audit.csv)

Utilisé pour :
- Réinitialiser l'état de la synchronisation
- Nettoyer les données de test
- Résoudre les problèmes de synchronisation
"""

import os

# Liste des fichiers à supprimer
# Les chemins sont relatifs à la racine du projet
FILES_TO_PURGE = [
    os.path.join(os.path.dirname(__file__), '../sync_local.db'),  # Base de données SQLite
    os.path.join(os.path.dirname(__file__), '../sync_audit.csv'),  # Fichier d'audit
]

def purge():
    """
    Supprime les fichiers de données locaux.
    
    Pour chaque fichier :
    1. Vérifie s'il existe
    2. Le supprime s'il existe
    3. Affiche un message de confirmation
    
    Note:
        Cette opération est irréversible.
        Toutes les données de synchronisation seront perdues.
    """
    for f in FILES_TO_PURGE:
        if os.path.exists(f):
            os.remove(f)
            print(f"Supprimé : {f}")
        else:
            print(f"Déjà absent : {f}")

if __name__ == "__main__":
    # Exécution de la purge si le script est lancé directement
    purge()
