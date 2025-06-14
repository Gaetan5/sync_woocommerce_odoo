"""
Module de mapping des clients entre WooCommerce et Odoo.
Ce module gère la transformation des données clients
entre les formats WooCommerce et Odoo.
"""

def map_wc_customer_to_odoo(wc_customer):
    """
    Convertit un client WooCommerce en format Odoo.
    
    Cette fonction transforme la structure de données d'un client
    WooCommerce en une structure compatible avec l'API Odoo.
    
    Structure du client Odoo :
    - name : Nom complet du client
    - email : Adresse email
    - phone : Numéro de téléphone
    - street : Adresse
    - city : Ville
    - zip : Code postal
    - country_id : ID du pays
    
    Args:
        wc_customer (dict): Client au format WooCommerce
        
    Returns:
        dict: Client au format Odoo
    """
    return {
        "name": f"{wc_customer.get('first_name', '')} {wc_customer.get('last_name', '')}".strip(),
        "email": wc_customer.get("email", ""),
        "phone": wc_customer.get("billing", {}).get("phone", ""),
        "street": wc_customer.get("billing", {}).get("address_1", ""),
        "city": wc_customer.get("billing", {}).get("city", ""),
        "zip": wc_customer.get("billing", {}).get("postcode", ""),
        "country_id": wc_customer.get("billing", {}).get("country", "")
    }

def map_odoo_customer_to_wc(odoo_customer):
    """
    Convertit un client Odoo en format WooCommerce.
    
    Cette fonction transforme la structure de données d'un client
    Odoo en une structure compatible avec l'API WooCommerce.
    
    Args:
        odoo_customer (dict): Client au format Odoo
        
    Returns:
        dict: Client au format WooCommerce
    """
    # Séparation du nom complet en prénom et nom
    name_parts = odoo_customer.get("name", "").split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": odoo_customer.get("email", ""),
        "billing": {
            "phone": odoo_customer.get("phone", ""),
            "address_1": odoo_customer.get("street", ""),
            "city": odoo_customer.get("city", ""),
            "postcode": odoo_customer.get("zip", ""),
            "country": odoo_customer.get("country_id", "")
        }
    }
