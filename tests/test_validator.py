import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from core.validator import validate_order

def test_validate_order_ok():
    order = {"customer_id": 1, "line_items": [{"product_id": 1, "quantity": 2}]}
    assert validate_order(order) is True

def test_validate_order_missing_customer():
    order = {"line_items": [{"product_id": 1, "quantity": 2}]}
    with pytest.raises(ValueError):
        validate_order(order)

def test_validate_order_empty_lines():
    order = {"customer_id": 1, "line_items": []}
    with pytest.raises(ValueError):
        validate_order(order)
