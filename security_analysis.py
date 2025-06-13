#!/usr/bin/env python3
"""
Security analysis for the WooCommerce-Odoo sync project
"""

import os
import sys
import re

sys.path.insert(0, os.path.abspath('.'))

def analyze_security():
    """Analyze security aspects of the project"""
    print("=== SECURITY ANALYSIS ===")
    
    security_issues = []
    recommendations = []
    
    # Check environment variable handling
    print("\n🔒 Environment Variable Security:")
    env_example_path = '.env.example'
    if os.path.exists(env_example_path):
        with open(env_example_path, 'r') as f:
            content = f.read()
            if 'admin' in content.lower():
                security_issues.append("Default credentials in .env.example")
                recommendations.append("Remove default credentials from .env.example")
            else:
                print("✅ No hardcoded credentials in .env.example")
    
    # Check for hardcoded secrets in code
    print("\n🔒 Hardcoded Secrets Check:")
    code_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                code_files.append(os.path.join(root, file))
    
    secret_patterns = [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']',
        r'key\s*=\s*["\'][^"\']+["\']',
        r'token\s*=\s*["\'][^"\']+["\']'
    ]
    
    hardcoded_secrets = False
    for file_path in code_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for pattern in secret_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        if 'os.getenv' not in content:  # Exclude environment variable usage
                            security_issues.append(f"Potential hardcoded secret in {file_path}")
                            hardcoded_secrets = True
        except Exception:
            continue
    
    if not hardcoded_secrets:
        print("✅ No hardcoded secrets found")
    
    # Check SQL injection protection
    print("\n🔒 SQL Injection Protection:")
    db_file = 'utils/database.py'
    if os.path.exists(db_file):
        with open(db_file, 'r') as f:
            content = f.read()
            if '?' in content and 'execute(' in content:
                print("✅ Parameterized queries used")
            else:
                security_issues.append("Potential SQL injection vulnerability")
                recommendations.append("Use parameterized queries in database operations")
    
    # Check input validation
    print("\n🔒 Input Validation:")
    validator_file = 'core/validator.py'
    if os.path.exists(validator_file):
        with open(validator_file, 'r') as f:
            content = f.read()
            if 'validate_order' in content and 'validate_customer' in content:
                print("✅ Input validation functions present")
            else:
                security_issues.append("Missing input validation")
                recommendations.append("Implement comprehensive input validation")
    
    # Check error handling
    print("\n🔒 Error Handling:")
    exception_file = 'core/exceptions.py'
    if os.path.exists(exception_file):
        with open(exception_file, 'r') as f:
            content = f.read()
            if 'Exception' in content:
                print("✅ Custom exception handling implemented")
            else:
                security_issues.append("Insufficient error handling")
                recommendations.append("Implement proper exception handling")
    
    # Check logging security
    print("\n🔒 Logging Security:")
    logger_file = 'utils/logger.py'
    if os.path.exists(logger_file):
        print("✅ Centralized logging implemented")
        recommendations.append("Ensure sensitive data is not logged")
    
    # Generate security report
    print(f"\n📋 SECURITY SUMMARY:")
    print(f"Issues found: {len(security_issues)}")
    print(f"Recommendations: {len(recommendations)}")
    
    if security_issues:
        print("\n❌ Security Issues:")
        for issue in security_issues:
            print(f"  - {issue}")
    
    if recommendations:
        print("\n💡 Security Recommendations:")
        for rec in recommendations:
            print(f"  - {rec}")
    
    # Security score
    max_score = 10
    deductions = len(security_issues) * 2
    security_score = max(0, max_score - deductions)
    
    if security_score >= 8:
        grade = "A"
    elif security_score >= 6:
        grade = "B"
    elif security_score >= 4:
        grade = "C"
    else:
        grade = "D"
    
    print(f"\n🛡️ SECURITY GRADE: {grade} ({security_score}/{max_score})")
    
    return {
        "issues": security_issues,
        "recommendations": recommendations,
        "score": security_score,
        "grade": grade
    }

if __name__ == "__main__":
    analyze_security()