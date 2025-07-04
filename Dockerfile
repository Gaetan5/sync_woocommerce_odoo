# Dockerfile pour sync_woocommerce_odoo
FROM python:3.12-bookworm

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "scripts/sync_orders.py"]