# Fonctions utilitaires pour sync_woocommerce_odoo

import os
import csv
from datetime import datetime

AUDIT_LOG = os.path.join(os.path.dirname(__file__), '../sync_audit.csv')

def format_date(date_str):
    # Exemple de formatage de date
    return date_str

def log_audit(order_id, status, message):
    with open(AUDIT_LOG, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            datetime.now().isoformat(),
            order_id,
            status,
            message
        ])
