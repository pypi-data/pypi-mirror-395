#!/usr/bin/env python3
"""
Comprehensive Automatic Parameter Serialization Test for SQLite MCP Server

This test verifies the new automatic parameter serialization feature:
1. Dict and list parameters are automatically serialized to JSON strings
2. Existing string/numeric parameters work unchanged (backward compatibility)
3. Comprehensive edge cases are handled properly
4. No breaking changes to existing API

Created for: https://github.com/neverinfamous/sqlite-mcp-server/issues/22
"""

import sqlite3
import os
import sys
import tempfile
import json
from typing import Any, List, Dict

# Add the src directory to the path so we can import the server
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_server_sqlite.server import EnhancedSqliteDatabase

class AutoParameterSerializationTester:
    def __init__(self):
        self.db_path = "./test-auto-param-serialization.db"
        self.db: EnhancedSqliteDatabase | None = None
        self.test_results = []
        
    def _ensure_db(self) -> EnhancedSqliteDatabase:
        """Ensure database is initialized"""
        if self.db is None:
            raise RuntimeError("Database not initialized. Call setup_database() first.")
        return self.db
        
    def setup_database(self):
        """Initialize test database with sample data"""
        print("📁 Creating test database:", self.db_path)
        
        # Remove existing test database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            
        # Initialize database
        self.db = EnhancedSqliteDatabase(self.db_path)
        
        # Create test table with JSON column
        self._ensure_db()._execute_query("""
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                json_data TEXT,
                metadata TEXT,
                created_at TEXT
            )
        """)
        
        print("✅ Database initialized with test table")
        
    def test_dict_parameter_serialization(self):
        """Test that dict parameters are automatically serialized to JSON"""
        print("\n📦 Test 1: Dict Parameter Auto-Serialization")
        
        test_dict = {"key": "value", "number": 42, "nested": {"inner": "data"}}
        
        try:
            # Insert with dict parameter (should be auto-serialized)
            result = self._ensure_db()._execute_query(
                "INSERT INTO test_table (name, json_data) VALUES (?, ?)",
                ["test_dict", test_dict]
            )
            
            # Verify insertion worked
            query_result = self._ensure_db()._execute_query(
                "SELECT json_data FROM test_table WHERE name = ?",
                ["test_dict"]
            )
            
            if len(query_result) == 1:
                stored_json = query_result[0]['json_data']
                parsed_dict = json.loads(stored_json)
                
                if parsed_dict == test_dict:
                    print("   ✅ PASS: Dict parameter auto-serialized correctly")
                    self.test_results.append(("Dict Auto-Serialization", "PASS"))
                else:
                    print(f"   ❌ FAIL: Dict mismatch - Expected {test_dict}, got {parsed_dict}")
                    self.test_results.append(("Dict Auto-Serialization", "FAIL"))
            else:
                print("   ❌ FAIL: Dict insertion failed")
                self.test_results.append(("Dict Auto-Serialization", "FAIL"))
                
        except Exception as e:
            print(f"   ❌ FAIL: Dict serialization error - {str(e)}")
            self.test_results.append(("Dict Auto-Serialization", "FAIL"))
    
    def test_list_parameter_serialization(self):
        """Test that list parameters are automatically serialized to JSON"""
        print("\n📋 Test 2: List Parameter Auto-Serialization")
        
        test_list = ["item1", "item2", 42, {"nested": "object"}, [1, 2, 3]]
        
        try:
            # Insert with list parameter (should be auto-serialized)
            result = self._ensure_db()._execute_query(
                "INSERT INTO test_table (name, json_data) VALUES (?, ?)",
                ["test_list", test_list]
            )
            
            # Verify insertion worked
            query_result = self._ensure_db()._execute_query(
                "SELECT json_data FROM test_table WHERE name = ?",
                ["test_list"]
            )
            
            if len(query_result) == 1:
                stored_json = query_result[0]['json_data']
                parsed_list = json.loads(stored_json)
                
                if parsed_list == test_list:
                    print("   ✅ PASS: List parameter auto-serialized correctly")
                    self.test_results.append(("List Auto-Serialization", "PASS"))
                else:
                    print(f"   ❌ FAIL: List mismatch - Expected {test_list}, got {parsed_list}")
                    self.test_results.append(("List Auto-Serialization", "FAIL"))
            else:
                print("   ❌ FAIL: List insertion failed")
                self.test_results.append(("List Auto-Serialization", "FAIL"))
                
        except Exception as e:
            print(f"   ❌ FAIL: List serialization error - {str(e)}")
            self.test_results.append(("List Auto-Serialization", "FAIL"))
    
    def test_backward_compatibility(self):
        """Test that existing string/numeric parameters still work unchanged"""
        print("\n🔄 Test 3: Backward Compatibility")
        
        test_cases = [
            ("String parameter", "test_string", "This is a regular string"),
            ("Integer parameter", "test_int", 12345),
            ("Float parameter", "test_float", 123.45),
            ("Boolean parameter", "test_bool", True),
            ("None parameter", "test_none", None),
            ("JSON string parameter", "test_json_string", '{"already": "serialized"}'),
        ]
        
        for description, name, value in test_cases:
            try:
                # Insert with regular parameter
                self._ensure_db()._execute_query(
                    "INSERT INTO test_table (name, json_data) VALUES (?, ?)",
                    [name, value]
                )
                
                # Verify insertion worked
                query_result = self._ensure_db()._execute_query(
                    "SELECT json_data FROM test_table WHERE name = ?",
                    [name]
                )
                
                if len(query_result) == 1:
                    stored_value = query_result[0]['json_data']
                    
                    # For backward compatibility, non-dict/list values should be stored as-is
                    if stored_value == value or (value is None and stored_value is None):
                        print(f"   ✅ PASS: {description}")
                        self.test_results.append((f"Backward Compatibility - {description}", "PASS"))
                    else:
                        print(f"   ❌ FAIL: {description} - Expected {value}, got {stored_value}")
                        self.test_results.append((f"Backward Compatibility - {description}", "FAIL"))
                else:
                    print(f"   ❌ FAIL: {description} - Insertion failed")
                    self.test_results.append((f"Backward Compatibility - {description}", "FAIL"))
                    
            except Exception as e:
                print(f"   ❌ FAIL: {description} - {str(e)}")
                self.test_results.append((f"Backward Compatibility - {description}", "FAIL"))
    
    def test_mixed_parameters(self):
        """Test queries with mixed parameter types (dict, list, string, int)"""
        print("\n🔀 Test 4: Mixed Parameter Types")
        
        try:
            mixed_dict = {"type": "mixed", "count": 5}
            mixed_list = ["tag1", "tag2", "tag3"]
            regular_string = "mixed_test"
            regular_int = 999
            
            # Insert with mixed parameter types
            self._ensure_db()._execute_query(
                "INSERT INTO test_table (id, name, json_data, metadata) VALUES (?, ?, ?, ?)",
                [regular_int, regular_string, mixed_dict, mixed_list]
            )
            
            # Verify insertion worked
            query_result = self._ensure_db()._execute_query(
                "SELECT * FROM test_table WHERE id = ?",
                [regular_int]
            )
            
            if len(query_result) == 1:
                row = query_result[0]
                
                # Check that dict was serialized
                stored_dict = json.loads(row['json_data'])
                # Check that list was serialized
                stored_list = json.loads(row['metadata'])
                
                if (stored_dict == mixed_dict and 
                    stored_list == mixed_list and 
                    row['name'] == regular_string and 
                    row['id'] == regular_int):
                    print("   ✅ PASS: Mixed parameter types handled correctly")
                    self.test_results.append(("Mixed Parameter Types", "PASS"))
                else:
                    print("   ❌ FAIL: Mixed parameter types not handled correctly")
                    self.test_results.append(("Mixed Parameter Types", "FAIL"))
            else:
                print("   ❌ FAIL: Mixed parameters insertion failed")
                self.test_results.append(("Mixed Parameter Types", "FAIL"))
                
        except Exception as e:
            print(f"   ❌ FAIL: Mixed parameters error - {str(e)}")
            self.test_results.append(("Mixed Parameter Types", "FAIL"))
    
    def test_complex_nested_structures(self):
        """Test complex nested dict/list structures"""
        print("\n🏗️ Test 5: Complex Nested Structures")
        
        complex_data = {
            "users": [
                {"id": 1, "name": "Alice", "roles": ["admin", "user"]},
                {"id": 2, "name": "Bob", "roles": ["user"], "metadata": {"active": True}}
            ],
            "settings": {
                "theme": "dark",
                "notifications": {
                    "email": True,
                    "push": False,
                    "categories": ["alerts", "updates"]
                }
            },
            "tags": ["important", "nested", "test"],
            "version": 1.0
        }
        
        try:
            # Insert complex nested structure
            self._ensure_db()._execute_query(
                "INSERT INTO test_table (name, json_data) VALUES (?, ?)",
                ["complex_nested", complex_data]
            )
            
            # Verify insertion and retrieval
            query_result = self._ensure_db()._execute_query(
                "SELECT json_data FROM test_table WHERE name = ?",
                ["complex_nested"]
            )
            
            if len(query_result) == 1:
                stored_json = query_result[0]['json_data']
                parsed_data = json.loads(stored_json)
                
                if parsed_data == complex_data:
                    print("   ✅ PASS: Complex nested structures serialized correctly")
                    self.test_results.append(("Complex Nested Structures", "PASS"))
                else:
                    print("   ❌ FAIL: Complex nested structures mismatch")
                    self.test_results.append(("Complex Nested Structures", "FAIL"))
            else:
                print("   ❌ FAIL: Complex nested structures insertion failed")
                self.test_results.append(("Complex Nested Structures", "FAIL"))
                
        except Exception as e:
            print(f"   ❌ FAIL: Complex nested structures error - {str(e)}")
            self.test_results.append(("Complex Nested Structures", "FAIL"))
    
    def test_edge_cases(self):
        """Test edge cases and error conditions"""
        print("\n🔍 Test 6: Edge Cases")
        
        edge_cases = [
            ("Empty dict", {}),
            ("Empty list", []),
            ("Dict with None values", {"key": None, "empty": ""}),
            ("List with mixed types", [None, "", 0, False, {}]),
            ("Unicode in dict", {"unicode": "测试", "emoji": "🚀"}),
            ("Large nested structure", {"data": [{"item": i} for i in range(100)]}),
        ]
        
        for description, test_data in edge_cases:
            try:
                # Insert edge case data
                self._ensure_db()._execute_query(
                    "INSERT INTO test_table (name, json_data) VALUES (?, ?)",
                    [f"edge_case_{description.replace(' ', '_')}", test_data]
                )
                
                # Verify retrieval
                query_result = self._ensure_db()._execute_query(
                    "SELECT json_data FROM test_table WHERE name = ?",
                    [f"edge_case_{description.replace(' ', '_')}"]
                )
                
                if len(query_result) == 1:
                    stored_json = query_result[0]['json_data']
                    parsed_data = json.loads(stored_json)
                    
                    if parsed_data == test_data:
                        print(f"   ✅ PASS: {description}")
                        self.test_results.append((f"Edge Case - {description}", "PASS"))
                    else:
                        print(f"   ❌ FAIL: {description} - Data mismatch")
                        self.test_results.append((f"Edge Case - {description}", "FAIL"))
                else:
                    print(f"   ❌ FAIL: {description} - Insertion failed")
                    self.test_results.append((f"Edge Case - {description}", "FAIL"))
                    
            except Exception as e:
                print(f"   ❌ FAIL: {description} - {str(e)}")
                self.test_results.append((f"Edge Case - {description}", "FAIL"))
    
    def test_api_improvement_examples(self):
        """Test the API improvement examples from the issue"""
        print("\n🚀 Test 7: API Improvement Examples")
        
        try:
            # Example 1: Simple object insertion (the main use case from issue #22)
            simple_object = {"key": "value"}
            
            # Old verbose way (should still work)
            self._ensure_db()._execute_query(
                "INSERT INTO test_table (name, json_data) VALUES (?, ?)",
                ["old_way", json.dumps(simple_object)]
            )
            
            # New simplified way (automatic serialization)
            self._ensure_db()._execute_query(
                "INSERT INTO test_table (name, json_data) VALUES (?, ?)",
                ["new_way", simple_object]
            )
            
            # Verify both approaches produce the same result
            old_result = self._ensure_db()._execute_query(
                "SELECT json_data FROM test_table WHERE name = ?",
                ["old_way"]
            )
            new_result = self._ensure_db()._execute_query(
                "SELECT json_data FROM test_table WHERE name = ?",
                ["new_way"]
            )
            
            if (len(old_result) == 1 and len(new_result) == 1 and 
                old_result[0]['json_data'] == new_result[0]['json_data']):
                print("   ✅ PASS: API improvement - both old and new ways work identically")
                self.test_results.append(("API Improvement - Compatibility", "PASS"))
            else:
                print("   ❌ FAIL: API improvement - old and new ways produce different results")
                self.test_results.append(("API Improvement - Compatibility", "FAIL"))
            
            # Example 2: Complex object without manual JSON.stringify()
            complex_object = {
                "user": {"id": 123, "name": "Test User"},
                "preferences": ["dark_mode", "notifications"],
                "metadata": {"created": "2024-01-01", "version": 2}
            }
            
            self._ensure_db()._execute_query(
                "INSERT INTO test_table (name, json_data) VALUES (?, ?)",
                ["api_improvement", complex_object]
            )
            
            # Verify complex object was stored correctly
            result = self._ensure_db()._execute_query(
                "SELECT json_data FROM test_table WHERE name = ?",
                ["api_improvement"]
            )
            
            if len(result) == 1:
                stored_data = json.loads(result[0]['json_data'])
                if stored_data == complex_object:
                    print("   ✅ PASS: API improvement - complex object without manual serialization")
                    self.test_results.append(("API Improvement - Complex Object", "PASS"))
                else:
                    print("   ❌ FAIL: API improvement - complex object data mismatch")
                    self.test_results.append(("API Improvement - Complex Object", "FAIL"))
            else:
                print("   ❌ FAIL: API improvement - complex object insertion failed")
                self.test_results.append(("API Improvement - Complex Object", "FAIL"))
                
        except Exception as e:
            print(f"   ❌ FAIL: API improvement examples error - {str(e)}")
            self.test_results.append(("API Improvement Examples", "FAIL"))
    
    def test_performance_impact(self):
        """Test performance impact of automatic serialization"""
        print("\n⚡ Test 8: Performance Impact")
        
        import time
        
        try:
            test_dict = {"performance": "test", "data": [1, 2, 3, 4, 5]}
            
            # Measure auto-serialization performance
            start_time = time.time()
            for i in range(100):
                self._ensure_db()._execute_query(
                    "INSERT INTO test_table (name, json_data) VALUES (?, ?)",
                    [f"perf_auto_{i}", test_dict]
                )
            auto_time = time.time() - start_time
            
            # Measure manual serialization performance
            start_time = time.time()
            for i in range(100):
                self._ensure_db()._execute_query(
                    "INSERT INTO test_table (name, json_data) VALUES (?, ?)",
                    [f"perf_manual_{i}", json.dumps(test_dict)]
                )
            manual_time = time.time() - start_time
            
            overhead = ((auto_time - manual_time) / manual_time) * 100 if manual_time > 0 else 0
            
            print(f"   📊 Auto-serialization: {auto_time:.4f}s")
            print(f"   📊 Manual serialization: {manual_time:.4f}s")
            print(f"   📊 Overhead: {overhead:.1f}%")
            
            if overhead < 25:  # Less than 25% overhead is acceptable
                print("   ✅ PASS: Performance overhead acceptable")
                self.test_results.append(("Performance Impact", "PASS"))
            else:
                print("   ⚠️ WARNING: Higher performance overhead")
                self.test_results.append(("Performance Impact", "WARNING"))
                
        except Exception as e:
            print(f"   ❌ FAIL: Performance test error - {str(e)}")
            self.test_results.append(("Performance Impact", "FAIL"))
    
    def cleanup(self):
        """Clean up test database"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"🧹 Cleaned up test database: {self.db_path}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("🎉 AUTOMATIC PARAMETER SERIALIZATION TESTS COMPLETED!")
        print("="*70)
        
        passed = sum(1 for _, result in self.test_results if result == "PASS")
        failed = sum(1 for _, result in self.test_results if result == "FAIL")
        warnings = sum(1 for _, result in self.test_results if result == "WARNING")
        errors = sum(1 for _, result in self.test_results if result == "ERROR")
        total = len(self.test_results)
        
        print(f"\n📊 TEST RESULTS:")
        print(f"   ✅ Passed: {passed}/{total}")
        print(f"   ❌ Failed: {failed}/{total}")
        print(f"   ⚠️ Warnings: {warnings}/{total}")
        print(f"   🚨 Errors: {errors}/{total}")
        
        if failed == 0 and errors == 0:
            print(f"\n🚀 FEATURE STATUS: ✅ EXCELLENT")
            print("🔧 Automatic parameter serialization working perfectly")
            print("🔄 Backward compatibility maintained")
            print("📦 Dict and list parameters auto-serialized to JSON")
            print("🎯 Ready for production use!")
        else:
            print(f"\n⚠️ FEATURE STATUS: ❌ ISSUES DETECTED")
            print("🔧 Please review failed tests before deployment")
        
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results:
            status_icon = {"PASS": "✅", "FAIL": "❌", "WARNING": "⚠️", "ERROR": "🚨"}[result]
            print(f"   {status_icon} {test_name}: {result}")

def main():
    """Run all automatic parameter serialization tests"""
    print("🚀 Testing SQLite MCP Server Automatic Parameter Serialization")
    print("="*70)
    print("🎯 Testing GitHub Issue #22: Auto Parameter Serialization")
    print("🔗 https://github.com/neverinfamous/sqlite-mcp-server/issues/22")
    print("="*70)
    
    tester = AutoParameterSerializationTester()
    
    try:
        tester.setup_database()
        tester.test_dict_parameter_serialization()
        tester.test_list_parameter_serialization()
        tester.test_backward_compatibility()
        tester.test_mixed_parameters()
        tester.test_complex_nested_structures()
        tester.test_edge_cases()
        tester.test_api_improvement_examples()
        tester.test_performance_impact()
        
    finally:
        tester.print_summary()
        tester.cleanup()

if __name__ == "__main__":
    main()