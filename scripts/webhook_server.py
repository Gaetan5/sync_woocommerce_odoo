from flask import Flask, request, jsonify
import os
import subprocess
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from dotenv import load_dotenv

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

@app.route('/webhook', methods=['POST'])
def webhook():
    # Ici, on pourrait vérifier la signature du webhook pour la sécurité
    data = request.json
    # Déclenche la synchronisation (en tâche de fond)
    subprocess.Popen(['python', 'scripts/sync_orders.py'])
    return jsonify({'status': 'sync triggered'}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
