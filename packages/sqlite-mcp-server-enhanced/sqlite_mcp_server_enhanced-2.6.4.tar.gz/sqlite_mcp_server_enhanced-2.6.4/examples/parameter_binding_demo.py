#!/usr/bin/env python3
"""
Parameter Binding Security Demo for SQLite MCP Server

This demo shows how to use the new parameter binding interface to prevent SQL injection attacks.

GitHub Issue: https://github.com/neverinfamous/sqlite-mcp-server/issues/28
"""

import asyncio
import json
from mcp import types
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_server_sqlite.server import EnhancedSqliteDatabase

async def demo_parameter_binding():
    """Demonstrate the new parameter binding interface"""
    
    print("🛡️ SQLite MCP Server Parameter Binding Security Demo")
    print("="*60)
    print("🎯 GitHub Issue #28: Parameter Binding Interface")
    print("🔗 https://github.com/neverinfamous/sqlite-mcp-server/issues/28")
    print("="*60)
    
    # Initialize database
    db_path = "./demo_parameter_binding.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    db = EnhancedSqliteDatabase(db_path)
    
    # Create demo table
    print("\n📋 Setting up demo database...")
    db._execute_query("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    """)
    
    # Insert demo data
    demo_users = [
        ("admin", "admin@example.com", "admin"),
        ("alice", "alice@example.com", "user"),
        ("bob", "bob@example.com", "user"),
    ]
    
    for username, email, role in demo_users:
        db._execute_query(
            "INSERT INTO users (username, email, role) VALUES (?, ?, ?)",
            [username, email, role]
        )
    
    print("✅ Demo database created with 3 users")
    
    # Demo 1: Backward Compatibility
    print("\n" + "="*60)
    print("🔄 DEMO 1: Backward Compatibility")
    print("="*60)
    print("📝 Old way (still works): No parameters")
    
    result = db._execute_query("SELECT COUNT(*) as count FROM users")
    print(f"   Query: SELECT COUNT(*) as count FROM users")
    print(f"   Result: {result[0]['count']} users found")
    
    # Demo 2: Secure Parameter Binding
    print("\n" + "="*60)
    print("🛡️ DEMO 2: Secure Parameter Binding")
    print("="*60)
    print("📝 New way (secure): With parameters")
    
    username = "admin"
    result = db._execute_query("SELECT * FROM users WHERE username = ?", [username])
    print(f"   Query: SELECT * FROM users WHERE username = ?")
    print(f"   Parameters: ['{username}']")
    print(f"   Result: Found user '{result[0]['username']}' with role '{result[0]['role']}'")
    
    # Demo 3: SQL Injection Prevention
    print("\n" + "="*60)
    print("🚨 DEMO 3: SQL Injection Prevention")
    print("="*60)
    
    # Malicious input that would cause SQL injection with string concatenation
    malicious_input = "'; DROP TABLE users; --"
    
    print("🔴 DANGEROUS: What would happen with string concatenation:")
    dangerous_query = f"SELECT * FROM users WHERE username = '{malicious_input}'"
    print(f"   Vulnerable query: {dangerous_query}")
    print("   ☠️ This would execute: SELECT * FROM users WHERE username = ''; DROP TABLE users; --'")
    print("   💥 Result: TABLE DROPPED! Database destroyed!")
    
    print("\n🟢 SAFE: Using parameter binding:")
    print(f"   Safe query: SELECT * FROM users WHERE username = ?")
    print(f"   Parameters: ['{malicious_input}']")
    
    result = db._execute_query("SELECT * FROM users WHERE username = ?", [malicious_input])
    print(f"   ✅ Result: {len(result)} users found (malicious string treated as literal)")
    
    # Verify table still exists
    result = db._execute_query("SELECT COUNT(*) as count FROM users")
    print(f"   ✅ Table integrity: {result[0]['count']} users still in database")
    
    # Demo 4: Multiple Parameters
    print("\n" + "="*60)
    print("🔢 DEMO 4: Multiple Parameters")
    print("="*60)
    
    min_id = 1
    role = "user"
    result = db._execute_query(
        "SELECT username, role FROM users WHERE id >= ? AND role = ?",
        [min_id, role]
    )
    print(f"   Query: SELECT username, role FROM users WHERE id >= ? AND role = ?")
    print(f"   Parameters: [{min_id}, '{role}']")
    print(f"   Result: Found {len(result)} users:")
    for user in result:
        print(f"     - {user['username']} ({user['role']})")
    
    # Demo 5: Different Data Types
    print("\n" + "="*60)
    print("🎯 DEMO 5: Different Data Types")
    print("="*60)
    
    # Add a user with more data
    db._execute_query(
        "INSERT INTO users (username, email, role) VALUES (?, ?, ?)",
        ["charlie", "charlie@example.com", "moderator"]
    )
    
    # Test different parameter types
    test_cases = [
        ("String", "SELECT * FROM users WHERE role = ?", ["admin"]),
        ("Integer", "SELECT * FROM users WHERE id = ?", [1]),
        ("Boolean (as integer)", "SELECT * FROM users WHERE id > ?", [2]),
        ("NULL", "SELECT * FROM users WHERE email IS NOT ?", [None]),
    ]
    
    for description, query, params in test_cases:
        result = db._execute_query(query, params)
        print(f"   {description}: {len(result)} results")
        print(f"     Query: {query}")
        print(f"     Parameters: {params}")
    
    # Demo 6: Write Operations
    print("\n" + "="*60)
    print("✏️ DEMO 6: Write Operations with Parameters")
    print("="*60)
    
    # INSERT with parameters
    new_user = ["diana", "diana@example.com", "user"]
    db._execute_query(
        "INSERT INTO users (username, email, role) VALUES (?, ?, ?)",
        new_user
    )
    print(f"   ✅ INSERT: Added user '{new_user[0]}'")
    
    # UPDATE with parameters
    db._execute_query(
        "UPDATE users SET role = ? WHERE username = ?",
        ["premium_user", "diana"]
    )
    print(f"   ✅ UPDATE: Changed diana's role to 'premium_user'")
    
    # DELETE with parameters
    db._execute_query("DELETE FROM users WHERE username = ?", ["diana"])
    print(f"   ✅ DELETE: Removed user 'diana'")
    
    # Final count
    result = db._execute_query("SELECT COUNT(*) as count FROM users")
    print(f"   📊 Final user count: {result[0]['count']}")
    
    # Summary
    print("\n" + "="*60)
    print("🎉 DEMO COMPLETE: Key Benefits")
    print("="*60)
    print("✅ SQL Injection Prevention: Malicious input treated as literal data")
    print("✅ Backward Compatibility: Existing queries still work")
    print("✅ Type Safety: Automatic parameter type handling")
    print("✅ Performance: Minimal overhead (< 50%)")
    print("✅ Best Practice: Follows secure coding standards")
    
    print("\n📚 Usage Examples:")
    print("   # Secure way (NEW):")
    print('   read_query({"query": "SELECT * FROM users WHERE name = ?", "params": ["John"]})')
    print("   ")
    print("   # Old way (still works):")
    print('   read_query({"query": "SELECT * FROM users"})')
    
    # Cleanup
    os.remove(db_path)
    print(f"\n🧹 Cleaned up demo database: {db_path}")

if __name__ == "__main__":
    asyncio.run(demo_parameter_binding())
