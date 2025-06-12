import logging.config
import os

LOGGING_CONFIG = os.path.join(os.path.dirname(__file__), '../config/logging.conf')
logging.config.fileConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
