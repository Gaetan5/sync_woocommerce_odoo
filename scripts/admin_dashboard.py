from flask import Flask, send_file, render_template_string, redirect, url_for, Response
import os
import subprocess
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from dotenv import load_dotenv
import time

app = Flask(__name__)

# Charger les variables d'environnement
load_dotenv()

# Initialiser Sentry si DSN présent
ds = os.getenv('SENTRY_DSN')
if ds:
    sentry_sdk.init(
        dsn=ds,
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.5,  # Ajuster selon besoin
        environment=os.getenv('ENV', 'development')
    )

# Stocker le démarrage pour l'uptime
start_time = time.time()
sync_count = 0

@app.route('/')
def index():
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
    audit_path = os.path.join(os.path.dirname(__file__), '../sync_audit.csv')
    if os.path.exists(audit_path):
        return send_file(audit_path, as_attachment=True)
    return 'Aucun audit disponible.'

@app.route('/purge')
def purge():
    subprocess.call(['python', 'scripts/purge_local_data.py'])
    return redirect(url_for('index'))

@app.route('/sync')
def sync():
    global sync_count
    subprocess.Popen(['python', 'scripts/sync_orders.py'])
    sync_count += 1
    return redirect(url_for('index'))

@app.route('/metrics')
def metrics():
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
    app.run(host='0.0.0.0', port=8081)
