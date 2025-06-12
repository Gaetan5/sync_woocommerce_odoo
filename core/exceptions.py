class SyncError(Exception):
    """Exception de synchronisation générique."""
    pass

class WooCommerceAPIError(SyncError):
    """Erreur lors d’un appel à l’API WooCommerce."""
    pass

class OdooAPIError(SyncError):
    """Erreur lors d’un appel à l’API Odoo."""
    pass
