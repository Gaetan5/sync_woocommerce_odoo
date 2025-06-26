"""
Module de collecte de métriques pour la synchronisation.
Expose des compteurs et timers pour Prometheus ou logs custom.
"""

from prometheus_client import Counter, Histogram, start_http_server
import time

# Compteurs de succès/erreurs
sync_success_counter = Counter('sync_success_total', 'Nombre de synchronisations réussies')
sync_error_counter = Counter('sync_error_total', 'Nombre de synchronisations échouées')

# Histogramme de durée de synchronisation
sync_duration_histogram = Histogram('sync_duration_seconds', 'Durée de la synchronisation (s)')

def start_metrics_server(port=8001):
    """Démarre un serveur HTTP pour exposer les métriques Prometheus."""
    start_http_server(port)

# Exemple d'utilisation dans le code principal :
# with sync_duration_histogram.time():
#     ... synchronisation ...
# sync_success_counter.inc()
# sync_error_counter.inc()
