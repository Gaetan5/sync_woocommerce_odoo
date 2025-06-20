import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from core.validator import validate_order

def test_validate_order_ok():
    order = {"id": 1, "customer_id": 1, "total": 20.0, "line_items": [
        {"product_id": 1, "quantity": 2, "total": 20.0}
    ]}
    assert validate_order(order) is True

def test_validate_order_missing_customer():
    order = {"id": 2, "total": 10.0, "line_items": [{"product_id": 1, "quantity": 2}]}
    with pytest.raises(Exception):
        validate_order(order)

def test_validate_order_empty_lines():
    order = {"id": 3, "customer_id": 1, "total": 10.0, "line_items": []}
    with pytest.raises(Exception):
        validate_order(order)
