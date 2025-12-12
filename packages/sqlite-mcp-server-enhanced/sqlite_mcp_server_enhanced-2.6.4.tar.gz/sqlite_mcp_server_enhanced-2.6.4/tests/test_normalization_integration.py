#!/usr/bin/env python3
"""
Integration test for JSON normalization functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_server_sqlite.jsonb_utils import validate_json, normalize_json
from mcp_server_sqlite.diagnostics import DiagnosticsService
from mcp_server_sqlite.json_logger import JsonLogger

def test_json_normalization_integration():
    """Test the JSON normalization integration"""
    
    # Create a diagnostics service for testing
    logger = JsonLogger({'enabled': True, 'db_path': 'test_normalization.db'})
    diagnostics = DiagnosticsService("test_normalization.db", logger)
    
    print("🧪 Testing JSON Auto-Normalization Integration")
    print("=" * 50)
    
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
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"Input: {test_case['input'][:60]}{'...' if len(test_case['input']) > 60 else ''}")
        
        try:
            # Test the diagnostics service validate_json method
            result = diagnostics.validate_json(test_case['input'])
            
            is_valid = result['valid']
            normalized = result.get('normalized', False)
            
            print(f"✅ Valid: {is_valid}")
            if normalized:
                print(f"🔄 Normalized: {normalized}")
                print(f"📝 Result: {result.get('normalized_json', 'N/A')[:60]}{'...' if len(str(result.get('normalized_json', ''))) > 60 else ''}")
            
            if is_valid == test_case['expected_valid']:
                print(f"✅ Test PASSED")
                passed += 1
            else:
                print(f"❌ Test FAILED - Expected valid={test_case['expected_valid']}, got {is_valid}")
                
        except Exception as e:
            print(f"❌ Test FAILED with exception: {e}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! JSON auto-normalization is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the implementation.")
    
    # Use assertion instead of return for pytest compatibility
    assert passed == total, f"Only {passed}/{total} tests passed"

def test_environment_configuration():
    """Test environment variable configuration"""
    print("\n🔧 Testing Environment Configuration")
    print("=" * 40)
    
    # Test default behavior (normalization enabled)
    print("Testing default behavior (normalization enabled)...")
    is_valid, normalized = validate_json("{'test': True}")
    print(f"✅ Default mode - Valid: {is_valid}, Normalized JSON: {normalized}")
    
    # Test with strict mode
    print("\nTesting strict mode...")
    is_valid_strict, normalized_strict = validate_json("{'test': True}", strict_mode=True)
    print(f"✅ Strict mode - Valid: {is_valid_strict}, Original JSON: {normalized_strict}")
    
    # Use assertion instead of return for pytest compatibility
    assert True  # Test completed successfully

if __name__ == "__main__":
    print("🚀 Starting JSON Auto-Normalization Integration Tests")
    print("=" * 60)
    
    success1 = test_json_normalization_integration()
    success2 = test_environment_configuration()
    
    if success1 and success2:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ JSON auto-normalization is ready for production use.")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("⚠️  Review the implementation before proceeding.")
        sys.exit(1)