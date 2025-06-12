import xmlrpc.client
from config import settings
from core.exceptions import OdooAPIError

class OdooClient:
    def __init__(self):
        self.common = xmlrpc.client.ServerProxy(f"{settings.ODOO_URL}/xmlrpc/2/common")
        self.models = xmlrpc.client.ServerProxy(f"{settings.ODOO_URL}/xmlrpc/2/object")
        self.uid = self.common.authenticate(
            settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASSWORD, {}
        )

    def create_order(self, order_data):
        try:
            return self.models.execute_kw(
                settings.ODOO_DB, self.uid, settings.ODOO_PASSWORD,
                "sale.order", "create", [order_data]
            )
        except Exception as e:
            raise OdooAPIError(f"Erreur lors de la création de la commande dans Odoo : {e}")

    def create_customer(self, customer_data):
        try:
            return self.models.execute_kw(
                settings.ODOO_DB, self.uid, settings.ODOO_PASSWORD,
                "res.partner", "create", [customer_data]
            )
        except Exception as e:
            raise OdooAPIError(f"Erreur lors de la création du client dans Odoo : {e}")