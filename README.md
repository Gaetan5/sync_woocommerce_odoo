# sync_woocommerce_odoo

Synchronisation automatisée des commandes et clients entre WooCommerce et Odoo.

## Activer l'environnement virtuel 

 -python3 -m venv venv && source venv/bin/activate 

## Structure du projet

- `config/` : Configuration (API, logs)
- `core/` : Logique métier et mapping
- `utils/` : Outils communs
- `scripts/` : Points d'entrée
- `tests/` : Tests unitaires

## Patterns et Bonnes Pratiques

### 1. Gestion des Variables d'Environnement
- Utilisation de `python-dotenv` pour charger les variables d'environnement
- Fichier `.env` pour les valeurs sensibles (non versionné)
- Fichier `.env.example` comme template (versionné)
- Validation des variables requises au démarrage

Exemple de structure `.env.example` :
```env
# WooCommerce API
WC_API_URL=https://votre-site.com/wp-json/wc/v3
WC_CONSUMER_KEY=votre_consumer_key
WC_CONSUMER_SECRET=votre_consumer_secret

# Odoo API
ODOO_URL=https://votre-odoo.com
ODOO_DB=votre_base
ODOO_USER=votre_user
ODOO_PASSWORD=votre_password

# Configuration
SYNC_INTERVAL=300  # en secondes
BATCH_SIZE=50      # nombre d'éléments par synchronisation
```

### 2. Logging
- Configuration centralisée dans `config/logging.conf`
- Différents niveaux de logs (DEBUG, INFO, WARNING, ERROR)
- Rotation des fichiers de logs
- Format standardisé : `%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s`
- Séparation des logs d'erreur dans un fichier dédié

Exemple d'utilisation :
```python
from utils.logging_utils import log_info, log_error, log_procedure

@log_procedure("Synchronisation des commandes")
def sync_orders():
    log_info("Début de la synchronisation")
    try:
        # ... code de synchronisation ...
    except Exception as e:
        log_error("Erreur lors de la synchronisation", exc_info=e)
```

### 3. Gestion des Erreurs
- Exceptions personnalisées dans `core/exceptions.py`
- Try/except avec logging approprié
- Validation des données avec messages d'erreur explicites
- Monitoring des erreurs avec Sentry

Exemple d'exceptions personnalisées :
```python
class SyncError(Exception):
    """Erreur générique de synchronisation"""
    pass

class ValidationError(SyncError):
    """Erreur de validation des données"""
    pass

class TransformationError(SyncError):
    """Erreur lors de la transformation des données"""
    pass
```

### 4. Tests
- Tests unitaires avec `pytest`
- Tests d'intégration pour les flux complets
- Mocks pour les appels API
- Fixtures réutilisables
- Assertions détaillées

#### Types de Tests

1. **Tests Unitaires**
```python
# tests/test_transformers.py
def test_order_transformation():
    transformer = OrderTransformer()
    wc_order = {
        'id': 1,
        'total': '100.00',
        'line_items': [...]
    }
    odoo_order = transformer.transform(wc_order)
    assert odoo_order['amount_total'] == 100.00
```

2. **Tests d'Intégration**
```python
# tests/test_integration.py
def test_full_sync_flow():
    sync_manager = SyncManager()
    result = sync_manager.sync_orders()
    assert result['status'] == 'success'
    assert result['synced_count'] > 0
```

3. **Tests de Validation**
```python
# tests/test_validator.py
def test_order_validation():
    validator = DataValidator()
    order = {
        'id': 1,
        'total': '100.00',
        'customer_id': 123
    }
    assert validator.validate_order(order) is True
```

4. **Tests de Performance**
```python
# tests/test_performance.py
def test_sync_performance():
    start_time = time.time()
    sync_manager = SyncManager()
    sync_manager.sync_orders()
    duration = time.time() - start_time
    assert duration < 5.0  # La synchronisation doit prendre moins de 5 secondes
```

5. **Tests de Gestion d'Erreurs**
```python
# tests/test_error_handling.py
def test_invalid_order_handling():
    transformer = OrderTransformer()
    with pytest.raises(TransformationError):
        transformer.transform({})  # Commande vide
```

6. **Tests de Logging**
```python
# tests/test_logging.py
def test_logging_output():
    with LogCapture() as logs:
        log_info("Test message")
        assert "Test message" in logs.records[0].message
```

#### Fixtures Réutilisables
```python
# tests/conftest.py
@pytest.fixture
def sample_wc_order():
    return {
        'id': 1,
        'total': '100.00',
        'customer_id': 123,
        'line_items': [
            {'product_id': 1, 'quantity': 2, 'total': '50.00'}
        ]
    }

@pytest.fixture
def mock_wc_client(mocker):
    return mocker.patch('core.wc_client.WooCommerceClient')
```

#### Mocks et Stubs
```python
# tests/test_wc_client.py
def test_get_orders(mock_wc_client):
    mock_wc_client.get_orders.return_value = [
        {'id': 1, 'total': '100.00'}
    ]
    client = WooCommerceClient()
    orders = client.get_orders()
    assert len(orders) == 1
    assert orders[0]['total'] == '100.00'
```

#### Assertions Avancées
```python
# tests/test_transformations.py
def test_complex_transformation():
    transformer = OrderTransformer()
    wc_order = sample_wc_order()
    odoo_order = transformer.transform(wc_order)
    
    # Vérification des champs obligatoires
    assert all(key in odoo_order for key in ['name', 'partner_id', 'amount_total'])
    
    # Vérification des calculs
    assert odoo_order['amount_total'] == 100.00
    assert len(odoo_order['order_line']) == 1
    
    # Vérification des relations
    assert odoo_order['partner_id'] == 123
```

#### Tests Paramétrés
```python
# tests/test_validator.py
@pytest.mark.parametrize("order,expected", [
    ({'id': 1, 'total': '100.00'}, False),  # Manque customer_id
    ({'id': 1, 'total': '100.00', 'customer_id': 123}, True),
    ({'id': 1, 'total': '-100.00', 'customer_id': 123}, False),  # Montant négatif
])
def test_order_validation_cases(order, expected):
    validator = DataValidator()
    assert validator.validate_order(order) == expected
```

#### Tests de Couverture
```bash
# Exécution des tests avec couverture
pytest --cov=core --cov-report=html tests/
```

#### Tests de Performance
```python
# tests/test_performance.py
@pytest.mark.benchmark
def test_batch_processing(benchmark):
    def process_batch():
        sync_manager = SyncManager()
        return sync_manager.sync_orders_batch(100)
    
    result = benchmark(process_batch)
    assert result['duration'] < 1.0  # Moins d'une seconde par lot
```

### 5. Architecture
- Pattern Repository pour l'accès aux données
- Pattern Factory pour la création d'objets
- Pattern Strategy pour les différentes stratégies de synchronisation
- Pattern Observer pour le monitoring
- Pattern Decorator pour le logging des procédures

Exemple de Factory :
```python
class TransformerFactory:
    @staticmethod
    def get_transformer(data_type: str) -> BaseTransformer:
        if data_type == 'order':
            return OrderTransformer()
        elif data_type == 'customer':
            return CustomerTransformer()
        raise ValueError(f"Type de données non supporté: {data_type}")
```

### 6. Sécurité
- Validation des entrées
- Gestion sécurisée des credentials
- Rate limiting sur les appels API
- Logging sécurisé (pas de données sensibles)

Exemple de validation :
```python
def validate_api_credentials(credentials: dict) -> bool:
    required_fields = ['url', 'key', 'secret']
    return all(field in credentials for field in required_fields)
```

### 7. Performance
- Mise en cache des données fréquemment utilisées
- Batch processing pour les synchronisations
- Monitoring des performances avec Prometheus
- Optimisation des requêtes API

Exemple de batch processing :
```python
def sync_orders_batch(orders: List[dict], batch_size: int = 50):
    for i in range(0, len(orders), batch_size):
        batch = orders[i:i + batch_size]
        process_batch(batch)
```

### 8. Documentation
- Docstrings au format Google
- Documentation technique avec MkDocs
- Commentaires explicatifs pour le code complexe
- README détaillé

Exemple de docstring :
```python
def transform_order(wc_order: dict) -> dict:
    """Transforme une commande WooCommerce en format Odoo.
    
    Args:
        wc_order (dict): Commande WooCommerce à transformer
        
    Returns:
        dict: Commande au format Odoo
        
    Raises:
        TransformationError: Si la transformation échoue
    """
```

### 9. CI/CD
- Tests automatisés avec GitHub Actions
- Vérification de la qualité du code
- Déploiement automatisé
- Gestion des versions

Exemple de workflow GitHub Actions :
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest tests/
```

### 10. Monitoring
- Métriques Prometheus
- Logs structurés
- Alertes configurables
- Dashboard de monitoring

Exemple de métrique Prometheus :
```python
from prometheus_client import Counter, Gauge

sync_counter = Counter('sync_operations_total', 'Nombre total de synchronisations')
sync_duration = Gauge('sync_duration_seconds', 'Durée des synchronisations')
```

### 11. Patterns de Synchronisation
- Gestion des conflits de données
- Stratégies de résolution des doublons
- Mise à jour atomique des données
- Gestion des timeouts et retries

Exemple de stratégie de résolution :
```python
def resolve_conflict(local_data: dict, remote_data: dict) -> dict:
    """Résout les conflits entre données locales et distantes."""
    if local_data['updated_at'] > remote_data['updated_at']:
        return local_data
    return remote_data
```

### 12. Gestion des États
- Machine à états pour le suivi des synchronisations
- Persistance des états de synchronisation
- Reprise sur erreur
- Historique des états

Exemple de machine à états :
```python
class SyncState(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
```

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
- **Connexion refusée** : vérifiez l'URL et les identifiants de vos APIs.

## Audit et monitoring

Chaque synchronisation de commande (succès, doublon, erreur) est enregistrée dans le fichier `sync_audit.csv` à la racine du projet.

- **Colonnes** : date ISO, order_id, statut (`success`, `ignored`, `error`), message
- **Utilité** : permet de suivre l'historique, d'auditer les erreurs, d'exporter pour reporting ou monitoring
- **Exemple d'entrée** :
  ```csv
  2025-06-12T14:23:01.123456,12345,success,Synchronisation OK
  2025-06-12T14:23:02.654321,12346,error,Erreur de mapping
  ```

Pour consulter l'audit :
```bash
cat sync_audit.csv
```

Pour automatiser l'analyse ou l'export, utilisez un tableur ou un outil de BI.

## Monitoring des erreurs (Sentry)

Pour activer le monitoring des erreurs avec Sentry :

1. Créez un compte sur [https://sentry.io/](https://sentry.io/) et créez un projet Python.
2. Récupérez le DSN Sentry et ajoutez-le dans votre fichier `.env` :

   ```env
   SENTRY_DSN=https://...@sentry.io/...
   ```

3. Relancez le dashboard admin Flask ou tout autre script utilisant Flask.

En cas d'erreur non gérée, un rapport sera envoyé à Sentry automatiquement.

## Monitoring et métriques Prometheus

Le dashboard admin expose un endpoint `/metrics` compatible Prometheus :

- `app_uptime_seconds` : uptime du dashboard en secondes
- `app_sync_count` : nombre de synchronisations lancées via l'interface

Exemple d'utilisation avec Prometheus :

```yaml
scrape_configs:
  - job_name: 'sync_dashboard'
    static_configs:
      - targets: ['localhost:8081']
```

Vous pouvez visualiser les métriques en visitant : [http://localhost:8081/metrics](http://localhost:8081/metrics)

## Contribution
Les PR et suggestions sont les bienvenues !
