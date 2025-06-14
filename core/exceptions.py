"""
Exceptions personnalisées pour l'application.
Ce module définit les exceptions spécifiques utilisées dans l'application.
"""

class SyncError(Exception):
    """Exception de base pour les erreurs de synchronisation."""
    pass

class TransformationError(SyncError):
    """Exception levée lors d'une erreur de transformation de données."""
    pass

class ValidationError(SyncError):
    """Exception levée lors d'une erreur de validation de données."""
    pass

class APIError(SyncError):
    """Exception levée lors d'une erreur d'API."""
    pass

class WooCommerceAPIError(APIError):
    """Exception levée lors d'une erreur de l'API WooCommerce."""
    pass

class OdooAPIError(APIError):
    """Exception levée lors d'une erreur de l'API Odoo."""
    pass

class DatabaseError(SyncError):
    """Exception levée lors d'une erreur de base de données."""
    pass

class ConfigurationError(SyncError):
    """Exception levée lors d'une erreur de configuration."""
    pass
