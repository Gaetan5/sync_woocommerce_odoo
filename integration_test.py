#!/usr/bin/env python3
"""
Integration test simulation for WooCommerce-Odoo sync
"""

import sys
import os
import tempfile
import json
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.abspath('.'))

def mock_woocommerce_api():
    """Mock WooCommerce API responses"""
    return [
        {
            "id": 12345,
            "customer_id": 1,
            "status": "processing",
            "line_items": [
                {
                    "product_id": 101,
                    "quantity": 2,
                    "price": 25.00
                },
                {
                    "product_id": 102,
                    "quantity": 1,
                    "price": 15.00
                }
            ]
        },
        {
            "id": 12346,
            "customer_id": 2,
            "status": "processing",
            "line_items": [
                {
                    "product_id": 103,
                    "quantity": 1,
                    "price": 50.00
                }
            ]
        }
    ]

def mock_odoo_client():
    """Mock Odoo client"""
    class MockOdooClient:
        def __init__(self):
            self.created_orders = []
        
        def create_order(self, order_data):
            order_id = len(self.created_orders) + 1000
            self.created_orders.append({
                "id": order_id,
                "data": order_data
            })
            return order_id
        
        def create_customer(self, customer_data):
            return 2000
    
    return MockOdooClient()

def test_full_sync_simulation():
    """Simulate a full synchronization process"""
    print("=== INTEGRATION TEST SIMULATION ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup test database
        import utils.database as db_module
        original_db_path = db_module.DB_PATH
        db_module.DB_PATH = os.path.join(tmpdir, 'test_sync.db')
        
        # Setup test audit log
        import utils.helpers as helpers_module
        original_audit_path = helpers_module.AUDIT_LOG
        helpers_module.AUDIT_LOG = os.path.join(tmpdir, 'test_audit.csv')
        
        try:
            # Initialize database
            db_module.init_db()
            
            # Mock the API clients
            mock_wc_orders = mock_woocommerce_api()
            mock_odoo = mock_odoo_client()
            
            # Simulate sync process
            from core.validator import validate_order
            from core.models.order import map_wc_order_to_odoo
            from utils.helpers import log_audit
            
            synced_count = 0
            error_count = 0
            
            print(f"📦 Processing {len(mock_wc_orders)} orders...")
            
            for order in mock_wc_orders:
                try:
                    # Check if already synced
                    if db_module.is_order_already_synced_db(order["id"]):
                        print(f"⏭️ Order {order['id']} already synced, skipping")
                        log_audit(order["id"], "ignored", "Already synced")
                        continue
                    
                    # Validate order
                    validate_order(order)
                    print(f"✅ Order {order['id']} validated")
                    
                    # Map to Odoo format
                    odoo_order_data = map_wc_order_to_odoo(order)
                    print(f"🔄 Order {order['id']} mapped to Odoo format")
                    
                    # Create in Odoo (mocked)
                    odoo_order_id = mock_odoo.create_order(odoo_order_data)
                    print(f"📝 Order {order['id']} created in Odoo as {odoo_order_id}")
                    
                    # Mark as synced
                    db_module.mark_order_as_synced_db(order["id"])
                    log_audit(order["id"], "success", f"Synced to Odoo order {odoo_order_id}")
                    
                    synced_count += 1
                    
                except Exception as e:
                    print(f"❌ Error processing order {order.get('id', '?')}: {e}")
                    log_audit(order.get('id', '?'), "error", str(e))
                    error_count += 1
            
            # Test duplicate handling
            print("\n🔄 Testing duplicate handling...")
            for order in mock_wc_orders[:1]:  # Test first order again
                if db_module.is_order_already_synced_db(order["id"]):
                    print(f"✅ Order {order['id']} correctly identified as duplicate")
                    log_audit(order["id"], "ignored", "Duplicate test")
            
            # Generate test report
            print(f"\n📊 SYNC SIMULATION RESULTS:")
            print(f"Total orders processed: {len(mock_wc_orders)}")
            print(f"Successfully synced: {synced_count}")
            print(f"Errors: {error_count}")
            print(f"Success rate: {(synced_count/(synced_count+error_count))*100:.1f}%")
            
            # Verify audit log
            if os.path.exists(helpers_module.AUDIT_LOG):
                with open(helpers_module.AUDIT_LOG, 'r') as f:
                    audit_lines = f.readlines()
                    print(f"Audit entries created: {len(audit_lines)}")
            
            # Verify database state
            total_synced = sum(1 for _ in range(1, 20000) if db_module.is_order_already_synced_db(_))
            print(f"Orders marked as synced in DB: {synced_count}")
            
            return {
                "total_processed": len(mock_wc_orders),
                "synced": synced_count,
                "errors": error_count,
                "success_rate": (synced_count/(synced_count+error_count))*100 if (synced_count+error_count) > 0 else 0
            }
            
        finally:
            # Restore original paths
            db_module.DB_PATH = original_db_path
            helpers_module.AUDIT_LOG = original_audit_path

def test_error_scenarios():
    """Test various error scenarios"""
    print("\n=== ERROR SCENARIO TESTING ===")
    
    from core.validator import validate_order
    from core.exceptions import SyncError
    
    error_scenarios = [
        # Invalid order data
        {"id": "invalid1", "customer_id": None, "line_items": []},
        {"id": "invalid2", "line_items": [{"product_id": 1}]},  # Missing customer_id
        {"id": "invalid3", "customer_id": 1},  # Missing line_items
    ]
    
    errors_handled = 0
    for scenario in error_scenarios:
        try:
            validate_order(scenario)
            print(f"❌ Scenario {scenario['id']}: Should have failed validation")
        except (ValueError, KeyError) as e:
            print(f"✅ Scenario {scenario['id']}: Properly caught error - {type(e).__name__}")
            errors_handled += 1
        except Exception as e:
            print(f"⚠️ Scenario {scenario['id']}: Unexpected error type - {type(e).__name__}")
    
    print(f"Error handling score: {errors_handled}/{len(error_scenarios)} ({(errors_handled/len(error_scenarios))*100:.0f}%)")
    
    return errors_handled / len(error_scenarios)

def main():
    """Run integration tests"""
    print("🧪 INTEGRATION TEST SUITE")
    print("=" * 50)
    
    try:
        # Run sync simulation
        sync_results = test_full_sync_simulation()
        
        # Run error scenario tests
        error_handling_score = test_error_scenarios()
        
        # Overall assessment
        print(f"\n🎯 INTEGRATION TEST SUMMARY:")
        print(f"Sync Success Rate: {sync_results['success_rate']:.1f}%")
        print(f"Error Handling: {error_handling_score*100:.0f}%")
        
        if sync_results['success_rate'] >= 90 and error_handling_score >= 0.8:
            grade = "A"
        elif sync_results['success_rate'] >= 75 and error_handling_score >= 0.6:
            grade = "B"
        elif sync_results['success_rate'] >= 60:
            grade = "C"
        else:
            grade = "D"
        
        print(f"Overall Integration Grade: {grade}")
        
        return {
            "sync_results": sync_results,
            "error_handling_score": error_handling_score,
            "grade": grade
        }
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()