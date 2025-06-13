from woocommerce import API
from config import settings
from core.exceptions import WooCommerceAPIError
import requests

class WooCommerceClient:
    def __init__(self):
        self.wcapi = API(
            url=settings.WC_API_URL,
            consumer_key=settings.WC_CONSUMER_KEY,
            consumer_secret=settings.WC_CONSUMER_SECRET,
            version="wc/v3"
        )

    def get_orders(self, status="processing"):
        try:
            response = self.wcapi.get("orders", params={"status": status})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise WooCommerceAPIError(f"Erreur lors de la récupération des commandes WooCommerce : {e}")

    def get_customers(self):
        try:
            response = self.wcapi.get("customers")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise WooCommerceAPIError(f"Erreur lors de la récupération des clients WooCommerce : {e}")