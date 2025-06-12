from .wc_client import WooCommerceClient
from .odoo_client import OdooClient
from .models.order import map_wc_order_to_odoo
from utils.logger import logger

class SyncManager:
    def __init__(self):
        self.wc = WooCommerceClient()
        self.odoo = OdooClient()
    
    def sync_orders(self):
        try:
            orders = self.wc.get_orders()
            for order in orders:
                odoo_order_data = map_wc_order_to_odoo(order)
                self.odoo.create_order(odoo_order_data)
                logger.info(f"Commande {order['id']} synchronisée.")
        except Exception as e:
            logger.error(f"Erreur: {e}")