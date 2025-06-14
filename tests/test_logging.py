"""
Tests du système de logging.
Ce module teste les différentes fonctionnalités de logging.
"""

import unittest
import os
import logging
from utils.logging_utils import (
    log_error, log_warning, log_info, log_debug,
    log_performance, log_procedure, log_sync_operation,
    log_api_call, log_data_transformation
)
from core.transformers.order_transformer import OrderTransformer
from core.transformers.customer_transformer import CustomerTransformer
from core.validator import DataValidator
from core.exceptions import TransformationError, ValidationError
import time

class TestLoggingSystem(unittest.TestCase):
    """Tests du système de logging."""
    
    def setUp(self):
        """Configuration initiale des tests."""
        # Définir le chemin absolu du dossier logs
        self.logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
        self.sync_log = os.path.join(self.logs_dir, 'sync.log')
        self.errors_log = os.path.join(self.logs_dir, 'errors.log')
        
        # Vérifier que le dossier logs existe
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        
        # Nettoyer les fichiers de log existants
        for log_file in [self.sync_log, self.errors_log]:
            if os.path.exists(log_file):
                os.remove(log_file)
        
        # Créer les fichiers de log vides
        for log_file in [self.sync_log, self.errors_log]:
            with open(log_file, 'w') as f:
                pass
        
        # Recharger la configuration du logger pour rouvrir les fichiers
        import importlib
        import utils.logging_utils
        importlib.reload(utils.logging_utils)
        
        # Forcer la création du fichier de log dès le début
        log_info("Initialisation des tests de logging (création du fichier de log)")
        time.sleep(0.05)  # Laisser le temps au système de créer le fichier
    
    def test_basic_logging(self):
        """Test des fonctions de logging de base."""
        # Test log_error
        log_error("Test d'erreur", exc_info=Exception("Erreur de test"))
        
        # Test log_warning
        log_warning("Test d'avertissement")
        
        # Test log_info
        log_info("Test d'information")
        
        # Test log_debug
        log_debug("Test de debug")
        
        # Vérifier que les logs ont été créés
        self.assertTrue(os.path.exists(self.sync_log))
        self.assertTrue(os.path.exists(self.errors_log))
        
        # Vérifier le contenu des logs
        with open(self.sync_log, 'r') as f:
            sync_logs = f.read()
            self.assertIn("Test d'erreur", sync_logs)
            self.assertIn("Test d'avertissement", sync_logs)
            self.assertIn("Test d'information", sync_logs)
            self.assertIn("Test de debug", sync_logs)
    
    def test_performance_logging(self):
        """Test du logging de performance."""
        # Test log_performance
        log_performance("Test de performance", 1.5)
        
        # Vérifier le contenu des logs
        with open(self.sync_log, 'r') as f:
            sync_logs = f.read()
            self.assertIn("Test de performance", sync_logs)
            self.assertIn("1.5", sync_logs)
    
    def test_procedure_logging(self):
        """Test du logging de procédure."""
        @log_procedure("Test de procédure")
        def test_procedure():
            return "Résultat de test"
        
        # Exécuter la procédure
        result = test_procedure()
        
        # Vérifier le résultat
        self.assertEqual(result, "Résultat de test")
        
        # Vérifier les logs
        with open(self.sync_log, 'r') as f:
            sync_logs = f.read()
            self.assertIn("Début de la procédure: Test de procédure", sync_logs)
            self.assertIn("Fin de la procédure: Test de procédure", sync_logs)
    
    def test_order_transformer_logging(self):
        """Test du logging dans le transformateur de commandes."""
        transformer = OrderTransformer()
        
        # Test avec des données valides
        valid_order = {
            'id': 1,
            'customer_id': 1,
            'date_created': '2024-01-01',
            'total': '100.00',
            'line_items': [
                {
                    'product_id': 1,
                    'name': 'Test Product',
                    'quantity': 1,
                    'price': '100.00',
                    'total': '100.00'
                }
            ]
        }
        
        # Transformer la commande
        result = transformer.transform(valid_order)
        
        # Vérifier le résultat
        self.assertIsNotNone(result)
        
        # Vérifier les logs
        with open(self.sync_log, 'r') as f:
            sync_logs = f.read()
            self.assertIn("Transformation de la commande WooCommerce #1", sync_logs)
            self.assertIn("Commande #1 transformée avec succès", sync_logs)
        
        # Test avec des données invalides
        invalid_order = {
            'id': 2,
            'customer_id': None,
            'total': '100.00'
        }
        
        # Vérifier que la transformation échoue
        with self.assertRaises(TransformationError):
            transformer.transform(invalid_order)
        
        # Vérifier les logs d'erreur
        with open(self.errors_log, 'r') as f:
            error_logs = f.read()
            self.assertIn("Données de commande invalides", error_logs)
    
    def test_customer_transformer_logging(self):
        """Test du logging dans le transformateur de clients."""
        transformer = CustomerTransformer()
        
        # Test avec des données valides
        valid_customer = {
            'id': 1,
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'billing': {
                'phone': '0123456789',
                'address_1': '123 Test St',
                'city': 'Test City',
                'postcode': '12345',
                'country': 'FR'
            }
        }
        
        # Transformer le client
        result = transformer.transform(valid_customer)
        
        # Vérifier le résultat
        self.assertIsNotNone(result)
        
        # Vérifier les logs
        with open(self.sync_log, 'r') as f:
            sync_logs = f.read()
            self.assertIn("Transformation du client WooCommerce #1", sync_logs)
            self.assertIn("Client #1 transformé avec succès", sync_logs)
        
        # Test avec des données invalides
        invalid_customer = {
            'id': 2,
            'email': 'invalid-email'
        }
        
        # Vérifier que la transformation échoue
        with self.assertRaises(TransformationError):
            transformer.transform(invalid_customer)
        
        # Vérifier les logs d'erreur
        with open(self.errors_log, 'r') as f:
            error_logs = f.read()
            self.assertIn("Données de client invalides", error_logs)
    
    def test_validator_logging(self):
        """Test du logging dans le validateur."""
        validator = DataValidator()
        
        # Test avec des données valides
        valid_order = {
            'id': 1,
            'customer_id': 1,
            'total': '100.00',
            'line_items': [
                {
                    'total': '100.00'
                }
            ]
        }
        
        # Valider la commande
        result = validator.validate_order(valid_order)
        
        # Vérifier le résultat
        self.assertTrue(result)
        
        # Vérifier les logs
        with open(self.sync_log, 'r') as f:
            sync_logs = f.read()
            self.assertIn("Validation de la commande #1", sync_logs)
            self.assertIn("Commande #1 validée avec succès", sync_logs)
        
        # Test avec des données invalides
        invalid_order = {
            'id': 2,
            'total': '100.00',
            'line_items': [
                {
                    'total': '200.00'  # Montant incohérent
                }
            ]
        }
        
        # Vérifier que la validation échoue
        with self.assertRaises(ValidationError):
            validator.validate_order(invalid_order)
        
        # Vérifier les logs d'erreur
        with open(self.errors_log, 'r') as f:
            error_logs = f.read()
            self.assertIn("Champs manquants dans la commande: customer_id", error_logs)

if __name__ == '__main__':
    unittest.main() 