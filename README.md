# sync_woocommerce_odoo

Synchronisation automatisée des commandes et clients entre WooCommerce et Odoo.

## Structure du projet

- `config/` : Configuration (API, logs)
- `core/` : Logique métier et mapping
- `utils/` : Outils communs
- `scripts/` : Points d'entrée

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

```bash
python scripts/sync_orders.py
```
