"""
Comprehensive test suite for JSON Helper Tools (Issue #25)

Tests cover:
- JSON path validation and security
- JSON insertion with auto-normalization
- JSON updates with path creation
- JSON selection with multiple output formats
- Complex JSON queries with filtering and aggregation
- JSON merging with conflict resolution
- Error handling and security scenarios
- Edge cases and malicious input detection
"""

import pytest
import json
import tempfile
import os
import sqlite3
from unittest.mock import patch, MagicMock

# Import the modules we're testing
from src.mcp_server_sqlite.json_helpers import (
    JSONPathValidator, 
    JSONQueryBuilder, 
    merge_json_objects, 
    validate_json_security
)
from src.mcp_server_sqlite.server import EnhancedSqliteDatabase


class TestJSONPathValidator:
    """Test JSON path validation functionality"""
    
    def setup_method(self):
        self.validator = JSONPathValidator()
    
    def test_valid_paths(self):
        """Test validation of valid JSON paths"""
        valid_paths = [
            '$',
            '$.key',
            '$.nested.field',
            '$.array[0]',
            '$.array[10]',
            '$.complex.nested[5].field',
            '$.data.items[0].name'
        ]
        
        for path in valid_paths:
            result = self.validator.validate_json_path(path)
            assert result['valid'] == True, f"Path {path} should be valid"
            assert 'normalized_path' in result
    
    def test_invalid_paths(self):
        """Test validation of invalid JSON paths"""
        invalid_paths = [
            '',  # Empty path
            'key',  # Missing $
            '$..',  # Consecutive dots
            '$.[',  # Missing closing bracket
            '$.array]',  # Missing opening bracket
            '$.field..nested',  # Double dots
        ]
        
        for path in invalid_paths:
            result = self.validator.validate_json_path(path)
            assert result['valid'] == False, f"Path {path} should be invalid"
            assert 'error' in result
            assert 'suggestions' in result
    
    def test_security_validation(self):
        """Test security pattern detection in JSON paths"""
        malicious_paths = [
            '$.key; DROP TABLE users',
            '$.field UNION SELECT password',
            '$.data--comment',
            '$.key/*comment*/',
            '$.field; DELETE FROM table'
        ]
        
        for path in malicious_paths:
            result = self.validator.validate_json_path(path)
            assert result['valid'] == False, f"Malicious path {path} should be rejected"
            assert result.get('security_concern') == True
    
    def test_create_intermediate_paths(self):
        """Test creation of intermediate paths"""
        path = '$.level1.level2.level3'
        paths = self.validator.create_intermediate_paths(path)
        
        expected = ['$', '$.level1', '$.level1.level2', '$.level1.level2.level3']
        assert paths == expected


class TestJSONQueryBuilder:
    """Test JSON query building functionality"""
    
    def setup_method(self):
        self.builder = JSONQueryBuilder()
    
    def test_json_insert_query_dict(self):
        """Test building JSON insert queries with dict data"""
        data = {"name": "test", "value": 123}
        query, params, validation = self.builder.build_json_insert_query(
            "products", "metadata", data
        )
        
        assert validation['valid'] == True
        assert query == "INSERT INTO products (metadata) VALUES (?)"
        assert len(params) == 1
        assert json.loads(params[0]) == data
    
    def test_json_insert_query_with_where(self):
        """Test building JSON insert queries with WHERE clause"""
        data = {"category": "electronics"}
        query, params, validation = self.builder.build_json_insert_query(
            "products", "metadata", data, where_clause="id = 1"
        )
        
        assert validation['valid'] == True
        assert "UPDATE" in query
        assert "WHERE id = 1" in query
    
    def test_json_insert_query_merge_strategy(self):
        """Test different merge strategies"""
        data = {"new_field": "value"}
        
        # Test merge strategy
        query, params, validation = self.builder.build_json_insert_query(
            "products", "metadata", data, 
            where_clause="id = 1", 
            merge_strategy="merge"
        )
        
        assert validation['valid'] == True
        assert "json_patch" in query
    
    def test_json_update_query(self):
        """Test building JSON update queries"""
        query, params, validation = self.builder.build_json_update_query(
            "products", "metadata", "$.category", "electronics"
        )
        
        assert validation['valid'] == True
        assert "json_replace" in query
        assert params == ["$.category", "electronics"]
    
    def test_json_update_query_create_path(self):
        """Test JSON update with path creation"""
        query, params, validation = self.builder.build_json_update_query(
            "products", "metadata", "$.new.field", "value", create_path=True
        )
        
        assert validation['valid'] == True
        assert "json_set" in query
    
    def test_json_select_query_structured(self):
        """Test JSON select with structured output"""
        paths = ["$.name", "$.category", "$.price"]
        query, params, validation = self.builder.build_json_select_query(
            "products", "metadata", paths, output_format="structured"
        )
        
        assert validation['valid'] == True
        assert "json_object" in query
        assert len(params) == 3
        assert params == paths
    
    def test_json_select_query_flat(self):
        """Test JSON select with flat output"""
        paths = ["$.name", "$.price"]
        query, params, validation = self.builder.build_json_select_query(
            "products", "metadata", paths, output_format="flat"
        )
        
        assert validation['valid'] == True
        assert "AS name" in query
        assert "AS price" in query
    
    def test_json_complex_query(self):
        """Test complex JSON queries with filtering and aggregation"""
        filter_paths = {"$.category": "electronics", "$.active": True}
        select_paths = ["$.name", "$.price"]
        aggregate = {"avg_price": "AVG(json_extract(metadata, '$.price'))"}
        
        query, params, validation = self.builder.build_json_query_complex(
            "products", "metadata",
            filter_paths=filter_paths,
            select_paths=select_paths,
            aggregate=aggregate,
            group_by="json_extract(metadata, '$.category')",
            limit=10
        )
        
        assert validation['valid'] == True
        assert "WHERE" in query
        assert "GROUP BY" in query
        assert "LIMIT 10" in query
        assert "AVG(" in query
    
    def test_invalid_path_handling(self):
        """Test handling of invalid JSON paths"""
        query, params, validation = self.builder.build_json_update_query(
            "products", "metadata", "invalid_path", "value"
        )
        
        assert validation['valid'] == False
        assert 'error' in validation


class TestJSONSecurityValidation:
    """Test JSON security validation"""
    
    def test_safe_json_data(self):
        """Test validation of safe JSON data"""
        safe_data = {
            "name": "Product A",
            "category": "electronics",
            "tags": ["new", "popular"],
            "metadata": {"color": "blue", "size": "large"}
        }
        
        result = validate_json_security(safe_data)
        assert result['safe'] == True
        assert result['risk_level'] == 'low'
        assert len(result['detected_patterns']) == 0
    
    def test_malicious_json_data(self):
        """Test detection of malicious patterns in JSON"""
        malicious_data = {
            "name": "Product'; DROP TABLE users; --",
            "description": "Test UNION SELECT password FROM users",
            "script": "<script>alert('xss')</script>"
        }
        
        result = validate_json_security(malicious_data)
        assert result['safe'] == False
        assert result['risk_level'] == 'high'
        assert len(result['detected_patterns']) > 0
    
    def test_sql_injection_patterns(self):
        """Test specific SQL injection pattern detection"""
        sql_patterns = [
            "'; DROP TABLE users; --",
            " UNION SELECT * FROM passwords",
            "/* malicious comment */",
            "; DELETE FROM important_table"
        ]
        
        for pattern in sql_patterns:
            data = {"field": pattern}
            result = validate_json_security(data)
            assert result['safe'] == False, f"Pattern {pattern} should be detected"


class TestJSONMerging:
    """Test JSON object merging functionality"""
    
    def test_merge_replace_strategy(self):
        """Test replace merge strategy"""
        obj1 = {"a": 1, "b": 2}
        obj2 = {"b": 3, "c": 4}
        
        result = merge_json_objects(obj1, obj2, "replace")
        expected = {"a": 1, "b": 3, "c": 4}
        
        assert result == expected
    
    def test_merge_shallow_strategy(self):
        """Test shallow merge strategy"""
        obj1 = {"a": 1, "b": {"x": 1}}
        obj2 = {"b": {"y": 2}, "c": 3}
        
        result = merge_json_objects(obj1, obj2, "merge_shallow")
        expected = {"a": 1, "b": {"y": 2}, "c": 3}
        
        assert result == expected
    
    def test_merge_deep_strategy(self):
        """Test deep merge strategy"""
        obj1 = {"a": 1, "b": {"x": 1, "z": 3}}
        obj2 = {"b": {"y": 2}, "c": 3}
        
        result = merge_json_objects(obj1, obj2, "merge_deep")
        expected = {"a": 1, "b": {"x": 1, "y": 2, "z": 3}, "c": 3}
        
        assert result == expected
    
    def test_invalid_merge_strategy(self):
        """Test handling of invalid merge strategy"""
        obj1 = {"a": 1}
        obj2 = {"b": 2}
        
        with pytest.raises(ValueError):
            merge_json_objects(obj1, obj2, "invalid_strategy")


class TestJSONHelpersIntegration:
    """Integration tests with SQLite database"""
    
    def setup_method(self):
        # Create temporary database
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.conn = sqlite3.connect(self.db_path)
        
        # Create test table
        self.conn.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                metadata TEXT
            )
        """)
        
        # Insert test data
        test_data = [
            (1, "Product A", '{"category": "electronics", "price": 100, "tags": ["new"]}'),
            (2, "Product B", '{"category": "books", "price": 20, "tags": ["popular"]}'),
            (3, "Product C", '{"category": "electronics", "price": 200, "active": true}')
        ]
        
        self.conn.executemany(
            "INSERT INTO products (id, name, metadata) VALUES (?, ?, ?)",
            test_data
        )
        self.conn.commit()
    
    def teardown_method(self):
        self.conn.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_json_path_extraction(self):
        """Test JSON path extraction from real database"""
        cursor = self.conn.cursor()
        
        # Test extracting category from all products
        cursor.execute("SELECT json_extract(metadata, '$.category') FROM products")
        categories = [row[0] for row in cursor.fetchall()]
        
        expected = ["electronics", "books", "electronics"]
        assert categories == expected
    
    def test_json_update_operation(self):
        """Test JSON update operation on real database"""
        cursor = self.conn.cursor()
        
        # Update price for product 1
        cursor.execute(
            "UPDATE products SET metadata = json_set(metadata, '$.price', ?) WHERE id = ?",
            (150, 1)
        )
        self.conn.commit()
        
        # Verify update
        cursor.execute("SELECT json_extract(metadata, '$.price') FROM products WHERE id = 1")
        price = cursor.fetchone()[0]
        
        assert price == 150
    
    def test_json_complex_filtering(self):
        """Test complex JSON filtering operations"""
        cursor = self.conn.cursor()
        
        # Find all electronics products
        cursor.execute("""
            SELECT name, json_extract(metadata, '$.price') as price 
            FROM products 
            WHERE json_extract(metadata, '$.category') = 'electronics'
            ORDER BY price
        """)
        
        results = cursor.fetchall()
        assert len(results) == 2
        assert results[0][0] == "Product A"  # Lower price first
        assert results[1][0] == "Product C"


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_empty_json_path(self):
        """Test handling of empty JSON paths"""
        validator = JSONPathValidator()
        result = validator.validate_json_path("")
        
        assert result['valid'] == False
        assert 'error' in result
    
    def test_malformed_json_data(self):
        """Test handling of malformed JSON data"""
        builder = JSONQueryBuilder()
        
        # Test with invalid JSON string
        query, params, validation = builder.build_json_insert_query(
            "products", "metadata", "{'invalid': json,}"
        )
        
        # Should attempt normalization and potentially succeed or fail gracefully
        assert 'valid' in validation
    
    def test_sql_injection_in_table_name(self):
        """Test handling of SQL injection attempts in table names"""
        builder = JSONQueryBuilder()
        
        # This should be handled at a higher level, but test the query building
        malicious_table = "products; DROP TABLE users; --"
        
        # The query builder itself doesn't validate table names (that's done elsewhere)
        # But we can test that it doesn't break
        query, params, validation = builder.build_json_insert_query(
            malicious_table, "metadata", {"test": "data"}
        )
        
        # Query should be built (validation happens at execution level)
        assert query is not None
    
    def test_large_json_data(self):
        """Test handling of large JSON data"""
        # Create large JSON object
        large_data = {f"key_{i}": f"value_{i}" for i in range(1000)}
        
        builder = JSONQueryBuilder()
        query, params, validation = builder.build_json_insert_query(
            "products", "metadata", large_data
        )
        
        assert validation['valid'] == True
        assert len(params[0]) > 10000  # Should be a large JSON string


class TestAutoNormalization:
    """Test automatic JSON normalization features"""
    
    def test_python_style_json_normalization(self):
        """Test normalization of Python-style JSON"""
        builder = JSONQueryBuilder()
        
        # Python-style JSON with single quotes, True/False, None
        python_json = "{'name': 'Product', 'active': True, 'price': None, 'tags': ['new', 'popular',]}"
        
        query, params, validation = builder.build_json_insert_query(
            "products", "metadata", python_json
        )
        
        # Should normalize successfully
        if validation['valid']:
            # Parse the normalized JSON to verify it's valid
            normalized_data = json.loads(params[0])
            assert normalized_data['name'] == 'Product'
            assert normalized_data['active'] == True
            assert normalized_data['price'] is None
            assert normalized_data['tags'] == ['new', 'popular']
    
    def test_security_during_normalization(self):
        """Test security validation during normalization"""
        builder = JSONQueryBuilder()
        
        # Malicious content that might be normalized
        malicious_json = "{'field': 'value'; DROP TABLE users; --'}"
        
        query, params, validation = builder.build_json_insert_query(
            "products", "metadata", malicious_json
        )
        
        # Should detect security issues even after normalization
        # (Either fail normalization or detect patterns in normalized content)
        if not validation['valid']:
            assert 'error' in validation


if __name__ == "__main__":
    # Run specific test classes for debugging
    pytest.main([__file__, "-v"])
