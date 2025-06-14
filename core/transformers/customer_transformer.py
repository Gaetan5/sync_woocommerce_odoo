"""
Transformateur de clients WooCommerce vers Odoo.
Ce module gère la transformation des données de clients entre les deux systèmes.
"""

from utils.logging_utils import (
    log_procedure, log_error, log_info, log_warning,
    log_data_transformation
)
from core.exceptions import TransformationError

class CustomerTransformer:
    """
    Transforme les données de clients WooCommerce au format Odoo.
    Gère la conversion des champs et la validation des données.
    """
    
    def __init__(self):
        """Initialise le transformateur de clients."""
        log_info("Initialisation du transformateur de clients")
    
    @log_procedure("Transformation de client")
    def transform(self, wc_customer):
        """
        Transforme un client WooCommerce au format Odoo.
        
        Args:
            wc_customer (dict): Client WooCommerce
            
        Returns:
            dict: Client au format Odoo
            
        Raises:
            TransformationError: Si la transformation échoue
        """
        try:
            log_info(f"Transformation du client WooCommerce #{wc_customer.get('id')}")
            
            # Log de la transformation des données
            log_data_transformation(
                "WooCommerce -> Odoo",
                "customer",
                wc_customer.get('id'),
                "Début de la transformation"
            )
            
            # Validation des données requises
            if not self._validate_customer(wc_customer):
                error_msg = f"Données de client invalides pour le client #{wc_customer.get('id')}"
                log_error(error_msg)
                raise TransformationError(error_msg)
            
            # Transformation des données
            odoo_customer = {
                'name': f"{wc_customer.get('first_name', '')} {wc_customer.get('last_name', '')}".strip(),
                'email': wc_customer.get('email'),
                'phone': wc_customer.get('billing', {}).get('phone'),
                'street': wc_customer.get('billing', {}).get('address_1'),
                'street2': wc_customer.get('billing', {}).get('address_2'),
                'city': wc_customer.get('billing', {}).get('city'),
                'zip': wc_customer.get('billing', {}).get('postcode'),
                'country_id': self._get_country_id(wc_customer.get('billing', {}).get('country')),
                'customer_rank': 1,
                'type': 'contact'
            }
            
            # Log de la transformation réussie
            log_data_transformation(
                "WooCommerce -> Odoo",
                "customer",
                wc_customer.get('id'),
                "Transformation réussie"
            )
            
            log_info(f"Client #{wc_customer.get('id')} transformé avec succès")
            return odoo_customer
            
        except Exception as e:
            error_msg = f"Erreur lors de la transformation du client #{wc_customer.get('id')}: {e}"
            log_error(error_msg, exc_info=e)
            log_data_transformation(
                "WooCommerce -> Odoo",
                "customer",
                wc_customer.get('id'),
                f"Échec de la transformation: {str(e)}"
            )
            raise TransformationError(error_msg)
    
    def _validate_customer(self, wc_customer):
        """
        Valide les données du client WooCommerce.
        
        Args:
            wc_customer (dict): Client WooCommerce
            
        Returns:
            bool: True si le client est valide
        """
        required_fields = ['id', 'email', 'first_name', 'last_name']
        missing_fields = [field for field in required_fields if not wc_customer.get(field)]
        
        if missing_fields:
            log_warning(
                f"Champs manquants dans le client #{wc_customer.get('id')}: {', '.join(missing_fields)}"
            )
            return False
            
        return True
    
    def _get_country_id(self, country_code):
        """
        Convertit le code pays WooCommerce en ID de pays Odoo.
        
        Args:
            country_code (str): Code pays WooCommerce
            
        Returns:
            int: ID du pays dans Odoo
        """
        try:
            # Mapping des codes pays (à compléter selon vos besoins)
            country_mapping = {
                'FR': 76,  # France
                'BE': 22,  # Belgique
                'CH': 209, # Suisse
                # Ajoutez d'autres pays selon vos besoins
            }
            
            country_id = country_mapping.get(country_code)
            if not country_id:
                log_warning(f"Code pays non mappé: {country_code}")
                return False
                
            return country_id
            
        except Exception as e:
            error_msg = f"Erreur lors de la conversion du code pays {country_code}: {e}"
            log_error(error_msg, exc_info=e)
            raise TransformationError(error_msg) 