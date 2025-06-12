import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis un fichier .env
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# WooCommerce
WC_API_URL = os.getenv("WC_API_URL")
WC_CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY")
WC_CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET")

# Odoo
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USER = os.getenv("ODOO_USER")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

# Synchronisation
SYNC_FREQUENCY = int(os.getenv("SYNC_FREQUENCY", 10))  # minutes

def validate_settings():
    missing = []
    for var in [
        "WC_API_URL", "WC_CONSUMER_KEY", "WC_CONSUMER_SECRET",
        "ODOO_URL", "ODOO_DB", "ODOO_USER", "ODOO_PASSWORD"
    ]:
        if not globals().get(var):
            missing.append(var)
    if missing:
        raise EnvironmentError(f"Variables d'environnement manquantes : {', '.join(missing)}. Vérifiez votre fichier .env.")

validate_settings()