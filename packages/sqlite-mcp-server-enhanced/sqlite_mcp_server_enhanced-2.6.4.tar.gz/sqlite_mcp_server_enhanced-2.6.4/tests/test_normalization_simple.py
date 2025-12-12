#!/usr/bin/env python3
"""
Simple integration test for JSON normalization functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_server_sqlite.jsonb_utils import validate_json, normalize_json

def test_json_normalization_simple():
    """Test the JSON normalization functionality"""
    
    print("🧪 Testing JSON Auto-Normalization")
    print("=" * 40)
    
    test_cases = [
        {
            "name": "Single quotes with Python types",
            "input": "{'name': 'John', 'active': True, 'data': None, 'count': 42,}",
            "expected_valid": True
        },
        {
            "name": "Already valid JSON",
            "input": '{"name": "Jane", "active": false, "data": null}',
            "expected_valid": True
        },
        {
            "name": "Malicious input (should be rejected)",
            "input": "{'key': 'value'; DROP TABLE users; --'}",
            "expected_valid": False
        },
        {
            "name": "Complex nested structure",
            "input": "{'user': {'profile': {'name': 'Alice', 'settings': {'theme': 'dark', 'notifications': True,}}}}", 
            "expected_valid": True
        },
        {
            "name": "Unicode content",
            "input": "{'name': 'José', 'city': '北京'}",
            "expected_valid": True
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"Input: {test_case['input'][:50]}{'...' if len(test_case['input']) > 50 else ''}")
        
        try:
            # Test the validate_json function with auto-normalization
            # Force strict_mode=False to override any CI environment variables
            is_valid, normalized_json = validate_json(test_case['input'], auto_normalize=True, strict_mode=False)
            
            print(f"✅ Valid: {is_valid}")
            if normalized_json != test_case['input']:
                print(f"🔄 Normalized: YES")
                print(f"📝 Result: {normalized_json[:50]}{'...' if len(normalized_json) > 50 else ''}")
            else:
                print(f"🔄 Normalized: NO (already valid)")
            
            if is_valid == test_case['expected_valid']:
                print(f"✅ Test PASSED")
                passed += 1
            else:
                print(f"❌ Test FAILED - Expected valid={test_case['expected_valid']}, got {is_valid}")
                
        except Exception as e:
            if test_case['expected_valid']:
                print(f"❌ Test FAILED with exception: {e}")
            else:
                print(f"✅ Test PASSED - Correctly rejected with: {e}")
                passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    # Use assertion instead of return for pytest compatibility
    assert passed == total, f"Only {passed}/{total} normalization tests passed"

def test_security_features():
    """Test security features"""
    print("\n🔒 Testing Security Features")
    print("=" * 30)
    
    malicious_inputs = [
        "{'key': 'value'; DROP TABLE users; --'}",
        "{'key': 'value'} UNION SELECT password FROM users",
        "{'key': 'value'} OR 1=1",
        "{'key': 'value'} /* comment */ DELETE FROM users"
    ]
    
    passed = 0
    total = len(malicious_inputs)
    
    for i, malicious_input in enumerate(malicious_inputs, 1):
        print(f"\n🛡️  Security Test {i}: {malicious_input[:40]}...")
        
        try:
            # Force strict_mode=False to override any CI environment variables
            result = normalize_json(malicious_input, strict_mode=False)
            print(f"❌ SECURITY FAILURE - Should have been rejected: {result}")
        except ValueError as e:
            print(f"✅ SECURITY PASS - Correctly rejected: {str(e)[:60]}...")
            passed += 1
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {e}")
    
    print(f"\n🛡️  Security Results: {passed}/{total} tests passed")
    # Use assertion instead of return for pytest compatibility
    assert passed == total, f"Only {passed}/{total} security tests passed"

if __name__ == "__main__":
    print("🚀 Starting JSON Auto-Normalization Simple Tests")
    print("=" * 50)
    
    success1 = test_json_normalization_simple()
    success2 = test_security_features()
    
    if success1 and success2:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ JSON auto-normalization is working correctly.")
        print("✅ Security safeguards are functioning properly.")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("⚠️  Review the implementation.")
        sys.exit(1)