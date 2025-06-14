"""
Module de fonctions utilitaires pour le projet sync_woocommerce_odoo.
Ce module contient des fonctions d'aide pour le formatage et l'audit.
"""

import os
import csv
from datetime import datetime

# Chemin vers le fichier de log d'audit
AUDIT_LOG = os.path.join(os.path.dirname(__file__), '../sync_audit.csv')

def format_date(date_str):
    """
    Formate une date selon le format attendu par Odoo.
    
    Args:
        date_str (str): Date à formater
        
    Returns:
        str: Date formatée
    """
    # TODO: Implémenter le formatage de date selon les besoins
    return date_str

def log_audit(order_id, status, message):
    """
    Enregistre une entrée dans le fichier d'audit CSV.
    
    Le fichier d'audit contient les colonnes suivantes :
    - timestamp : Date et heure de l'événement
    - order_id : Identifiant de la commande
    - status : Statut de la synchronisation (success, error, ignored)
    - message : Message détaillant l'événement
    
    Args:
        order_id: Identifiant de la commande
        status (str): Statut de la synchronisation
        message (str): Message détaillant l'événement
    """
    with open(AUDIT_LOG, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            datetime.now().isoformat(),
            order_id,
            status,
            message
        ])
