"""
Module utilitaire pour le logging.
Ce module fournit des fonctions pour faciliter l'utilisation du système de logging
avec différents niveaux et formats de messages.
"""

import os

# S'assurer que le dossier logs existe AVANT de charger la config
logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
os.makedirs(logs_dir, exist_ok=True)

# Créer les fichiers de log s'ils n'existent pas
sync_log = os.path.join(logs_dir, 'sync.log')
error_log = os.path.join(logs_dir, 'errors.log')

for log_file in [sync_log, error_log]:
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            pass

import logging
import logging.config
from datetime import datetime
from functools import wraps
import time

# Charger la configuration logging si ce n'est pas déjà fait
def _load_logging_config():
    LOGGING_CONF = os.path.join(os.path.dirname(__file__), '../config/logging.conf')
    LOGGING_CONF = os.path.abspath(LOGGING_CONF)
    if os.path.exists(LOGGING_CONF):
        # Créer un dictionnaire de variables pour la configuration
        defaults = {
            'log_dir': logs_dir
        }
        logging.config.fileConfig(LOGGING_CONF, defaults=defaults, disable_existing_loggers=False)

_load_logging_config()

# Configuration du logger
logger = logging.getLogger('sync_woocommerce_odoo')

def log_error(message, exc_info=None):
    """
    Log une erreur avec un message détaillé.
    
    Args:
        message (str): Message d'erreur
        exc_info (Exception, optional): Exception à logger
    """
    logger.error(message, exc_info=exc_info)

def log_warning(message):
    """
    Log un avertissement.
    
    Args:
        message (str): Message d'avertissement
    """
    logger.warning(message)

def log_info(message):
    """
    Log une information.
    
    Args:
        message (str): Message d'information
    """
    logger.info(message)

def log_debug(message):
    """
    Log un message de debug.
    
    Args:
        message (str): Message de debug
    """
    logger.debug(message)

def log_procedure(procedure_name):
    """
    Décorateur pour logger le début et la fin d'une procédure.
    
    Args:
        procedure_name (str): Nom de la procédure à logger
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger.info(f"Début de la procédure: {procedure_name}")
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"Fin de la procédure: {procedure_name} (durée: {duration:.2f}s)")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    f"Erreur dans la procédure: {procedure_name} "
                    f"(durée: {duration:.2f}s): {str(e)}",
                    exc_info=True
                )
                raise
        return wrapper
    return decorator

def log_sync_operation(operation_type, details):
    """
    Log une opération de synchronisation.
    
    Args:
        operation_type (str): Type d'opération (ex: 'order_sync', 'customer_sync')
        details (dict): Détails de l'opération
    """
    message = f"Opération de synchronisation: {operation_type}"
    if details:
        message += f" - Détails: {details}"
    logger.info(message)

def log_api_call(api_name, method, endpoint, status_code=None, error=None):
    """
    Log un appel API.
    
    Args:
        api_name (str): Nom de l'API (WooCommerce ou Odoo)
        method (str): Méthode HTTP
        endpoint (str): Endpoint appelé
        status_code (int, optional): Code de statut HTTP
        error (str, optional): Message d'erreur
    """
    message = f"Appel API {api_name}: {method} {endpoint}"
    if status_code:
        message += f" - Status: {status_code}"
    if error:
        message += f" - Erreur: {error}"
    logger.info(message)

def log_performance(operation, duration):
    """
    Log les performances d'une opération.
    
    Args:
        operation (str): Nom de l'opération
        duration (float): Durée en secondes
    """
    logger.info(f"Performance - {operation}: {duration:.2f}s")

def log_data_transformation(source, data_type, data_id, message):
    """
    Loggue une transformation de données.
    Args:
        source (str): Source de la transformation (ex: 'WooCommerce -> Odoo')
        data_type (str): Type de donnée (ex: 'order', 'customer')
        data_id (str/int): Identifiant de la donnée
        message (str): Message de log
    """
    logger.info(f"[TRANSFORMATION] {source} | {data_type} #{data_id} | {message}")