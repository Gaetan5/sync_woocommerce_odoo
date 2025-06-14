"""
Module de configuration du système de logging.
Ce module initialise le système de logging de l'application en utilisant
une configuration externe définie dans config/logging.conf.
"""

import logging.config
import os

# Chemin vers le fichier de configuration du logging
LOGGING_CONFIG = os.path.join(os.path.dirname(__file__), '../config/logging.conf')

# Configuration du logging à partir du fichier de configuration
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)

# Création du logger principal de l'application
logger = logging.getLogger("sync_woocommerce_odoo")
