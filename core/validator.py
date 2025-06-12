def validate_order(order):
    required_fields = ["customer_id", "line_items"]
    for field in required_fields:
        if field not in order or not order[field]:
            raise ValueError(f"Champ obligatoire manquant ou vide : {field}")
    if not isinstance(order["line_items"], list) or not order["line_items"]:
        raise ValueError("La commande doit contenir au moins un article.")
    # Ajoute d'autres validations selon tes besoins
    return True

def validate_customer(customer):
    required_fields = ["email", "first_name", "last_name"]
    for field in required_fields:
        if field not in customer or not customer[field]:
            raise ValueError(f"Champ client obligatoire manquant ou vide : {field}")
    return True
