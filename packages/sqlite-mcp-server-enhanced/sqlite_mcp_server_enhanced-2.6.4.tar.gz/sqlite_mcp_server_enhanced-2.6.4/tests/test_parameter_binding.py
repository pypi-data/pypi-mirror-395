#!/usr/bin/env python3
"""
Comprehensive Parameter Binding Security Test for SQLite MCP Server

This test verifies that the new parameter binding interface:
1. Provides enhanced SQL injection protection
2. Maintains backward compatibility
3. Works correctly with all supported data types
4. Handles edge cases properly

Created for: https://github.com/neverinfamous/sqlite-mcp-server/issues/28
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

class ParameterBindingTester:
    def __init__(self):
        self.db_path = "./test-parameter-binding.db"
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
        
        # Create test table
        self._ensure_db()._execute_query("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT,
                age INTEGER,
                balance REAL,
                is_active BOOLEAN,
                created_at TEXT
            )
        """)
        
        # Insert test data
        test_users = [
            (1, "admin", "admin@example.com", 30, 1000.50, True, "2024-01-01"),
            (2, "user1", "user1@example.com", 25, 250.75, True, "2024-01-02"),
            (3, "test_user", "test@example.com", 35, 0.0, False, "2024-01-03"),
        ]
        
        for user in test_users:
            self._ensure_db()._execute_query(
                "INSERT INTO users (id, username, email, age, balance, is_active, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                list(user)
            )
        
        print("✅ Database initialized with test data")
        
    def test_backward_compatibility(self):
        """Test that existing queries without params still work"""
        print("\n🔄 Test 1: Backward Compatibility")
        
        try:
            # Test without parameters (old way)
            result = self._ensure_db()._execute_query("SELECT COUNT(*) as count FROM users")
            count = result[0]['count']
            
            if count == 3:
                print("   ✅ PASS: Queries without params work correctly")
                self.test_results.append(("Backward Compatibility", "PASS"))
            else:
                print(f"   ❌ FAIL: Expected 3 users, got {count}")
                self.test_results.append(("Backward Compatibility", "FAIL"))
                
        except Exception as e:
            print(f"   ❌ FAIL: {str(e)}")
            self.test_results.append(("Backward Compatibility", "FAIL"))
    
    def test_parameter_binding_types(self):
        """Test parameter binding with different data types"""
        print("\n🔢 Test 2: Parameter Binding Data Types")
        
        test_cases = [
            # (description, query, params, expected_count)
            ("String parameter", "SELECT * FROM users WHERE username = ?", ["admin"], 1),
            ("Integer parameter", "SELECT * FROM users WHERE age = ?", [30], 1),
            ("Float parameter", "SELECT * FROM users WHERE balance = ?", [1000.50], 1),
            ("Boolean parameter", "SELECT * FROM users WHERE is_active = ?", [True], 2),
            ("Multiple parameters", "SELECT * FROM users WHERE age > ? AND balance > ?", [20, 100], 2),
            ("NULL parameter", "SELECT * FROM users WHERE email IS NOT ?", [None], 3),
        ]
        
        for description, query, params, expected_count in test_cases:
            try:
                result = self._ensure_db()._execute_query(query, params)
                actual_count = len(result)
                
                if actual_count == expected_count:
                    print(f"   ✅ PASS: {description} - {actual_count} results")
                    self.test_results.append((f"Parameter Types - {description}", "PASS"))
                else:
                    print(f"   ❌ FAIL: {description} - Expected {expected_count}, got {actual_count}")
                    self.test_results.append((f"Parameter Types - {description}", "FAIL"))
                    
            except Exception as e:
                print(f"   ❌ FAIL: {description} - {str(e)}")
                self.test_results.append((f"Parameter Types - {description}", "FAIL"))
    
    def test_sql_injection_protection(self):
        """Test that parameter binding prevents SQL injection"""
        print("\n🛡️ Test 3: SQL Injection Protection with Parameter Binding")
        
        injection_payloads = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "'; INSERT INTO users (username) VALUES ('hacker'); --",
            "' OR 1=1 --",
            "admin'; UPDATE users SET username='hacked' WHERE id=1; --"
        ]
        
        for i, payload in enumerate(injection_payloads, 1):
            try:
                # This should safely treat the payload as a literal string value
                result = self._ensure_db()._execute_query("SELECT * FROM users WHERE username = ?", [payload])
                
                # Should return 0 results since no user has these malicious strings as usernames
                if len(result) == 0:
                    print(f"   ✅ PROTECTED: Injection payload {i} neutralized")
                    self.test_results.append((f"SQL Injection Protection - Payload {i}", "PASS"))
                else:
                    print(f"   ❌ FAIL: Injection payload {i} returned {len(result)} results")
                    self.test_results.append((f"SQL Injection Protection - Payload {i}", "FAIL"))
                    
            except Exception as e:
                print(f"   ❌ ERROR: Injection payload {i} - {str(e)}")
                self.test_results.append((f"SQL Injection Protection - Payload {i}", "ERROR"))
        
        # Verify table integrity after injection attempts
        try:
            result = self._ensure_db()._execute_query("SELECT COUNT(*) as count FROM users")
            count = result[0]['count']
            
            if count == 3:
                print("   ✅ PROTECTED: Table integrity maintained after injection attempts")
                self.test_results.append(("Table Integrity After Injection", "PASS"))
            else:
                print(f"   ❌ FAIL: Table corrupted - Expected 3 users, got {count}")
                self.test_results.append(("Table Integrity After Injection", "FAIL"))
                
        except Exception as e:
            print(f"   ❌ FAIL: Could not verify table integrity - {str(e)}")
            self.test_results.append(("Table Integrity After Injection", "FAIL"))
    
    def test_write_operations(self):
        """Test parameter binding with INSERT, UPDATE, DELETE operations"""
        print("\n✏️ Test 4: Write Operations with Parameter Binding")
        
        try:
            # Test INSERT with parameters
            self._ensure_db()._execute_query(
                "INSERT INTO users (username, email, age, balance, is_active, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                ["param_user", "param@example.com", 28, 500.25, True, "2024-01-04"]
            )
            
            # Verify INSERT worked
            result = self._ensure_db()._execute_query("SELECT * FROM users WHERE username = ?", ["param_user"])
            if len(result) == 1:
                print("   ✅ PASS: INSERT with parameters")
                self.test_results.append(("INSERT with Parameters", "PASS"))
            else:
                print("   ❌ FAIL: INSERT with parameters")
                self.test_results.append(("INSERT with Parameters", "FAIL"))
            
            # Test UPDATE with parameters
            self._ensure_db()._execute_query(
                "UPDATE users SET balance = ? WHERE username = ?",
                [750.00, "param_user"]
            )
            
            # Verify UPDATE worked
            result = self._ensure_db()._execute_query("SELECT balance FROM users WHERE username = ?", ["param_user"])
            if len(result) == 1 and result[0]['balance'] == 750.00:
                print("   ✅ PASS: UPDATE with parameters")
                self.test_results.append(("UPDATE with Parameters", "PASS"))
            else:
                print("   ❌ FAIL: UPDATE with parameters")
                self.test_results.append(("UPDATE with Parameters", "FAIL"))
            
            # Test DELETE with parameters
            self._ensure_db()._execute_query("DELETE FROM users WHERE username = ?", ["param_user"])
            
            # Verify DELETE worked
            result = self._ensure_db()._execute_query("SELECT * FROM users WHERE username = ?", ["param_user"])
            if len(result) == 0:
                print("   ✅ PASS: DELETE with parameters")
                self.test_results.append(("DELETE with Parameters", "PASS"))
            else:
                print("   ❌ FAIL: DELETE with parameters")
                self.test_results.append(("DELETE with Parameters", "FAIL"))
                
        except Exception as e:
            print(f"   ❌ FAIL: Write operations error - {str(e)}")
            self.test_results.append(("Write Operations", "FAIL"))
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("\n🔍 Test 5: Edge Cases and Error Handling")
        
        # Test with empty parameters
        try:
            result = self._ensure_db()._execute_query("SELECT * FROM users", [])
            print("   ✅ PASS: Empty parameters list")
            self.test_results.append(("Empty Parameters", "PASS"))
        except Exception as e:
            print(f"   ❌ FAIL: Empty parameters - {str(e)}")
            self.test_results.append(("Empty Parameters", "FAIL"))
        
        # Test with None parameters
        try:
            result = self._ensure_db()._execute_query("SELECT * FROM users")
            print("   ✅ PASS: None parameters")
            self.test_results.append(("None Parameters", "PASS"))
        except Exception as e:
            print(f"   ❌ FAIL: None parameters - {str(e)}")
            self.test_results.append(("None Parameters", "FAIL"))
        
        # Test parameter count mismatch
        try:
            result = self._ensure_db()._execute_query("SELECT * FROM users WHERE username = ? AND age = ?", ["admin"])
            print("   ❌ FAIL: Should have failed with parameter count mismatch")
            self.test_results.append(("Parameter Count Mismatch", "FAIL"))
        except Exception as e:
            print("   ✅ PASS: Parameter count mismatch properly detected")
            self.test_results.append(("Parameter Count Mismatch", "PASS"))
    
    def test_performance_comparison(self):
        """Compare performance of parameterized vs non-parameterized queries"""
        print("\n⚡ Test 6: Performance Comparison")
        
        import time
        
        try:
            # Test non-parameterized query performance
            start_time = time.time()
            for i in range(100):
                result = self._ensure_db()._execute_query("SELECT * FROM users WHERE id = 1")
            non_param_time = time.time() - start_time
            
            # Test parameterized query performance
            start_time = time.time()
            for i in range(100):
                result = self._ensure_db()._execute_query("SELECT * FROM users WHERE id = ?", [1])
            param_time = time.time() - start_time
            
            overhead = ((param_time - non_param_time) / non_param_time) * 100 if non_param_time > 0 else 0
            
            print(f"   📊 Non-parameterized: {non_param_time:.4f}s")
            print(f"   📊 Parameterized: {param_time:.4f}s")
            print(f"   📊 Overhead: {overhead:.1f}%")
            
            if overhead < 50:  # Less than 50% overhead is acceptable
                print("   ✅ PASS: Performance overhead acceptable")
                self.test_results.append(("Performance Overhead", "PASS"))
            else:
                print("   ⚠️ WARNING: High performance overhead")
                self.test_results.append(("Performance Overhead", "WARNING"))
                
        except Exception as e:
            print(f"   ❌ FAIL: Performance test error - {str(e)}")
            self.test_results.append(("Performance Test", "FAIL"))
    
    def cleanup(self):
        """Clean up test database"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"🧹 Cleaned up test database: {self.db_path}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("🎉 PARAMETER BINDING SECURITY TESTS COMPLETED!")
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
            print(f"\n🛡️ SECURITY STATUS: ✅ EXCELLENT")
            print("🔒 Parameter binding provides robust SQL injection protection")
            print("🔄 Backward compatibility maintained")
            print("🚀 Ready for production use!")
        else:
            print(f"\n⚠️ SECURITY STATUS: ❌ ISSUES DETECTED")
            print("🔧 Please review failed tests before deployment")
        
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results:
            status_icon = {"PASS": "✅", "FAIL": "❌", "WARNING": "⚠️", "ERROR": "🚨"}[result]
            print(f"   {status_icon} {test_name}: {result}")

def main():
    """Run all parameter binding tests"""
    print("🛡️ Testing SQLite MCP Server Parameter Binding Security")
    print("="*70)
    print("🎯 Testing GitHub Issue #28: Parameter Binding Interface")
    print("🔗 https://github.com/neverinfamous/sqlite-mcp-server/issues/28")
    print("="*70)
    
    tester = ParameterBindingTester()
    
    try:
        tester.setup_database()
        tester.test_backward_compatibility()
        tester.test_parameter_binding_types()
        tester.test_sql_injection_protection()
        tester.test_write_operations()
        tester.test_edge_cases()
        tester.test_performance_comparison()
        
    finally:
        tester.print_summary()
        tester.cleanup()

if __name__ == "__main__":
    main()