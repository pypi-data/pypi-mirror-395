"""
Comprehensive test suite for JSON auto-normalization functionality.
Tests various malformed JSON inputs and security considerations.
"""
import pytest
import json
import os
import logging
from unittest.mock import patch

# Import the functions to test
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_server_sqlite.jsonb_utils import (
    normalize_json,
    validate_json,
    convert_to_jsonb,
    SQLITE_JSON_STRICT_MODE
)

class TestJSONNormalization:
    """Test cases for JSON auto-normalization"""
    
    def test_single_quotes_to_double_quotes_keys(self):
        """Test conversion of single quotes to double quotes for keys"""
        input_json = "{'name': 'John', 'age': 30}"
        expected = '{"name": "John", "age": 30}'
        result = normalize_json(input_json)
        assert json.loads(result) == json.loads(expected)
    
    def test_single_quotes_to_double_quotes_values(self):
        """Test conversion of single quotes to double quotes for values"""
        input_json = '{"name": \'John\', "city": \'New York\'}'
        expected = '{"name": "John", "city": "New York"}'
        result = normalize_json(input_json)
        assert json.loads(result) == json.loads(expected)
    
    def test_trailing_commas_removal(self):
        """Test removal of trailing commas"""
        test_cases = [
            ('{"key": "value",}', '{"key": "value"}'),
            ('{"items": [1, 2, 3,]}', '{"items": [1, 2, 3]}'),
            ('{"nested": {"a": 1, "b": 2,}, "c": 3,}', '{"nested": {"a": 1, "b": 2}, "c": 3}'),
        ]
        
        for input_json, expected in test_cases:
            result = normalize_json(input_json)
            assert json.loads(result) == json.loads(expected)
    
    def test_python_booleans_to_json(self):
        """Test conversion of Python booleans to JSON booleans"""
        input_json = '{"active": True, "deleted": False}'
        expected = '{"active": true, "deleted": false}'
        result = normalize_json(input_json)
        assert json.loads(result) == json.loads(expected)
    
    def test_python_none_to_json_null(self):
        """Test conversion of Python None to JSON null"""
        input_json = '{"data": None, "count": 5}'
        expected = '{"data": null, "count": 5}'
        result = normalize_json(input_json)
        assert json.loads(result) == json.loads(expected)
    
    def test_complex_normalization(self):
        """Test complex JSON with multiple normalization needs"""
        input_json = "{'name': 'John', 'active': True, 'data': None, 'items': [1, 2, 3,],}"
        expected = '{"name": "John", "active": true, "data": null, "items": [1, 2, 3]}'
        result = normalize_json(input_json)
        assert json.loads(result) == json.loads(expected)
    
    def test_already_valid_json_unchanged(self):
        """Test that already valid JSON remains unchanged"""
        valid_json = '{"name": "John", "age": 30, "active": true, "data": null}'
        result = normalize_json(valid_json)
        assert result == valid_json
    
    def test_strict_mode_no_normalization(self):
        """Test that strict mode prevents normalization"""
        input_json = "{'key': 'value'}"
        result = normalize_json(input_json, strict_mode=True)
        assert result == input_json  # Should be unchanged
    
    def test_non_string_input_unchanged(self):
        """Test that non-string input is returned unchanged"""
        inputs = [123, None, [], {}]
        for input_val in inputs:
            result = normalize_json(input_val)
            assert result == input_val

class TestSecuritySafeguards:
    """Test security safeguards against SQL injection"""
    
    def test_sql_injection_detection_drop(self):
        """Test detection of DROP statements"""
        malicious_input = "{'key': 'value'; DROP TABLE users; --'}"
        with pytest.raises(ValueError, match="Suspicious input detected"):
            normalize_json(malicious_input)
    
    def test_sql_injection_detection_union(self):
        """Test detection of UNION SELECT statements"""
        malicious_input = "{'key': 'value'} UNION SELECT password FROM users"
        with pytest.raises(ValueError, match="Suspicious input detected"):
            normalize_json(malicious_input)
    
    def test_sql_injection_detection_comments(self):
        """Test detection of SQL comments"""
        malicious_input = "{'key': 'value'} --"
        with pytest.raises(ValueError, match="Suspicious input detected"):
            normalize_json(malicious_input)
    
    def test_sql_injection_detection_or_condition(self):
        """Test detection of OR 1=1 conditions"""
        malicious_input = "{'key': 'value'} OR 1=1"
        with pytest.raises(ValueError, match="Suspicious input detected"):
            normalize_json(malicious_input)
    
    def test_legitimate_json_with_sql_keywords(self):
        """Test that legitimate JSON containing SQL keywords passes"""
        legitimate_json = '{"query": "SELECT name FROM users", "action": "INSERT new record"}'
        result = normalize_json(legitimate_json)
        assert json.loads(result) == json.loads(legitimate_json)

class TestValidateJSON:
    """Test the enhanced validate_json function"""
    
    def test_validate_valid_json(self):
        """Test validation of already valid JSON"""
        valid_json = '{"name": "John", "age": 30}'
        is_valid, normalized = validate_json(valid_json)
        assert is_valid is True
        assert normalized == valid_json
    
    def test_validate_and_normalize_invalid_json(self):
        """Test validation with auto-normalization of invalid JSON"""
        invalid_json = "{'name': 'John', 'active': True,}"
        is_valid, normalized = validate_json(invalid_json)
        assert is_valid is True
        expected = {"name": "John", "active": True}
        assert json.loads(normalized) == expected
    
    def test_validate_without_normalization(self):
        """Test validation without auto-normalization"""
        invalid_json = "{'name': 'John'}"
        is_valid, normalized = validate_json(invalid_json, auto_normalize=False)
        assert is_valid is False
        assert normalized == invalid_json
    
    def test_validate_strict_mode(self):
        """Test validation in strict mode"""
        invalid_json = "{'name': 'John'}"
        is_valid, normalized = validate_json(invalid_json, strict_mode=True)
        assert is_valid is False
        assert normalized == invalid_json
    
    def test_validate_malicious_input(self):
        """Test validation rejects malicious input"""
        malicious_json = "{'key': 'value'; DROP TABLE users; --'}"
        is_valid, normalized = validate_json(malicious_json)
        assert is_valid is False
        assert normalized == malicious_json

class TestEnvironmentConfiguration:
    """Test environment variable configuration"""
    
    def test_strict_mode_environment_variable(self):
        """Test that SQLITE_JSON_STRICT_MODE environment variable works"""
        with patch.dict(os.environ, {'SQLITE_JSON_STRICT_MODE': 'true'}):
            # Reload the module to pick up the environment variable
            import importlib
            import mcp_server_sqlite.jsonb_utils
            importlib.reload(mcp_server_sqlite.jsonb_utils)
            
            from mcp_server_sqlite.jsonb_utils import normalize_json
            
            input_json = "{'key': 'value'}"
            result = normalize_json(input_json)
            assert result == input_json  # Should be unchanged in strict mode

class TestPerformance:
    """Test performance characteristics"""
    
    def test_normalization_performance(self):
        """Test that normalization doesn't add significant overhead"""
        import time
        
        large_json = "{'items': [" + ", ".join([f"{{'id': {i}, 'name': 'item_{i}', 'active': True}}" for i in range(100)]) + "]}"
        
        start_time = time.time()
        # Force strict_mode=False to override any CI environment variables
        result = normalize_json(large_json, strict_mode=False)
        end_time = time.time()
        
        # Should complete in less than 50ms even for large JSON
        assert (end_time - start_time) < 0.05
        
        # Should produce valid JSON
        assert json.loads(result) is not None

class TestEdgeCases:
    """Test edge cases and unusual inputs"""
    
    def test_empty_string(self):
        """Test handling of empty string"""
        result = normalize_json("")
        assert result == ""
    
    def test_nested_quotes(self):
        """Test handling of nested quotes"""
        input_json = '{"message": "He said \'hello\' to me"}'
        result = normalize_json(input_json)
        assert json.loads(result) == json.loads(input_json)
    
    def test_escaped_quotes(self):
        """Test handling of escaped quotes"""
        input_json = '{"path": "C:\\\\Users\\\\name"}'
        result = normalize_json(input_json)
        assert json.loads(result) == json.loads(input_json)
    
    def test_unicode_content(self):
        """Test handling of Unicode content"""
        input_json = "{'name': 'José', 'city': '北京'}"
        # Force strict_mode=False to override any CI environment variables
        result = normalize_json(input_json, strict_mode=False)
        expected = {"name": "José", "city": "北京"}
        assert json.loads(result) == expected
    
    def test_deeply_nested_structure(self):
        """Test handling of deeply nested JSON structures"""
        input_json = "{'level1': {'level2': {'level3': {'value': True, 'data': None,}}}}"
        # Force strict_mode=False to override any CI environment variables
        result = normalize_json(input_json, strict_mode=False)
        expected = {"level1": {"level2": {"level3": {"value": True, "data": None}}}}
        assert json.loads(result) == expected

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])