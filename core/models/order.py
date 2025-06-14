"""
Module de mapping des commandes entre WooCommerce et Odoo.
Ce module contient les fonctions de transformation des données
de commandes du format WooCommerce vers le format Odoo.
"""

def map_wc_order_to_odoo(wc_order):
    """
    Convertit une commande WooCommerce en format Odoo.
    
    Cette fonction transforme la structure de données d'une commande
    WooCommerce en une structure compatible avec l'API Odoo.
    
    Structure de la commande Odoo :
    - partner_id : ID du client dans Odoo
    - order_line : Liste des lignes de commande au format Odoo
        - product_id : ID du produit
        - product_uom_qty : Quantité
        - price_unit : Prix unitaire
    
    Args:
        wc_order (dict): Commande au format WooCommerce
        
    Returns:
        dict: Commande au format Odoo
        
    Note:
        Le partner_id doit être adapté pour utiliser l'ID Odoo
        correspondant au client WooCommerce.
    """
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