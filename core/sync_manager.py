"""
Gestionnaire principal de la synchronisation entre WooCommerce et Odoo.
Cette classe orchestre le processus de synchronisation des commandes, incluant :
- Récupération des commandes WooCommerce
- Validation des données
- Transformation des données
- Création des commandes dans Odoo
- Suivi de la synchronisation dans la base de données locale
"""

from .wc_client import WooCommerceClient
from .odoo_client import OdooClient
from .models.order import map_wc_order_to_odoo
from utils.logger import logger
from utils.logging_utils import (
    log_procedure, log_error, log_info, log_warning,
    log_sync_operation, log_api_call, log_performance,
    log_data_transformation
)
from core.validator import validate_order
from utils.database import init_db, is_order_already_synced_db, mark_order_as_synced_db
from utils.helpers import log_audit
import time

class SyncManager:
    """
    Gestionnaire de synchronisation qui coordonne le processus de transfert
    des commandes de WooCommerce vers Odoo.
    """
    
    def __init__(self):
        """
        Initialise les clients WooCommerce et Odoo, et la base de données locale.
        """
        log_info("Initialisation du gestionnaire de synchronisation")
        self.wc = WooCommerceClient()
        self.odoo = OdooClient()
        init_db()
        log_info("Gestionnaire de synchronisation initialisé")

    @log_procedure("Synchronisation des commandes")
    def sync_orders(self):
        """
        Synchronise les commandes de WooCommerce vers Odoo.
        
        Le processus comprend :
        1. Récupération des commandes WooCommerce
        2. Pour chaque commande :
           - Vérification si déjà synchronisée
           - Validation des données
           - Transformation en format Odoo
           - Création dans Odoo
           - Marquage comme synchronisée
           - Journalisation de l'audit
        """
        try:
            # Récupération de toutes les commandes WooCommerce
            log_info("Récupération des commandes WooCommerce")
            start_time = time.time()
            orders = self.wc.get_orders()
            log_performance("Récupération des commandes WooCommerce", time.time() - start_time)
            
            log_info(f"{len(orders)} commandes récupérées")
            
            for order in orders:
                try:
                    order_id = order["id"]
                    log_sync_operation("order_processing", {"order_id": order_id})
                    
                    # Vérification si la commande a déjà été synchronisée
                    if is_order_already_synced_db(order_id):
                        log_warning(f"Commande {order_id} déjà synchronisée")
                        log_audit(order_id, "ignored", "Déjà synchronisée")
                        continue
                    
                    # Validation des données de la commande
                    log_info(f"Validation de la commande {order_id}")
                    validate_order(order)
                    
                    # Transformation des données pour Odoo
                    log_info(f"Transformation de la commande {order_id}")
                    start_time = time.time()
                    odoo_order_data = map_wc_order_to_odoo(order)
                    log_performance(f"Transformation commande {order_id}", time.time() - start_time)
                    log_data_transformation("WooCommerce", "Odoo", order_id)
                    
                    # Création de la commande dans Odoo
                    log_info(f"Création de la commande {order_id} dans Odoo")
                    start_time = time.time()
                    self.odoo.create_order(odoo_order_data)
                    log_performance(f"Création commande Odoo {order_id}", time.time() - start_time)
                    
                    # Marquage de la commande comme synchronisée
                    mark_order_as_synced_db(order_id)
                    log_info(f"Commande {order_id} marquée comme synchronisée")
                    
                    log_audit(order_id, "success", "Synchronisation OK")
                    log_sync_operation("order_success", {"order_id": order_id})
                    
                except Exception as ve:
                    log_error(f"Erreur lors du traitement de la commande {order.get('id', '?')}", exc_info=ve)
                    log_audit(order.get('id', '?'), "error", str(ve))
                    log_sync_operation("order_error", {
                        "order_id": order.get('id', '?'),
                        "error": str(ve)
                    })
                    
        except Exception as e:
            log_error("Erreur lors de la synchronisation", exc_info=e)
            raise