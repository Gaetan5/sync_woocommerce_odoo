from flask import Flask, jsonify
import os
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

@app.route('/health')
def health():
    # Vérifie la présence des fichiers critiques
    db_exists = os.path.exists(os.path.join(os.path.dirname(__file__), '../sync_local.db'))
    return jsonify({
        'status': 'ok',
        'db_exists': db_exists
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
