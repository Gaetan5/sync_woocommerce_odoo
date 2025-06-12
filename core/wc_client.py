from woocommerce import API
from config import settings

class WooCommerceClient:
    def __init__(self):
        self.wcapi = API(
            url=settings.WC_API_URL,
            consumer_key=settings.WC_CONSUMER_KEY,
            consumer_secret=settings.WC_CONSUMER_SECRET,
            version="wc/v3"
        )
    
    def get_orders(self, status="processing"):
        return self.wcapi.get("orders", params={"status": status}).json()
    
    def get_customers(self):
        return self.wcapi.get("customers").json()