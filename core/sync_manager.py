from .wc_client import WooCommerceClient
from .odoo_client import OdooClient
from .models.order import map_wc_order_to_odoo
from utils.logger import logger
from core.validator import validate_order
from utils.database import init_db
from utils.helpers import is_order_already_synced_db, mark_order_as_synced_db, log_audit

class SyncManager:
    def __init__(self):
        self.wc = WooCommerceClient()
        self.odoo = OdooClient()
        init_db()

    def sync_orders(self):
        try:
            orders = self.wc.get_orders()
            for order in orders:
                try:
                    if is_order_already_synced_db(order["id"]):
                        logger.info(f"Commande {order['id']} déjà synchronisée (DB), ignorée.")
                        log_audit(order["id"], "ignored", "Déjà synchronisée")
                        continue
                    validate_order(order)
                    odoo_order_data = map_wc_order_to_odoo(order)
                    self.odoo.create_order(odoo_order_data)
                    mark_order_as_synced_db(order["id"])
                    logger.info(f"Commande {order['id']} synchronisée.")
                    log_audit(order["id"], "success", "Synchronisation OK")
                except Exception as ve:
                    logger.error(f"Commande {order.get('id', '?')} ignorée : {ve}")
                    log_audit(order.get('id', '?'), "error", str(ve))
        except Exception as e:
            logger.error(f"Erreur: {e}")