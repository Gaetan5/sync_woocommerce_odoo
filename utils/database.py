"""
Module de gestion de la base de données SQLite locale.
Ce module gère le stockage local des informations de synchronisation
pour éviter les doublons et garder une trace des commandes synchronisées.
"""

import sqlite3
import os

# Chemin vers la base de données SQLite locale
DB_PATH = os.path.join(os.path.dirname(__file__), '../sync_local.db')

def get_connection():
    """
    Crée et retourne une connexion à la base de données SQLite.
    
    Returns:
        sqlite3.Connection: Connexion à la base de données
    """
    return sqlite3.connect(DB_PATH)

def init_db():
    """
    Initialise la base de données en créant la table synced_orders
    si elle n'existe pas déjà.
    
    La table stocke :
    - order_id : Identifiant unique de la commande (clé primaire)
    - synced_at : Date et heure de la synchronisation
    """
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS synced_orders (
                order_id TEXT PRIMARY KEY,
                synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def is_order_already_synced_db(order_id):
    """
    Vérifie si une commande a déjà été synchronisée.
    
    Args:
        order_id: Identifiant de la commande à vérifier
        
    Returns:
        bool: True si la commande a déjà été synchronisée, False sinon
    """
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM synced_orders WHERE order_id = ?', (str(order_id),))
        return c.fetchone() is not None

def mark_order_as_synced_db(order_id):
    """
    Marque une commande comme synchronisée dans la base de données.
    
    Args:
        order_id: Identifiant de la commande à marquer
    """
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO synced_orders(order_id) VALUES (?)', (str(order_id),))
        conn.commit()
