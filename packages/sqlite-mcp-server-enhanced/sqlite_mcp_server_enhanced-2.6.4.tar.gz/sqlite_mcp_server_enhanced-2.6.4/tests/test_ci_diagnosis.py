#!/usr/bin/env python3
"""
CI Diagnosis Test - Debug why normalization fails in CI but works locally
"""
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_ci_diagnosis():
    """Diagnose CI environment issues"""
    
    print("🔍 CI DIAGNOSIS TEST")
    print("=" * 50)
    
    # Check environment
    print("1. Environment Check:")
    strict_mode_env = os.getenv('SQLITE_JSON_STRICT_MODE', 'not_set')
    print(f"   SQLITE_JSON_STRICT_MODE: {strict_mode_env}")
    print(f"   Python version: {sys.version}")
    print(f"   Platform: {sys.platform}")
    
    # Check module loading
    print("\n2. Module Loading Check:")
    try:
        from mcp_server_sqlite.jsonb_utils import normalize_json, validate_json, SQLITE_JSON_STRICT_MODE
        print(f"   ✅ Modules imported successfully")
        print(f"   SQLITE_JSON_STRICT_MODE value: {SQLITE_JSON_STRICT_MODE}")
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Test basic normalization
    print("\n3. Basic Normalization Test:")
    test_input = "{'name': 'John', 'active': True}"
    try:
        result = normalize_json(test_input)
        print(f"   Input:  {test_input}")
        print(f"   Output: {result}")
        print(f"   Changed: {result != test_input}")
        
        if result != test_input:
            print("   ✅ Normalization working")
        else:
            print("   ❌ Normalization NOT working")
            
    except Exception as e:
        print(f"   ❌ Normalization failed: {e}")
        return False
    
    # Test validate_json
    print("\n4. Validate JSON Test:")
    try:
        is_valid, normalized = validate_json(test_input, auto_normalize=True)
        print(f"   is_valid: {is_valid}")
        print(f"   normalized: {normalized}")
        print(f"   changed: {normalized != test_input}")
        
        if is_valid and normalized != test_input:
            print("   ✅ validate_json working")
        else:
            print("   ❌ validate_json NOT working as expected")
            
    except Exception as e:
        print(f"   ❌ validate_json failed: {e}")
        return False
    
    # Test security
    print("\n5. Security Test:")
    malicious_input = "{'key': 'value'; DROP TABLE users; --'}"
    try:
        result = normalize_json(malicious_input)
        print(f"   ❌ SECURITY FAILURE - Should have been rejected: {result}")
        return False
    except ValueError as e:
        print(f"   ✅ SECURITY PASS - Correctly rejected: {e}")
    except Exception as e:
        print(f"   ❓ UNEXPECTED ERROR: {e}")
        return False
    
    print("\n🎯 DIAGNOSIS COMPLETE")
    return True

if __name__ == "__main__":
    success = test_ci_diagnosis()
    if success:
        print("✅ All diagnosis tests passed")
    else:
        print("❌ Diagnosis found issues")
        sys.exit(1)
