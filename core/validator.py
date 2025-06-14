"""
Module de validation des données.
Ce module gère la validation des données entre WooCommerce et Odoo.
"""

from utils.logging_utils import (
    log_procedure, log_error, log_info, log_warning,
    log_data_transformation
)
from core.exceptions import ValidationError

class DataValidator:
    """
    Valide les données entre WooCommerce et Odoo.
    Assure la cohérence et l'intégrité des données.
    """
    
    def __init__(self):
        """Initialise le validateur de données."""
        log_info("Initialisation du validateur de données")
    
    @log_procedure("Validation de commande")
    def validate_order(self, order_data):
        """
        Valide les données d'une commande.
        
        Args:
            order_data (dict): Données de la commande
            
        Returns:
            bool: True si la commande est valide
            
        Raises:
            ValidationError: Si la validation échoue
        """
        try:
            log_info(f"Validation de la commande #{order_data.get('id')}")
            
            # Log de la validation
            log_data_transformation(
                "Validation",
                "order",
                order_data.get('id'),
                "Début de la validation"
            )
            
            # Vérification des champs obligatoires
            required_fields = ['id', 'customer_id', 'total', 'line_items']
            missing_fields = [field for field in required_fields if not order_data.get(field)]
            
            if missing_fields:
                error_msg = f"Champs manquants dans la commande: {', '.join(missing_fields)}"
                log_error(error_msg)
                log_data_transformation(
                    "Validation",
                    "order",
                    order_data.get('id'),
                    f"Échec de la validation: {error_msg}"
                )
                raise ValidationError(error_msg)
            
            # Vérification des montants
            if not self._validate_amounts(order_data):
                error_msg = "Montants de commande invalides"
                log_error(error_msg)
                log_data_transformation(
                    "Validation",
                    "order",
                    order_data.get('id'),
                    f"Échec de la validation: {error_msg}"
                )
                raise ValidationError(error_msg)
            
            # Log de la validation réussie
            log_data_transformation(
                "Validation",
                "order",
                order_data.get('id'),
                "Validation réussie"
            )
            
            log_info(f"Commande #{order_data.get('id')} validée avec succès")
            return True
            
        except Exception as e:
            error_msg = f"Erreur lors de la validation de la commande #{order_data.get('id')}: {e}"
            log_error(error_msg, exc_info=e)
            log_data_transformation(
                "Validation",
                "order",
                order_data.get('id'),
                f"Échec de la validation: {str(e)}"
            )
            raise ValidationError(error_msg)
    
    def _validate_amounts(self, order_data):
        """
        Valide les montants de la commande.
        
        Args:
            order_data (dict): Données de la commande
            
        Returns:
            bool: True si les montants sont valides
        """
        try:
            total = float(order_data.get('total', 0))
            line_items_total = sum(
                float(item.get('total', 0)) for item in order_data.get('line_items', [])
            )
            
            # Vérification de la cohérence des montants
            if abs(total - line_items_total) > 0.01:  # Tolérance de 0.01 pour les arrondis
                log_warning(
                    f"Différence de montant détectée pour la commande #{order_data.get('id')}: "
                    f"total={total}, somme_lignes={line_items_total}"
                )
                return False
            
            return True

        except Exception as e:
            error_msg = f"Erreur lors de la validation des montants: {e}"
            log_error(error_msg, exc_info=e)
            return False
    
    @log_procedure("Validation de client")
    def validate_customer(self, customer_data):
        """
        Valide les données d'un client.
        
        Args:
            customer_data (dict): Données du client
            
        Returns:
            bool: True si le client est valide
            
        Raises:
            ValidationError: Si la validation échoue
        """
        try:
            log_info(f"Validation du client #{customer_data.get('id')}")
            
            # Log de la validation
            log_data_transformation(
                "Validation",
                "customer",
                customer_data.get('id'),
                "Début de la validation"
            )
            
            # Vérification des champs obligatoires
            required_fields = ['id', 'email', 'first_name', 'last_name']
            missing_fields = [field for field in required_fields if not customer_data.get(field)]
            
            if missing_fields:
                error_msg = f"Champs manquants dans le client: {', '.join(missing_fields)}"
                log_error(error_msg)
                log_data_transformation(
                    "Validation",
                    "customer",
                    customer_data.get('id'),
                    f"Échec de la validation: {error_msg}"
                )
                raise ValidationError(error_msg)
            
            # Vérification de l'email
            if not self._validate_email(customer_data.get('email')):
                error_msg = f"Email invalide pour le client #{customer_data.get('id')}"
                log_error(error_msg)
                log_data_transformation(
                    "Validation",
                    "customer",
                    customer_data.get('id'),
                    f"Échec de la validation: {error_msg}"
                )
                raise ValidationError(error_msg)
            
            # Log de la validation réussie
            log_data_transformation(
                "Validation",
                "customer",
                customer_data.get('id'),
                "Validation réussie"
            )
            
            log_info(f"Client #{customer_data.get('id')} validé avec succès")
            return True
            
        except Exception as e:
            error_msg = f"Erreur lors de la validation du client #{customer_data.get('id')}: {e}"
            log_error(error_msg, exc_info=e)
            log_data_transformation(
                "Validation",
                "customer",
                customer_data.get('id'),
                f"Échec de la validation: {str(e)}"
            )
            raise ValidationError(error_msg)
    
    def _validate_email(self, email):
        """
        Valide le format d'une adresse email.
        
        Args:
            email (str): Adresse email à valider
            
        Returns:
            bool: True si l'email est valide
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
