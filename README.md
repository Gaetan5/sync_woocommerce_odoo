# sync_woocommerce_odoo

Synchronisation automatisée des commandes et clients entre WooCommerce et Odoo.

## Structure du projet

- `config/` : Configuration (API, logs)
- `core/` : Logique métier et mapping
- `utils/` : Outils communs
- `scripts/` : Points d'entrée
- `tests/` : Tests unitaires

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

1. Copiez le fichier `.env.example` en `.env` à la racine du projet :
   ```bash
   cp .env.example .env
   ```
2. Renseignez vos identifiants WooCommerce et Odoo dans `.env` :
   - WC_API_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET
   - ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD

## Utilisation

```bash
python scripts/sync_orders.py
```

## Déploiement avec Docker

Pour lancer la synchronisation dans un conteneur Docker :

```bash
docker-compose build
docker-compose up
```

- Le fichier `.env` doit être présent à la racine du projet.
- Les logs et la base locale seront persistés dans le dossier du projet.

Pour arrêter et supprimer les conteneurs :
```bash
docker-compose down
```

Vous pouvez personnaliser le service Odoo dans `docker-compose.yml` si besoin.

## Tests unitaires

Pour lancer tous les tests :
```bash
pytest tests/
```

## Dépannage
- **Erreur "Variables d'environnement manquantes"** : vérifiez que le fichier `.env` est bien présent et complété.
- **Problème d'import** : assurez-vous d'utiliser l'environnement virtuel Python du projet.
- **Connexion refusée** : vérifiez l’URL et les identifiants de vos APIs.

## Audit et monitoring

Chaque synchronisation de commande (succès, doublon, erreur) est enregistrée dans le fichier `sync_audit.csv` à la racine du projet.

- **Colonnes** : date ISO, order_id, statut (`success`, `ignored`, `error`), message
- **Utilité** : permet de suivre l’historique, d’auditer les erreurs, d’exporter pour reporting ou monitoring
- **Exemple d’entrée** :
  ```csv
  2025-06-12T14:23:01.123456,12345,success,Synchronisation OK
  2025-06-12T14:23:02.654321,12346,error,Erreur de mapping
  ```

Pour consulter l’audit :
```bash
cat sync_audit.csv
```

Pour automatiser l’analyse ou l’export, utilisez un tableur ou un outil de BI.

## Monitoring des erreurs (Sentry)

Pour activer le monitoring des erreurs avec Sentry :

1. Créez un compte sur [https://sentry.io/](https://sentry.io/) et créez un projet Python.
2. Récupérez le DSN Sentry et ajoutez-le dans votre fichier `.env` :

   ```env
   SENTRY_DSN=https://...@sentry.io/...
   ```

3. Relancez le dashboard admin Flask ou tout autre script utilisant Flask.

En cas d’erreur non gérée, un rapport sera envoyé à Sentry automatiquement.

## Monitoring et métriques Prometheus

Le dashboard admin expose un endpoint `/metrics` compatible Prometheus :

- `app_uptime_seconds` : uptime du dashboard en secondes
- `app_sync_count` : nombre de synchronisations lancées via l’interface

Exemple d’utilisation avec Prometheus :

```yaml
scrape_configs:
  - job_name: 'sync_dashboard'
    static_configs:
      - targets: ['localhost:8081']
```

Vous pouvez visualiser les métriques en visitant : [http://localhost:8081/metrics](http://localhost:8081/metrics)

## Contribution
Les PR et suggestions sont les bienvenues !
