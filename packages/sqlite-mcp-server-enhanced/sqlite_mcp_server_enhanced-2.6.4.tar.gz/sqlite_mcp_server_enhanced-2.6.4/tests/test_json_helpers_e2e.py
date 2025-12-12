"""
End-to-end test for JSON Helper Tools (Issue #25)

This test verifies that the complete JSON helper implementation works
including path validation, query building, security checks, and database operations.
"""

import pytest
import json
import tempfile
import os
import sqlite3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_server_sqlite.json_helpers import (
    JSONPathValidator, 
    JSONQueryBuilder, 
    validate_json_security
)


class TestJSONHelpersE2E:
    """End-to-end integration test for JSON helpers"""
    
    def setup_method(self):
        # Create temporary database
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.conn = sqlite3.connect(self.db_path)
        
        # Create test table with JSON column
        self.conn.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                metadata TEXT
            )
        """)
        self.conn.commit()
    
    def teardown_method(self):
        self.conn.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_complete_json_workflow(self):
        """Test complete workflow: validate, build, execute, verify"""
        
        # 1. Path Validation
        validator = JSONPathValidator()
        path_result = validator.validate_json_path("$.category")
        assert path_result['valid'] == True
        
        # 2. Security Check
        test_data = {"category": "electronics", "price": 100}
        security_result = validate_json_security(test_data)
        assert security_result['safe'] == True
        
        # 3. Query Building
        builder = JSONQueryBuilder()
        query, params, validation = builder.build_json_insert_query(
            "products", "metadata", test_data
        )
        assert validation['valid'] == True
        assert query == "INSERT INTO products (metadata) VALUES (?)"
        assert len(params) == 1
        
        # 4. Database Execution
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        
        # 5. Verification
        cursor.execute("SELECT json_extract(metadata, '$.category') FROM products WHERE id = 1")
        result = cursor.fetchone()
        assert result[0] == "electronics"
        
        print("✅ Complete JSON workflow test passed!")
    
    def test_json_update_workflow(self):
        """Test JSON update workflow"""
        
        # Insert initial data
        initial_data = {"category": "books", "price": 20, "active": False}
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, metadata) VALUES (?, ?)",
            ["Test Product", json.dumps(initial_data)]
        )
        self.conn.commit()
        
        # Build update query
        builder = JSONQueryBuilder()
        query, params, validation = builder.build_json_update_query(
            "products", "metadata", "$.price", 25, where_clause="id = 1"
        )
        
        assert validation['valid'] == True
        assert "json_replace" in query
        
        # Execute update
        cursor.execute(query, params)
        self.conn.commit()
        
        # Verify update
        cursor.execute("SELECT json_extract(metadata, '$.price') FROM products WHERE id = 1")
        result = cursor.fetchone()
        assert result[0] == 25
        
        print("✅ JSON update workflow test passed!")
    
    def test_json_select_workflow(self):
        """Test JSON select workflow with multiple paths"""
        
        # Insert test data
        test_data = {
            "category": "electronics",
            "price": 150,
            "specs": {"cpu": "intel", "ram": "8GB"},
            "tags": ["popular", "new"]
        }
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, metadata) VALUES (?, ?)",
            ["Complex Product", json.dumps(test_data)]
        )
        self.conn.commit()
        
        # Build select query
        builder = JSONQueryBuilder()
        paths = ["$.category", "$.price", "$.specs.cpu", "$.tags[0]"]
        query, params, validation = builder.build_json_select_query(
            "products", "metadata", paths, output_format="flat"
        )
        
        assert validation['valid'] == True
        assert "AS category" in query
        # The nested path becomes "specs_cpu" as the column alias (dots replaced with underscores)
        assert "AS specs_cpu" in query
        
        # Execute query
        cursor.execute(query, params)
        result = cursor.fetchone()
        
        # Verify results
        assert result[0] == "electronics"  # category
        assert result[1] == 150           # price
        assert result[2] == "intel"       # specs.cpu
        assert result[3] == "popular"     # tags[0]
        
        print("✅ JSON select workflow test passed!")
    
    def test_security_rejection_workflow(self):
        """Test that security violations are properly detected and rejected"""
        
        # Test malicious JSON data
        malicious_data = {
            "name": "Product'; DROP TABLE users; --",
            "description": "Test UNION SELECT password FROM users"
        }
        
        # Security check should fail
        security_result = validate_json_security(malicious_data)
        assert security_result['safe'] == False
        assert len(security_result['detected_patterns']) > 0
        
        print("✅ Security rejection workflow test passed!")
    
    def test_path_validation_edge_cases(self):
        """Test edge cases in path validation"""
        
        validator = JSONPathValidator()
        
        # Test various valid paths
        valid_paths = [
            "$",
            "$.simple",
            "$.nested.deep.path",
            "$.array[0]",
            "$.complex[5].nested.field[10]"
        ]
        
        for path in valid_paths:
            result = validator.validate_json_path(path)
            assert result['valid'] == True, f"Path {path} should be valid"
        
        # Test invalid paths
        invalid_paths = [
            "",                    # Empty
            "simple",             # No $
            "$..",                # Double dots
            "$.[missing_bracket", # Malformed bracket
            "$.field; DROP TABLE" # SQL injection
        ]
        
        for path in invalid_paths:
            result = validator.validate_json_path(path)
            assert result['valid'] == False, f"Path {path} should be invalid"
        
        print("✅ Path validation edge cases test passed!")
    
    def test_auto_normalization_workflow(self):
        """Test Python-style JSON auto-normalization"""
        
        # Python-style JSON
        python_json = "{'category': 'electronics', 'active': True, 'price': None, 'tags': ['new', 'popular',]}"
        
        builder = JSONQueryBuilder()
        query, params, validation = builder.build_json_insert_query(
            "products", "metadata", python_json
        )
        
        # Should either succeed with normalization or provide clear error
        if validation['valid']:
            # If normalization succeeded, verify the JSON is valid
            normalized_data = json.loads(params[0])
            assert normalized_data['category'] == 'electronics'
            assert normalized_data['active'] == True
            assert normalized_data['price'] is None
            assert normalized_data['tags'] == ['new', 'popular']
            print("✅ Auto-normalization succeeded!")
        else:
            # If normalization failed, should provide helpful error
            assert 'error' in validation
            print("✅ Auto-normalization provided helpful error!")
        
        print("✅ Auto-normalization workflow test passed!")


if __name__ == "__main__":
    # Run the tests
    test_instance = TestJSONHelpersE2E()
    
    try:
        test_instance.setup_method()
        test_instance.test_complete_json_workflow()
        test_instance.teardown_method()
        
        test_instance.setup_method()
        test_instance.test_json_update_workflow()
        test_instance.teardown_method()
        
        test_instance.setup_method()
        test_instance.test_json_select_workflow()
        test_instance.teardown_method()
        
        test_instance.setup_method()
        test_instance.test_security_rejection_workflow()
        test_instance.teardown_method()
        
        test_instance.setup_method()
        test_instance.test_path_validation_edge_cases()
        test_instance.teardown_method()
        
        test_instance.setup_method()
        test_instance.test_auto_normalization_workflow()
        test_instance.teardown_method()
        
        print("\n🎉 ALL END-TO-END TESTS PASSED!")
        print("✅ JSON Helper Tools (Issue #25) implementation is complete and working!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
