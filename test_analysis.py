#!/usr/bin/env python3
"""
Comprehensive analysis of the WooCommerce-Odoo sync project
"""

import os
import sys
import time
import sqlite3
import tempfile
from datetime import datetime
import json

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

def analyze_project_structure():
    """Analyze project structure and organization"""
    print("=== PROJECT STRUCTURE ANALYSIS ===")
    
    structure = {
        "config": ["settings.py", "logging.conf"],
        "core": ["sync_manager.py", "odoo_client.py", "validator.py", "exceptions.py", "wc_client.py"],
        "core/models": ["order.py", "customer.py"],
        "utils": ["database.py", "helpers.py", "logger.py"],
        "scripts": ["sync_orders.py", "purge_local_data.py"],
        "tests": ["test_validator.py", "test_database.py", "test_audit.py"]
    }
    
    missing_files = []
    for folder, files in structure.items():
        for file in files:
            path = os.path.join(folder, file)
            if not os.path.exists(path):
                missing_files.append(path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All expected files present")
        return True

def analyze_code_quality():
    """Analyze code quality and potential issues"""
    print("\n=== CODE QUALITY ANALYSIS ===")
    
    issues = []
    
    # Check imports and dependencies
    try:
        from core.sync_manager import SyncManager
        from core.validator import validate_order, validate_customer
        from utils.database import init_db, is_order_already_synced_db
        from utils.helpers import log_audit
        print("✅ All imports working correctly")
    except ImportError as e:
        issues.append(f"Import error: {e}")
    
    # Check configuration validation
    try:
        from config.settings import validate_settings
        print("✅ Configuration validation available")
    except Exception as e:
        issues.append(f"Configuration issue: {e}")
    
    return issues

def test_database_performance():
    """Test database operations performance"""
    print("\n=== DATABASE PERFORMANCE TEST ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Override database path for testing
        import utils.database as db_module
        original_path = db_module.DB_PATH
        db_module.DB_PATH = os.path.join(tmpdir, 'test_perf.db')
        
        try:
            # Initialize database
            start_time = time.time()
            db_module.init_db()
            init_time = time.time() - start_time
            print(f"✅ Database initialization: {init_time:.4f}s")
            
            # Test bulk operations
            start_time = time.time()
            for i in range(1000):
                db_module.mark_order_as_synced_db(f"order_{i}")
            bulk_insert_time = time.time() - start_time
            print(f"✅ 1000 order inserts: {bulk_insert_time:.4f}s ({1000/bulk_insert_time:.0f} ops/sec)")
            
            # Test lookup performance
            start_time = time.time()
            for i in range(100):
                db_module.is_order_already_synced_db(f"order_{i}")
            lookup_time = time.time() - start_time
            print(f"✅ 100 order lookups: {lookup_time:.4f}s ({100/lookup_time:.0f} ops/sec)")
            
        finally:
            db_module.DB_PATH = original_path
    
    return {
        "init_time": init_time,
        "bulk_insert_rate": 1000/bulk_insert_time,
        "lookup_rate": 100/lookup_time
    }

def test_validation_performance():
    """Test validation functions performance"""
    print("\n=== VALIDATION PERFORMANCE TEST ===")
    
    from core.validator import validate_order, validate_customer
    
    # Test order validation
    valid_order = {
        "customer_id": 123,
        "line_items": [
            {"product_id": 1, "quantity": 2, "price": 10.0},
            {"product_id": 2, "quantity": 1, "price": 15.0}
        ]
    }
    
    start_time = time.time()
    for _ in range(10000):
        validate_order(valid_order)
    validation_time = time.time() - start_time
    print(f"✅ 10,000 order validations: {validation_time:.4f}s ({10000/validation_time:.0f} ops/sec)")
    
    # Test customer validation
    valid_customer = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    start_time = time.time()
    for _ in range(10000):
        validate_customer(valid_customer)
    customer_validation_time = time.time() - start_time
    print(f"✅ 10,000 customer validations: {customer_validation_time:.4f}s ({10000/customer_validation_time:.0f} ops/sec)")
    
    return {
        "order_validation_rate": 10000/validation_time,
        "customer_validation_rate": 10000/customer_validation_time
    }

def test_audit_logging_performance():
    """Test audit logging performance"""
    print("\n=== AUDIT LOGGING PERFORMANCE TEST ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Override audit log path
        import utils.helpers as helpers_module
        original_path = helpers_module.AUDIT_LOG
        helpers_module.AUDIT_LOG = os.path.join(tmpdir, 'test_audit.csv')
        
        try:
            start_time = time.time()
            for i in range(1000):
                helpers_module.log_audit(f"order_{i}", "success", "Test message")
            logging_time = time.time() - start_time
            print(f"✅ 1000 audit logs: {logging_time:.4f}s ({1000/logging_time:.0f} ops/sec)")
            
            # Check file size
            file_size = os.path.getsize(helpers_module.AUDIT_LOG)
            print(f"✅ Audit file size: {file_size} bytes ({file_size/1000:.1f} KB)")
            
        finally:
            helpers_module.AUDIT_LOG = original_path
    
    return {
        "logging_rate": 1000/logging_time,
        "file_size_per_1000_entries": file_size
    }

def test_error_handling():
    """Test error handling and edge cases"""
    print("\n=== ERROR HANDLING TEST ===")
    
    from core.validator import validate_order, validate_customer
    from core.exceptions import SyncError, WooCommerceAPIError, OdooAPIError
    
    test_cases = [
        # Invalid orders
        ({}, "Empty order"),
        ({"customer_id": None}, "Null customer_id"),
        ({"customer_id": 123, "line_items": []}, "Empty line_items"),
        ({"customer_id": 123}, "Missing line_items"),
        
        # Invalid customers
        ({}, "Empty customer"),
        ({"email": ""}, "Empty email"),
        ({"email": "test@example.com"}, "Missing names"),
    ]
    
    errors_caught = 0
    for test_data, description in test_cases:
        try:
            if "customer" in description.lower():
                validate_customer(test_data)
            else:
                validate_order(test_data)
            print(f"❌ {description}: No error raised")
        except (ValueError, KeyError):
            errors_caught += 1
            print(f"✅ {description}: Error properly caught")
        except Exception as e:
            print(f"⚠️ {description}: Unexpected error type: {type(e).__name__}")
    
    print(f"✅ Error handling: {errors_caught}/{len(test_cases)} cases handled correctly")
    return errors_caught / len(test_cases)

def generate_performance_report(db_perf, validation_perf, audit_perf, error_handling_score):
    """Generate comprehensive performance report"""
    print("\n=== PERFORMANCE REPORT ===")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "database": {
            "initialization_time_ms": db_perf["init_time"] * 1000,
            "bulk_insert_rate_ops_per_sec": db_perf["bulk_insert_rate"],
            "lookup_rate_ops_per_sec": db_perf["lookup_rate"]
        },
        "validation": {
            "order_validation_rate_ops_per_sec": validation_perf["order_validation_rate"],
            "customer_validation_rate_ops_per_sec": validation_perf["customer_validation_rate"]
        },
        "audit_logging": {
            "logging_rate_ops_per_sec": audit_perf["logging_rate"],
            "file_size_per_1000_entries_bytes": audit_perf["file_size_per_1000_entries"]
        },
        "error_handling": {
            "score": error_handling_score,
            "percentage": error_handling_score * 100
        }
    }
    
    # Performance grades
    grades = {}
    
    # Database performance grading
    if db_perf["bulk_insert_rate"] > 500:
        grades["database_insert"] = "A"
    elif db_perf["bulk_insert_rate"] > 200:
        grades["database_insert"] = "B"
    else:
        grades["database_insert"] = "C"
    
    if db_perf["lookup_rate"] > 1000:
        grades["database_lookup"] = "A"
    elif db_perf["lookup_rate"] > 500:
        grades["database_lookup"] = "B"
    else:
        grades["database_lookup"] = "C"
    
    # Validation performance grading
    if validation_perf["order_validation_rate"] > 5000:
        grades["validation"] = "A"
    elif validation_perf["order_validation_rate"] > 2000:
        grades["validation"] = "B"
    else:
        grades["validation"] = "C"
    
    # Error handling grading
    if error_handling_score >= 0.9:
        grades["error_handling"] = "A"
    elif error_handling_score >= 0.7:
        grades["error_handling"] = "B"
    else:
        grades["error_handling"] = "C"
    
    report["grades"] = grades
    
    print(f"Database Insert Performance: {grades['database_insert']} ({db_perf['bulk_insert_rate']:.0f} ops/sec)")
    print(f"Database Lookup Performance: {grades['database_lookup']} ({db_perf['lookup_rate']:.0f} ops/sec)")
    print(f"Validation Performance: {grades['validation']} ({validation_perf['order_validation_rate']:.0f} ops/sec)")
    print(f"Error Handling: {grades['error_handling']} ({error_handling_score*100:.0f}%)")
    
    # Overall grade
    grade_values = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
    avg_grade = sum(grade_values[g] for g in grades.values()) / len(grades)
    
    if avg_grade >= 3.5:
        overall = "A"
    elif avg_grade >= 2.5:
        overall = "B"
    elif avg_grade >= 1.5:
        overall = "C"
    else:
        overall = "D"
    
    print(f"\n🎯 OVERALL PERFORMANCE GRADE: {overall}")
    
    return report

def main():
    """Run comprehensive project analysis"""
    print("🔍 COMPREHENSIVE PROJECT ANALYSIS")
    print("=" * 50)
    
    # Structure analysis
    structure_ok = analyze_project_structure()
    
    # Code quality analysis
    code_issues = analyze_code_quality()
    
    if code_issues:
        print(f"\n❌ Code issues found: {code_issues}")
        return
    
    # Performance tests
    try:
        db_perf = test_database_performance()
        validation_perf = test_validation_performance()
        audit_perf = test_audit_logging_performance()
        error_handling_score = test_error_handling()
        
        # Generate report
        report = generate_performance_report(db_perf, validation_perf, audit_perf, error_handling_score)
        
        # Save report
        with open('performance_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Detailed report saved to: performance_report.json")
        
    except Exception as e:
        print(f"\n❌ Error during performance testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()