"""
Client pour l'API WooCommerce.
Ce module gère toutes les interactions avec l'API WooCommerce, incluant :
- Récupération des commandes
- Récupération des clients
- Gestion des erreurs d'API
"""

from woocommerce import API
from config import settings
from core.exceptions import WooCommerceAPIError
from utils.logging_utils import (
    log_procedure, log_error, log_info, log_api_call,
    log_performance
)
import requests
import time
from tenacity import retry, wait_exponential, stop_after_attempt
from ratelimit import limits, sleep_and_retry

class WooCommerceClient:
    """
    Client pour interagir avec l'API WooCommerce.
    Utilise les paramètres de configuration pour l'authentification.
    """
    
    def __init__(self):
        """
        Initialise le client WooCommerce avec les paramètres de configuration.
        Utilise les variables d'environnement pour les credentials.
        """
        log_info("Initialisation du client WooCommerce")
        self.wcapi = API(
            url=settings.WC_API_URL,
            consumer_key=settings.WC_CONSUMER_KEY,
            consumer_secret=settings.WC_CONSUMER_SECRET,
            version="wc/v3"
        )
        log_info("Client WooCommerce initialisé")

    @log_procedure("Récupération des commandes WooCommerce")
    @sleep_and_retry
    @limits(calls=80, period=60)  # 80 appels par minute (adapter selon quota WooCommerce)
    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def get_orders(self, status="processing", after=None):
        """
        Récupère les commandes WooCommerce avec un statut spécifique et optionnellement après une date donnée.
        
        Args:
            status (str): Statut des commandes à récupérer (par défaut: "processing")
            after (str): Date ISO 8601 (ex: '2024-01-01T00:00:00') pour ne récupérer que les commandes récentes
            
        Returns:
            list: Liste des commandes au format JSON
            
        Raises:
            WooCommerceAPIError: Si une erreur survient lors de l'appel API
        """
        try:
            log_info(f"Récupération des commandes avec le statut: {status} après: {after}")
            start_time = time.time()
            params = {"status": status}
            if after:
                params["after"] = after
            
            # Log de l'appel API
            log_api_call("WooCommerce", "GET", f"orders?status={status}&after={after}")
            
            # Appel à l'API
            response = self.wcapi.get("orders", params=params)
            response.raise_for_status()
            
            # Log de la performance
            duration = time.time() - start_time
            log_performance("Récupération des commandes WooCommerce", duration)
            
            # Log du résultat
            orders = response.json()
            log_info(f"{len(orders)} commandes récupérées")
            
            return orders
            
        except requests.RequestException as e:
            error_msg = f"Erreur lors de la récupération des commandes WooCommerce : {e}"
            log_error(error_msg, exc_info=e)
            log_api_call("WooCommerce", "GET", "orders", error=str(e))
            raise WooCommerceAPIError(error_msg)

    @log_procedure("Récupération des clients WooCommerce")
    def get_customers(self):
        """
        Récupère tous les clients WooCommerce.
        
        Returns:
            list: Liste des clients au format JSON
            
        Raises:
            WooCommerceAPIError: Si une erreur survient lors de l'appel API
        """
        try:
            log_info("Récupération des clients")
            start_time = time.time()
            
            # Log de l'appel API
            log_api_call("WooCommerce", "GET", "customers")
            
            # Appel à l'API
            response = self.wcapi.get("customers")
            response.raise_for_status()
            
            # Log de la performance
            duration = time.time() - start_time
            log_performance("Récupération des clients WooCommerce", duration)
            
            # Log du résultat
            customers = response.json()
            log_info(f"{len(customers)} clients récupérés")
            
            return customers
            
        except requests.RequestException as e:
            error_msg = f"Erreur lors de la récupération des clients WooCommerce : {e}"
            log_error(error_msg, exc_info=e)
            log_api_call("WooCommerce", "GET", "customers", error=str(e))
            raise WooCommerceAPIError(error_msg)