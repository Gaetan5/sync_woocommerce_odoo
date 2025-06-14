"""
Transformateur de commandes WooCommerce vers Odoo.
Ce module gère la transformation des données de commandes entre les deux systèmes.
"""

from utils.logging_utils import (
    log_procedure, log_error, log_info, log_warning,
    log_data_transformation
)
from core.exceptions import TransformationError

class OrderTransformer:
    """
    Transforme les données de commandes WooCommerce au format Odoo.
    Gère la conversion des champs et la validation des données.
    """
    
    def __init__(self):
        """Initialise le transformateur de commandes."""
        log_info("Initialisation du transformateur de commandes")
    
    @log_procedure("Transformation de commande")
    def transform(self, wc_order):
        """
        Transforme une commande WooCommerce au format Odoo.
        
        Args:
            wc_order (dict): Commande WooCommerce
            
        Returns:
            dict: Commande au format Odoo
            
        Raises:
            TransformationError: Si la transformation échoue
        """
        try:
            log_info(f"Transformation de la commande WooCommerce #{wc_order.get('id')}")
            
            # Log de la transformation des données
            log_data_transformation(
                "WooCommerce -> Odoo",
                "order",
                wc_order.get('id'),
                "Début de la transformation"
            )
            
            # Validation des données requises
            if not self._validate_order(wc_order):
                error_msg = f"Données de commande invalides pour l'ordre #{wc_order.get('id')}"
                log_error(error_msg)
                raise TransformationError(error_msg)
            
            # Transformation des données
            odoo_order = {
                'name': f"SO{wc_order.get('id')}",
                'partner_id': wc_order.get('customer_id'),
                'date_order': wc_order.get('date_created'),
                'amount_total': float(wc_order.get('total', 0)),
                'state': 'draft',
                'order_line': self._transform_order_lines(wc_order)
            }
            
            # Log de la transformation réussie
            log_data_transformation(
                "WooCommerce -> Odoo",
                "order",
                wc_order.get('id'),
                "Transformation réussie"
            )
            
            log_info(f"Commande #{wc_order.get('id')} transformée avec succès")
            return odoo_order
            
        except Exception as e:
            error_msg = f"Erreur lors de la transformation de la commande #{wc_order.get('id')}: {e}"
            log_error(error_msg, exc_info=e)
            log_data_transformation(
                "WooCommerce -> Odoo",
                "order",
                wc_order.get('id'),
                f"Échec de la transformation: {str(e)}"
            )
            raise TransformationError(error_msg)
    
    def _validate_order(self, wc_order):
        """
        Valide les données de la commande WooCommerce.
        
        Args:
            wc_order (dict): Commande WooCommerce
            
        Returns:
            bool: True si la commande est valide
        """
        required_fields = ['id', 'customer_id', 'date_created', 'total', 'line_items']
        missing_fields = [field for field in required_fields if not wc_order.get(field)]
        
        if missing_fields:
            log_warning(
                f"Champs manquants dans la commande #{wc_order.get('id')}: {', '.join(missing_fields)}"
            )
            return False
            
        return True
    
    def _transform_order_lines(self, wc_order):
        """
        Transforme les lignes de commande WooCommerce au format Odoo.
        
        Args:
            wc_order (dict): Commande WooCommerce
            
        Returns:
            list: Lignes de commande au format Odoo
        """
        try:
            log_info(f"Transformation des lignes de commande pour l'ordre #{wc_order.get('id')}")
            
            order_lines = []
            for item in wc_order.get('line_items', []):
                order_line = {
                    'product_id': item.get('product_id'),
                    'name': item.get('name'),
                    'product_uom_qty': item.get('quantity', 1),
                    'price_unit': float(item.get('price', 0)),
                    'price_subtotal': float(item.get('total', 0))
                }
                order_lines.append((0, 0, order_line))
                
            log_info(f"{len(order_lines)} lignes transformées pour l'ordre #{wc_order.get('id')}")
            return order_lines
            
        except Exception as e:
            error_msg = f"Erreur lors de la transformation des lignes de commande: {e}"
            log_error(error_msg, exc_info=e)
            raise TransformationError(error_msg) 