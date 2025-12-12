"""
Comprehensive test suite for enhanced JSON error context functionality.
Tests complex JSON validation failures and contextual error messaging.
"""
import pytest
import json
import sys
import os

# Import the modules to test
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_server_sqlite.json_error_context import provide_advanced_json_error_context
from mcp_server_sqlite.diagnostics_isolated import isolated_validate_json, _format_enhanced_error_message


class TestAdvancedJSONErrorContext:
    """Test cases for advanced JSON error context analysis"""
    
    def test_security_violation_detection(self):
        """Test detection and handling of security violations in JSON"""
        malicious_inputs = [
            "{'key': 'value'; DROP TABLE users; --'}",
            "SELECT * FROM users UNION SELECT password FROM admin; {'valid': 'json'}",
            "/* malicious comment */ {'data': 'test'}",
            "{'injection': 'OR 1=1'}",
        ]
        
        for malicious_input in malicious_inputs:
            try:
                # This should trigger security detection
                json.loads(malicious_input)
            except json.JSONDecodeError as e:
                context = provide_advanced_json_error_context(
                    error_msg=str(e),
                    original_json=malicious_input,
                    normalized_attempt=None
                )
                
                # Should detect security concern even if error type is structural
                # (structural errors take precedence, but security is still flagged)
                if any(pattern in malicious_input.upper() for pattern in ['DROP', 'SELECT', 'UNION', 'OR 1=1']):
                    assert context['security_concern'] is True
                    assert len(context['suggestions']) > 0
                    # Security concern should be detected regardless of primary error type
                    assert context['error_type'] in ['security_violation', 'structural_syntax']
    
    def test_structural_syntax_errors(self):
        """Test detection and analysis of structural syntax errors"""
        structural_errors = [
            ("{key_without_quotes: 'value'}", "unquoted keys"),
            ("{'key': 'value',}", "trailing comma"),
            ("{'key': 'unclosed_string}", "unclosed string"),
            ("{'unmatched': 'brackets'", "unmatched brackets"),
            ("{nested: {broken: structure}}", "multiple structural issues"),
        ]
        
        for invalid_json, description in structural_errors:
            try:
                json.loads(invalid_json)
            except json.JSONDecodeError as e:
                context = provide_advanced_json_error_context(
                    error_msg=str(e),
                    original_json=invalid_json,
                    normalized_attempt=None
                )
                
                assert context['error_type'] == 'structural_syntax'
                assert len(context['suggestions']) > 0
                assert not context['security_concern']
                
                # Check for specific suggestions based on error type
                suggestions_text = ' '.join(context['suggestions']).lower()
                if 'quotes' in description:
                    assert 'quote' in suggestions_text
                if 'comma' in description:
                    assert ('comma' in suggestions_text or 'trailing' in suggestions_text)
                if 'bracket' in description:
                    assert 'bracket' in suggestions_text


class TestIsolatedValidationWithEnhancedErrors:
    """Test the integrated isolated validation with enhanced error context"""
    
    def test_isolated_validation_with_enhanced_context(self):
        """Test that isolated validation includes enhanced error context"""
        invalid_json = "{'key': 'value'; DROP TABLE users; --'}"
        
        result = isolated_validate_json(invalid_json)
        
        assert result['valid'] is False
        assert 'error_context' in result
        assert 'enhanced_message' in result
        
        # Check enhanced message formatting
        enhanced_msg = result['enhanced_message']
        assert 'JSON validation failed' in enhanced_msg
    
    def test_structural_error_with_suggestions(self):
        """Test structural errors provide actionable suggestions"""
        invalid_json = "{key_without_quotes: 'value', 'trailing_comma': 'here',}"
        
        result = isolated_validate_json(invalid_json)
        
        assert result['valid'] is False
        assert 'error_context' in result
        
        context = result['error_context']
        assert context['error_type'] == 'structural_syntax'
        assert len(context['suggestions']) > 0
        
        # Check that suggestions are actionable
        suggestions_text = ' '.join(context['suggestions']).lower()
        assert 'quote' in suggestions_text


if __name__ == '__main__':
    # Run a simple test
    print("Running basic test...")
    
    # Test basic functionality
    invalid_json = "{key_without_quotes: 'value'}"
    
    try:
        json.loads(invalid_json)
    except json.JSONDecodeError as e:
        context = provide_advanced_json_error_context(
            error_msg=str(e),
            original_json=invalid_json,
            normalized_attempt=None
        )
        
        print(f"Error type: {context['error_type']}")
        print(f"Security concern: {context['security_concern']}")
        print(f"Suggestions: {context['suggestions']}")
        print("Basic test passed!")
    
    # Test isolated validation
    result = isolated_validate_json(invalid_json)
    print(f"Isolated validation result: {result['valid']}")
    if 'enhanced_message' in result:
        print(f"Enhanced message: {result['enhanced_message'][:200]}...")
    
    print("All basic tests completed!")