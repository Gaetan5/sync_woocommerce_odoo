"""
Client pour l'API Odoo.
Ce module gère toutes les interactions avec l'API Odoo via XML-RPC, incluant :
- Création de commandes
- Création de clients
- Gestion des erreurs d'API
"""

import xmlrpc.client
from config import settings
from core.exceptions import OdooAPIError
from utils.logging_utils import (
    log_procedure, log_error, log_info, log_api_call,
    log_performance
)
from tenacity import retry, wait_exponential, stop_after_attempt
from ratelimit import limits, sleep_and_retry
import time

class OdooClient:
    """
    Client pour interagir avec l'API Odoo via XML-RPC.
    Utilise les paramètres de configuration pour l'authentification.
    """
    
    def __init__(self):
        """
        Initialise le client Odoo avec les paramètres de configuration.
        Établit la connexion XML-RPC et authentifie l'utilisateur.
        """
        log_info("Initialisation du client Odoo")
        try:
            # Connexion aux endpoints XML-RPC d'Odoo
            log_info(f"Connexion à l'API Odoo: {settings.ODOO_URL}")
            self.common = xmlrpc.client.ServerProxy(f"{settings.ODOO_URL}/xmlrpc/2/common")
            self.models = xmlrpc.client.ServerProxy(f"{settings.ODOO_URL}/xmlrpc/2/object")
            
            # Authentification avec les credentials
            log_info("Authentification Odoo en cours...")
            self.uid = self.common.authenticate(
                settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {}
            )
            
            if not self.uid:
                error_msg = "Échec de l'authentification Odoo"
                log_error(error_msg)
                raise OdooAPIError(error_msg)
                
            log_info("Client Odoo initialisé avec succès")
            
        except Exception as e:
            error_msg = f"Erreur lors de l'initialisation du client Odoo: {e}"
            log_error(error_msg, exc_info=e)
            raise OdooAPIError(error_msg)

    @log_procedure("Création de commande Odoo")
    @sleep_and_retry
    @limits(calls=80, period=60)  # 80 appels par minute (adapter selon quota Odoo)
    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def create_order(self, order_data):
        """
        Crée une nouvelle commande dans Odoo.
        
        Args:
            order_data (dict): Données de la commande au format Odoo
            
        Returns:
            int: ID de la commande créée dans Odoo
            
        Raises:
            OdooAPIError: Si une erreur survient lors de la création
        """
        try:
            log_info("Création d'une nouvelle commande dans Odoo")
            start_time = time.time()
            
            # Log de l'appel API
            log_api_call("Odoo", "POST", "sale.order/create")
            
            # Création de la commande
            order_id = self.models.execute_kw(
                settings.ODOO_DB, self.uid, settings.ODOO_PASSWORD,
                "sale.order", "create", [order_data]
            )
            
            # Log de la performance
            duration = time.time() - start_time
            log_performance("Création de commande Odoo", duration)
            
            log_info(f"Commande Odoo créée avec succès (ID: {order_id})")
            return order_id
            
        except Exception as e:
            error_msg = f"Erreur lors de la création de la commande dans Odoo : {e}"
            log_error(error_msg, exc_info=e)
            log_api_call("Odoo", "POST", "sale.order/create", error=str(e))
            raise OdooAPIError(error_msg)

    @log_procedure("Création de client Odoo")
    @sleep_and_retry
    @limits(calls=80, period=60)  # 80 appels par minute (adapter selon quota Odoo)
    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def create_customer(self, customer_data):
        """
        Crée un nouveau client dans Odoo.
        
        Args:
            customer_data (dict): Données du client au format Odoo
            
        Returns:
            int: ID du client créé dans Odoo
            
        Raises:
            OdooAPIError: Si une erreur survient lors de la création
        """
        try:
            log_info("Création d'un nouveau client dans Odoo")
            start_time = time.time()
            
            # Log de l'appel API
            log_api_call("Odoo", "POST", "res.partner/create")
            
            # Création du client
            customer_id = self.models.execute_kw(
                settings.ODOO_DB, self.uid, settings.ODOO_PASSWORD,
                "res.partner", "create", [customer_data]
            )
            
            # Log de la performance
            duration = time.time() - start_time
            log_performance("Création de client Odoo", duration)
            
            log_info(f"Client Odoo créé avec succès (ID: {customer_id})")
            return customer_id
            
        except Exception as e:
            error_msg = f"Erreur lors de la création du client dans Odoo : {e}"
            log_error(error_msg, exc_info=e)
            log_api_call("Odoo", "POST", "res.partner/create", error=str(e))
            raise OdooAPIError(error_msg)