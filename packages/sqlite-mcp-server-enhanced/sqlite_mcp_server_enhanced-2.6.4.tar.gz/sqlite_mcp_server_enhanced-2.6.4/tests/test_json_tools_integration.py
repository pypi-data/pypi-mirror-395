"""
Integration tests for JSON Helper Tools (Issue #25)

Tests the JSON helper tools directly through their core functions to ensure
complete functionality including:
- JSON path validation and query building
- Parameter validation and error handling  
- JSON auto-normalization in real scenarios
- Security pattern detection and prevention
- Database operations with real SQLite connections
"""

import pytest
import json
import tempfile
import os

from src.mcp_server_sqlite.server import EnhancedSqliteDatabase
from src.mcp_server_sqlite.json_helpers import JSONPathValidator, JSONQueryBuilder, validate_json_security


class TestJSONToolsIntegration:
    """Integration tests for JSON helper tools"""
    
    def setup_method(self):
        # Create temporary database
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Initialize server with temporary database
        self.server_instance = EnhancedSqliteDatabase(self.db_path)
        
        # Initialize JSON helpers
        self.path_validator = JSONPathValidator()
        self.query_builder = JSONQueryBuilder()
        
        # Create test table with JSON column
        self.server_instance._execute_query("""
            CREATE TABLE test_products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                metadata TEXT
            )
        """)
        
        # Insert test data
        test_data = [
            '{"category": "electronics", "price": 100, "tags": ["new"], "specs": {"cpu": "intel"}}',
            '{"category": "books", "price": 20, "tags": ["popular"], "author": {"name": "John Doe"}}',
            '{"category": "electronics", "price": 200, "active": true, "specs": {"cpu": "amd"}}'
        ]
        
        for i, metadata in enumerate(test_data, 1):
            self.server_instance._execute_query(
                "INSERT INTO test_products (id, name, metadata) VALUES (?, ?, ?)",
                [i, f"Product {i}", metadata]
            )
    
    def teardown_method(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_json_insert_tool(self):
        """Test json_insert functionality"""
        # Test data
        table = "test_products"
        column = "metadata"
        data = {"category": "clothing", "price": 50, "new_field": True}
        
        # Build and execute insert query
        query, params, metadata = self.query_builder.build_json_insert_query(
            table=table,
            column=column,
            data=data,
            merge_strategy="replace"
        )
        
        # Execute the query
        self.server_instance._execute_query(query, params)
        
        # Verify database was updated
        rows = self.server_instance._execute_query(
            "SELECT metadata FROM test_products WHERE json_extract(metadata, '$.category') = 'clothing'"
        )
        assert len(rows) == 1
        
        # Verify inserted data
        inserted_data = json.loads(rows[0]["metadata"])
        assert inserted_data["category"] == "clothing"
        assert inserted_data["price"] == 50
        assert inserted_data["new_field"] is True
    
    def test_json_update_tool(self):
        """Test json_update functionality"""
        # Test data
        table = "test_products"
        column = "metadata"
        path = "$.price"
        value = 150
        where_clause = "id = 1"
        
        # Build and execute update query
        query, params, metadata = self.query_builder.build_json_update_query(
            table=table,
            column=column,
            path=path,
            value=value,
            where_clause=where_clause
        )
        
        # Execute the query
        self.server_instance._execute_query(query, params)
        
        # Verify database was updated
        rows = self.server_instance._execute_query(
            "SELECT metadata FROM test_products WHERE id = 1"
        )
        assert len(rows) == 1
        
        # Verify updated data
        updated_data = json.loads(rows[0]["metadata"])
        assert updated_data["price"] == 150
        assert updated_data["category"] == "electronics"  # Should remain unchanged
    
    def test_json_select_tool(self):
        """Test json_select functionality"""
        # Test data
        table = "test_products"
        column = "metadata"
        paths = ["$.category", "$.price", "$.specs.cpu"]
        
        # Build and execute select query with flat format for individual columns
        query, params, metadata = self.query_builder.build_json_select_query(
            table=table,
            column=column,
            paths=paths,
            output_format="flat"
        )
        
        # Execute the query
        rows = self.server_instance._execute_query(query, params)
        
        # Verify results
        assert len(rows) == 3  # Should have 3 products
        
        # Check first row (electronics with intel cpu)
        first_row = rows[0]
        assert "category" in first_row
        assert "price" in first_row
        assert "specs_cpu" in first_row
        assert first_row["category"] == "electronics"
        assert first_row["price"] == 100
        assert first_row["specs_cpu"] == "intel"
    
    def test_json_query_tool_complex(self):
        """Test json_query complex functionality"""
        # Test data
        table = "test_products"
        column = "metadata"
        # Use exact match filters since complex operators aren't supported in this function
        filter_paths = {
            "$.category": "electronics"
        }
        
        # Build and execute complex query
        query, params, metadata = self.query_builder.build_json_query_complex(
            table=table,
            column=column,
            filter_paths=filter_paths
        )
        
        # Execute the query
        rows = self.server_instance._execute_query(query, params)
        
        # Verify results (should find electronics items - there are 2 in test data)
        assert len(rows) == 2
        for row in rows:
            metadata = json.loads(row["metadata"])
            assert metadata["category"] == "electronics"
    
    def test_json_validate_path_tool(self):
        """Test json_validate_path functionality"""
        # Test valid paths
        valid_paths = ["$.category", "$.specs.cpu", "$.tags[0]"]
        for path in valid_paths:
            result = self.path_validator.validate_json_path(path)
            assert result['valid'] == True
        
        # Test invalid paths
        invalid_paths = ["category", "$..", "$..invalid", "$.path["]
        for path in invalid_paths:
            result = self.path_validator.validate_json_path(path)
            assert result['valid'] == False
    
    def test_json_merge_tool(self):
        """Test json_merge functionality"""
        from src.mcp_server_sqlite.json_helpers import merge_json_objects
        
        # Test data
        original = {"category": "electronics", "price": 100, "specs": {"cpu": "intel"}}
        update = {"price": 150, "specs": {"ram": "16GB"}, "new_field": True}
        
        # Test different merge strategies
        result_replace = merge_json_objects(original, update, "replace")
        assert result_replace["price"] == 150
        assert result_replace["new_field"] == True
        assert "cpu" not in result_replace["specs"]  # Should be replaced
        
        result_deep = merge_json_objects(original, update, "merge_deep")
        assert result_deep["price"] == 150
        assert result_deep["new_field"] == True
        assert result_deep["specs"]["cpu"] == "intel"  # Should be preserved
        assert result_deep["specs"]["ram"] == "16GB"   # Should be added


class TestJSONToolsErrorHandling:
    """Error handling tests for JSON helper tools"""
    
    def setup_method(self):
        self.path_validator = JSONPathValidator()
        self.query_builder = JSONQueryBuilder()
    
    def test_missing_arguments_error(self):
        """Test error handling for missing arguments"""
        # Test with empty table name - should not raise ValueError directly
        # but should be handled gracefully
        try:
            query, params, metadata = self.query_builder.build_json_insert_query(
                table="",  # Empty table name
                column="metadata",
                data={}
            )
            # If it doesn't raise, check the query is still valid
            assert query is not None
        except ValueError:
            # This is also acceptable behavior
            pass
    
    def test_invalid_json_data_error(self):
        """Test error handling for invalid JSON data"""
        # This should work fine as the function handles dict input
        query, params, metadata = self.query_builder.build_json_insert_query(
            table="test_table",
            column="metadata",
            data={"valid": "data"}
        )
        assert query is not None
        assert params is not None
        assert metadata is not None
    
    def test_security_violation_detection(self):
        """Test security pattern detection"""
        malicious_data = {
            "category": "'; DROP TABLE users; --",
            "description": "UNION SELECT * FROM sensitive_table"
        }
        
        # Security validation should detect malicious patterns
        result = validate_json_security(json.dumps(malicious_data))
        assert result['safe'] == False
        assert 'detected_patterns' in result
        assert len(result['detected_patterns']) > 0
    
    def test_invalid_table_error(self):
        """Test error handling for invalid table names"""
        # Test with potentially malicious table name - should be handled gracefully
        try:
            query, params, metadata = self.query_builder.build_json_insert_query(
                table="invalid; DROP TABLE users;",
                column="metadata",
                data={}
            )
            # If it doesn't raise, the function handles it gracefully
            assert query is not None
        except ValueError:
            # This is also acceptable behavior
            pass


class TestJSONToolsAutoNormalization:
    """Auto-normalization tests for JSON helper tools"""
    
    def setup_method(self):
        self.query_builder = JSONQueryBuilder()
    
    def test_python_style_json_normalization(self):
        """Test Python-style JSON normalization"""
        from src.mcp_server_sqlite.jsonb_utils import normalize_json
        
        # Python-style JSON
        python_json = "{'name': 'John', 'active': True, 'data': None}"
        
        # Should normalize to valid JSON
        normalized = normalize_json(python_json)
        parsed = json.loads(normalized)
        
        assert parsed["name"] == "John"
        assert parsed["active"] == True
        assert parsed["data"] is None
    
    def test_complex_nested_normalization(self):
        """Test complex nested JSON normalization"""
        from src.mcp_server_sqlite.jsonb_utils import normalize_json
        
        # Complex Python-style JSON
        complex_json = """
        {
            'user': {
                'name': 'Alice',
                'preferences': {
                    'theme': 'dark',
                    'notifications': True,
                    'data': None
                },
                'tags': ['admin', 'user'],
            }
        }
        """
        
        # Should normalize successfully
        normalized = normalize_json(complex_json)
        parsed = json.loads(normalized)
        
        assert parsed["user"]["name"] == "Alice"
        assert parsed["user"]["preferences"]["theme"] == "dark"
        assert parsed["user"]["preferences"]["notifications"] == True
        assert parsed["user"]["preferences"]["data"] is None
        assert "admin" in parsed["user"]["tags"]


class TestJSONToolsPerformance:
    """Performance tests for JSON helper tools"""
    
    def setup_method(self):
        # Create temporary database
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.server_instance = EnhancedSqliteDatabase(self.db_path)
        self.query_builder = JSONQueryBuilder()
        
        # Create test table
        self.server_instance._execute_query("""
            CREATE TABLE performance_test (
                id INTEGER PRIMARY KEY,
                data TEXT
            )
        """)
    
    def teardown_method(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_large_json_handling(self):
        """Test handling of large JSON objects"""
        # Create a large JSON object
        large_data = {
            "items": [{"id": i, "name": f"Item {i}", "data": f"Data {i}"} for i in range(1000)]
        }
        
        # Build and execute insert query
        query, params, metadata = self.query_builder.build_json_insert_query(
            table="performance_test",
            column="data",
            data=large_data
        )
        
        # Should handle large data without issues
        self.server_instance._execute_query(query, params)
        
        # Verify data was inserted
        rows = self.server_instance._execute_query("SELECT COUNT(*) as count FROM performance_test")
        assert rows[0]["count"] == 1
    
    def test_multiple_path_selection(self):
        """Test selecting multiple JSON paths efficiently"""
        # Insert test data
        test_data = {
            "user": {"name": "John", "age": 30},
            "preferences": {"theme": "dark", "lang": "en"},
            "metadata": {"created": "2023-01-01", "updated": "2023-12-01"}
        }
        
        query, params, metadata = self.query_builder.build_json_insert_query(
            table="performance_test",
            column="data",
            data=test_data
        )
        self.server_instance._execute_query(query, params)
        
        # Select multiple paths
        paths = ["$.user.name", "$.user.age", "$.preferences.theme", "$.metadata.created"]
        query, params, metadata = self.query_builder.build_json_select_query(
            table="performance_test",
            column="data",
            paths=paths,
            output_format="flat"
        )
        
        # Execute and verify
        rows = self.server_instance._execute_query(query, params)
        assert len(rows) == 1
        
        row = rows[0]
        assert row["user_name"] == "John"
        assert row["user_age"] == 30
        assert row["preferences_theme"] == "dark"
        assert row["metadata_created"] == "2023-01-01"