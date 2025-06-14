import logging
import logging.config
import os

# Charger la configuration
LOGGING_CONF = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config/logging.conf'))
logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs'))

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

defaults = {'log_dir': logs_dir}
logging.config.fileConfig(LOGGING_CONF, defaults=defaults, disable_existing_loggers=False)

logger = logging.getLogger('sync_woocommerce_odoo')

logger.info('Test manuel de création du fichier de log.')
logger.error('Erreur test manuel.')

# Forcer le flush de tous les handlers
for handler in logger.handlers:
    handler.flush()

print('Log écrit. Vérifiez logs/sync.log et logs/errors.log.') 