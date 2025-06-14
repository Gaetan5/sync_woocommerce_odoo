"""
Dashboard d'administration pour la synchronisation WooCommerce ↔ Odoo.
Ce module fournit une interface web simple pour :
- Visualiser et télécharger les logs d'audit
- Purger la base de données locale et les logs
- Lancer des synchronisations manuelles
- Exposer des métriques pour Prometheus
"""

from flask import Flask, send_file, render_template_string, redirect, url_for, Response
import os
import subprocess
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from dotenv import load_dotenv
import time

# Initialisation de l'application Flask
app = Flask(__name__)

# Chargement des variables d'environnement depuis .env
load_dotenv()

# Configuration de Sentry pour le monitoring des erreurs
ds = os.getenv('SENTRY_DSN')
if ds:
    sentry_sdk.init(
        dsn=ds,
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.5,  # Ajuster selon besoin
        environment=os.getenv('ENV', 'development')
    )

# Variables globales pour les métriques
start_time = time.time()  # Timestamp de démarrage pour l'uptime
sync_count = 0  # Compteur de synchronisations

@app.route('/')
def index():
    """
    Page d'accueil du dashboard.
    Affiche les liens vers les différentes fonctionnalités.
    """
    return render_template_string('''
    <h1>Sync WooCommerce ↔ Odoo</h1>
    <ul>
      <li><a href="/audit">Télécharger l'audit</a></li>
      <li><a href="/purge">Purger la base locale et l'audit</a></li>
      <li><a href="/sync">Lancer une synchronisation</a></li>
    </ul>
    ''')

@app.route('/audit')
def audit():
    """
    Télécharge le fichier d'audit CSV.
    Le fichier contient l'historique des synchronisations.
    """
    audit_path = os.path.join(os.path.dirname(__file__), '../sync_audit.csv')
    if os.path.exists(audit_path):
        return send_file(audit_path, as_attachment=True)
    return 'Aucun audit disponible.'

@app.route('/purge')
def purge():
    """
    Lance le script de purge des données locales.
    Supprime la base SQLite et le fichier d'audit.
    """
    subprocess.call(['python', 'scripts/purge_local_data.py'])
    return redirect(url_for('index'))

@app.route('/sync')
def sync():
    """
    Lance une synchronisation manuelle.
    Incrémente le compteur de synchronisations.
    """
    global sync_count
    subprocess.Popen(['python', 'scripts/sync_orders.py'])
    sync_count += 1
    return redirect(url_for('index'))

@app.route('/metrics')
def metrics():
    """
    Endpoint Prometheus pour les métriques.
    Expose :
    - Uptime du dashboard
    - Nombre de synchronisations lancées
    """
    uptime = int(time.time() - start_time)
    metrics = f"""
# HELP app_uptime_seconds Uptime du dashboard en secondes
# TYPE app_uptime_seconds counter
app_uptime_seconds {uptime}
# HELP app_sync_count Nombre de synchronisations lancées via le dashboard
# TYPE app_sync_count counter
app_sync_count {sync_count}
"""
    return Response(metrics, mimetype='text/plain')

if __name__ == '__main__':
    # Démarrage du serveur Flask sur le port 8081
    app.run(host='0.0.0.0', port=8081)
