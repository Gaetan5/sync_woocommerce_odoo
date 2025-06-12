def map_wc_order_to_odoo(wc_order):
    """Convertit une commande WooCommerce en format Odoo."""
    return {
        "partner_id": wc_order["customer_id"],  # À adapter (chercher ou créer le client)
        "order_line": [
            (0, 0, {
                "product_id": item["product_id"],
                "product_uom_qty": item["quantity"],
                "price_unit": item["price"]
            }) for item in wc_order["line_items"]
        ]
    }