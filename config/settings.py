"""
Module de configuration centralisé pour l'application.
Ce module charge et valide les variables d'environnement nécessaires
pour la synchronisation entre WooCommerce et Odoo.
"""

import os
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
# Le fichier .env doit être placé à la racine du projet
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# Configuration WooCommerce
# URL de l'API WooCommerce (ex: https://monsite.com/wp-json/wc/v3)
WC_API_URL = os.getenv("WC_API_URL")
# Clé consommateur WooCommerce pour l'authentification API
WC_CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY")
# Secret consommateur WooCommerce pour l'authentification API
WC_CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET")

# Configuration Odoo
# URL de l'instance Odoo (ex: https://odoo.monsite.com)
ODOO_URL = os.getenv("ODOO_URL")
# Nom de la base de données Odoo
ODOO_DB = os.getenv("ODOO_DB")
# Nom d'utilisateur Odoo pour l'authentification
ODOO_USER = os.getenv("ODOO_USER")
# Mot de passe Odoo pour l'authentification
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

# Configuration de la synchronisation
# Fréquence de synchronisation en minutes (défaut: 10 minutes)
SYNC_FREQUENCY = int(os.getenv("SYNC_FREQUENCY", 10))

def validate_settings():
    """
    Valide que toutes les variables d'environnement requises sont définies.
    
    Vérifie la présence des variables suivantes :
    - WC_API_URL : URL de l'API WooCommerce
    - WC_CONSUMER_KEY : Clé consommateur WooCommerce
    - WC_CONSUMER_SECRET : Secret consommateur WooCommerce
    - ODOO_URL : URL de l'instance Odoo
    - ODOO_DB : Nom de la base de données Odoo
    - ODOO_USER : Nom d'utilisateur Odoo
    - ODOO_PASSWORD : Mot de passe Odoo
    
    Raises:
        EnvironmentError: Si une ou plusieurs variables sont manquantes
    """
    missing = []
    for var in [
        "WC_API_URL", "WC_CONSUMER_KEY", "WC_CONSUMER_SECRET",
        "ODOO_URL", "ODOO_DB", "ODOO_USER", "ODOO_PASSWORD"
    ]:
        if not globals().get(var):
            missing.append(var)
    if missing:
        raise EnvironmentError(
            f"Variables d'environnement manquantes : {', '.join(missing)}. "
            "Vérifiez votre fichier .env."
        )

# Validation des paramètres au démarrage
validate_settings()