"""
JSON Query Helper Tools for SQLite MCP Server

This module provides high-level JSON-specific MCP tools that abstract away SQL complexity
and provide intelligent error handling for JSON operations in SQLite databases.

Features:
- JSON path validation and normalization
- Auto-normalization of Python-style JSON
- Enhanced error handling with contextual guidance
- Security pattern detection for SQL injection prevention
- Performance-optimized query building
"""

import sqlite3
import json as json_module
import re
from typing import Any, Dict, List, Optional, Union, Tuple
from pathlib import Path

from .json_error_context import provide_advanced_json_error_context
from .diagnostics_isolated import isolated_validate_json
from .jsonb_utils import normalize_json


class JSONPathValidator:
    """Validate and normalize JSON paths for SQLite JSON operations."""
    
    @staticmethod
    def validate_json_path(path: str) -> Dict[str, Any]:
        """
        Validate a JSON path for SQLite compatibility.
        
        Args:
            path: JSON path string (e.g., '$.key', '$.array[0]', '$.nested.field')
            
        Returns:
            Dict with validation results and error context
        """
        if not path:
            return {
                'valid': False,
                'error': 'JSON path cannot be empty',
                'suggestions': ['Provide a valid JSON path starting with "$"']
            }
        
        if not path.startswith('$'):
            return {
                'valid': False,
                'error': 'JSON path must start with "$"',
                'suggestions': [
                    'Use "$" as the root reference (e.g., "$.key")',
                    'For array access use "$.array[index]"',
                    'For nested objects use "$.parent.child"'
                ]
            }
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r';\s*DROP\s+TABLE',
            r';\s*DELETE\s+FROM',
            r';\s*UPDATE\s+',
            r';\s*INSERT\s+INTO',
            r'--',
            r'/\*.*\*/',
            r'\bUNION\b.*\bSELECT\b'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                return {
                    'valid': False,
                    'error': 'Suspicious pattern detected in JSON path',
                    'security_concern': True,
                    'suggestions': [
                        'Remove SQL keywords from JSON path',
                        'Use only valid JSON path syntax',
                        'Avoid comments and SQL statements in paths'
                    ]
                }
        
        # Validate path syntax
        try:
            # Test path with a dummy JSON object
            test_json = {'key': 'value', 'array': [1, 2, 3], 'nested': {'field': 'test'}}
            test_json_str = json_module.dumps(test_json)
            
            # Create a test query to validate path syntax
            test_query = f"SELECT json_extract(?, '{path}')"
            
            # Basic syntax validation without executing
            if '..' in path:
                return {
                    'valid': False,
                    'error': 'Invalid path syntax: consecutive dots not allowed',
                    'suggestions': ['Use single dots to separate object keys (e.g., "$.parent.child")']
                }
            
            # Check for malformed array access
            if '[' in path and ']' not in path:
                return {
                    'valid': False,
                    'error': 'Malformed array access: missing closing bracket',
                    'suggestions': ['Ensure array access uses proper syntax: "$.array[index]"']
                }
            
            if ']' in path and '[' not in path:
                return {
                    'valid': False,
                    'error': 'Malformed array access: missing opening bracket',
                    'suggestions': ['Ensure array access uses proper syntax: "$.array[index]"']
                }
            
            return {
                'valid': True,
                'normalized_path': path,
                'suggestions': []
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Invalid JSON path syntax: {str(e)}',
                'suggestions': [
                    'Check JSON path syntax documentation',
                    'Use valid SQLite JSON path expressions',
                    'Test path with a simple JSON object first'
                ]
            }
    
    @staticmethod
    def create_intermediate_paths(path: str) -> List[str]:
        """
        Generate intermediate paths for creating nested JSON structures.
        
        Args:
            path: Target JSON path
            
        Returns:
            List of paths from root to target
        """
        if not path.startswith('$'):
            return []
        
        parts = path[1:].split('.')  # Remove $ and split
        paths = ['$']
        
        current_path = '$'
        for part in parts:
            if part:  # Skip empty parts
                current_path += f'.{part}'
                paths.append(current_path)
        
        return paths


class JSONQueryBuilder:
    """Build optimized JSON queries with error handling and security validation."""
    
    def __init__(self):
        self.path_validator = JSONPathValidator()
    
    def build_json_insert_query(
        self, 
        table: str, 
        column: str, 
        data: Union[Dict, List, str], 
        where_clause: Optional[str] = None,
        merge_strategy: str = 'replace'
    ) -> Tuple[str, List[Any], Dict[str, Any]]:
        """
        Build a query for JSON insertion with validation.
        
        Args:
            table: Table name
            column: JSON column name
            data: JSON data to insert
            where_clause: Optional WHERE clause for updates
            merge_strategy: 'replace', 'merge', or 'error'
            
        Returns:
            Tuple of (query, params, validation_result)
        """
        # Validate and normalize JSON data
        if isinstance(data, str):
            # Try to parse and validate JSON string
            validation_result = isolated_validate_json(data)
            if not validation_result['valid']:
                # Try auto-normalization
                try:
                    normalized_data = normalize_json(data)
                    validation_result = isolated_validate_json(normalized_data)
                    if validation_result['valid']:
                        json_str = normalized_data
                    else:
                        return "", [], {
                            'valid': False,
                            'error': 'Invalid JSON data after normalization attempt',
                            'validation_details': validation_result
                        }
                except Exception as e:
                    return "", [], {
                        'valid': False,
                        'error': f'JSON normalization failed: {str(e)}',
                        'suggestions': ['Provide valid JSON data or use dict/list objects']
                    }
            else:
                json_str = data
        else:
            # Convert dict/list to JSON string
            try:
                json_str = json_module.dumps(data)
            except Exception as e:
                return "", [], {
                    'valid': False,
                    'error': f'Failed to serialize data to JSON: {str(e)}',
                    'suggestions': ['Ensure data is JSON-serializable']
                }
        
        # Build query based on strategy
        if where_clause:
            if merge_strategy == 'replace':
                query = f"UPDATE {table} SET {column} = ? WHERE {where_clause}"
                params = [json_str]
            elif merge_strategy == 'merge':
                # Use json_patch for merging
                query = f"UPDATE {table} SET {column} = json_patch({column}, ?) WHERE {where_clause}"
                params = [json_str]
            else:  # error strategy
                # Check if data exists first
                check_query = f"SELECT COUNT(*) FROM {table} WHERE {where_clause} AND {column} IS NOT NULL"
                query = f"UPDATE {table} SET {column} = ? WHERE {where_clause} AND {column} IS NULL"
                params = [json_str]
        else:
            # INSERT operation
            query = f"INSERT INTO {table} ({column}) VALUES (?)"
            params = [json_str]
        
        return query, params, {'valid': True, 'normalized': isinstance(data, str)}
    
    def build_json_update_query(
        self, 
        table: str, 
        column: str, 
        path: str, 
        value: Any,
        where_clause: Optional[str] = None,
        create_path: bool = False
    ) -> Tuple[str, List[Any], Dict[str, Any]]:
        """
        Build a query for updating JSON values by path.
        
        Args:
            table: Table name
            column: JSON column name
            path: JSON path to update
            value: New value
            where_clause: Optional WHERE clause
            create_path: Whether to create intermediate paths
            
        Returns:
            Tuple of (query, params, validation_result)
        """
        # Validate JSON path
        path_validation = self.path_validator.validate_json_path(path)
        if not path_validation['valid']:
            return "", [], path_validation
        
        # Serialize value if needed
        if isinstance(value, (dict, list)):
            try:
                value_str = json_module.dumps(value)
            except Exception as e:
                return "", [], {
                    'valid': False,
                    'error': f'Failed to serialize value: {str(e)}',
                    'suggestions': ['Ensure value is JSON-serializable']
                }
        else:
            value_str = value
        
        # Build update query
        if create_path:
            # Use json_set which creates missing paths
            query = f"UPDATE {table} SET {column} = json_set({column}, ?, ?)"
        else:
            # Use json_replace which only updates existing paths
            query = f"UPDATE {table} SET {column} = json_replace({column}, ?, ?)"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        params = [path, value_str]
        
        return query, params, {'valid': True, 'path_validated': True}
    
    def build_json_select_query(
        self, 
        table: str, 
        column: str, 
        paths: List[str],
        where_clause: Optional[str] = None,
        output_format: str = 'structured'
    ) -> Tuple[str, List[Any], Dict[str, Any]]:
        """
        Build a query for selecting JSON data by paths.
        
        Args:
            table: Table name
            column: JSON column name
            paths: List of JSON paths to extract
            where_clause: Optional WHERE clause
            output_format: 'structured', 'flat', or 'raw'
            
        Returns:
            Tuple of (query, params, validation_result)
        """
        # Validate all paths
        path_validations = []
        for path in paths:
            validation = self.path_validator.validate_json_path(path)
            if not validation['valid']:
                return "", [], {
                    'valid': False,
                    'error': f'Invalid path "{path}": {validation["error"]}',
                    'path_validations': path_validations
                }
            path_validations.append(validation)
        
        # Build SELECT clause based on output format
        if output_format == 'structured':
            # Create JSON object with path results
            select_parts = []
            for i, path in enumerate(paths):
                # Use path as key name (remove $. prefix for cleaner keys)
                key_name = path[2:] if path.startswith('$.') else path
                select_parts.append(f"'{key_name}', json_extract({column}, ?)")
            
            select_clause = f"json_object({', '.join(select_parts)})"
        elif output_format == 'flat':
            # Select individual columns
            select_parts = []
            for i, path in enumerate(paths):
                key_name = path[2:] if path.startswith('$.') else path
                # Replace dots and brackets with underscores for valid SQL column names
                safe_key_name = key_name.replace('.', '_').replace('[', '_').replace(']', '')
                select_parts.append(f"json_extract({column}, ?) AS {safe_key_name}")
            
            select_clause = ', '.join(select_parts)
        else:  # raw
            # Just extract the values
            select_parts = [f"json_extract({column}, ?)" for _ in paths]
            select_clause = ', '.join(select_parts)
        
        # Build full query
        query = f"SELECT {select_clause} FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        params = paths
        
        return query, params, {
            'valid': True, 
            'paths_validated': len(paths),
            'output_format': output_format
        }
    
    def build_json_query_complex(
        self,
        table: str,
        column: str,
        filter_paths: Optional[Dict[str, Any]] = None,
        select_paths: Optional[List[str]] = None,
        aggregate: Optional[Dict[str, str]] = None,
        group_by: Optional[str] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> Tuple[str, List[Any], Dict[str, Any]]:
        """
        Build complex JSON queries with filtering, aggregation, and grouping.
        
        Args:
            table: Table name
            column: JSON column name
            filter_paths: Dict of path->value filters
            select_paths: List of paths to select
            aggregate: Dict of alias->aggregation expressions
            group_by: GROUP BY expression
            order_by: ORDER BY expression
            limit: LIMIT value
            
        Returns:
            Tuple of (query, params, validation_result)
        """
        params = []
        
        # Validate filter paths
        if filter_paths:
            for path in filter_paths.keys():
                validation = self.path_validator.validate_json_path(path)
                if not validation['valid']:
                    return "", [], {
                        'valid': False,
                        'error': f'Invalid filter path "{path}": {validation["error"]}'
                    }
        
        # Validate select paths
        if select_paths:
            for path in select_paths:
                validation = self.path_validator.validate_json_path(path)
                if not validation['valid']:
                    return "", [], {
                        'valid': False,
                        'error': f'Invalid select path "{path}": {validation["error"]}'
                    }
        
        # Build SELECT clause
        select_parts = []
        
        if select_paths:
            for path in select_paths:
                key_name = path[2:] if path.startswith('$.') else path
                select_parts.append(f"json_extract({column}, ?) AS {key_name}")
                params.append(path)
        
        if aggregate:
            for alias, expression in aggregate.items():
                select_parts.append(f"{expression} AS {alias}")
        
        if not select_parts:
            select_parts = ["*"]
        
        query = f"SELECT {', '.join(select_parts)} FROM {table}"
        
        # Build WHERE clause
        where_parts = []
        if filter_paths:
            for path, value in filter_paths.items():
                where_parts.append(f"json_extract({column}, ?) = ?")
                params.extend([path, value])
        
        if where_parts:
            query += f" WHERE {' AND '.join(where_parts)}"
        
        # Add GROUP BY
        if group_by:
            query += f" GROUP BY {group_by}"
        
        # Add ORDER BY
        if order_by:
            query += f" ORDER BY {order_by}"
        
        # Add LIMIT
        if limit:
            query += f" LIMIT {limit}"
        
        return query, params, {
            'valid': True,
            'complexity': 'high',
            'filter_paths': len(filter_paths) if filter_paths else 0,
            'select_paths': len(select_paths) if select_paths else 0
        }


def merge_json_objects(obj1: Dict[str, Any], obj2: Dict[str, Any], strategy: str = 'replace') -> Dict[str, Any]:
    """
    Merge two JSON objects with different strategies.
    
    Args:
        obj1: First JSON object
        obj2: Second JSON object
        strategy: 'replace', 'merge_deep', or 'merge_shallow'
        
    Returns:
        Merged JSON object
    """
    if strategy == 'replace':
        return {**obj1, **obj2}
    elif strategy == 'merge_shallow':
        result = obj1.copy()
        result.update(obj2)
        return result
    elif strategy == 'merge_deep':
        def deep_merge(d1, d2):
            result = d1.copy()
            for key, value in d2.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result
        
        return deep_merge(obj1, obj2)
    else:
        raise ValueError(f"Unknown merge strategy: {strategy}")


def validate_json_security(data: Union[str, Dict, List]) -> Dict[str, Any]:
    """
    Validate JSON data for security concerns.
    
    Args:
        data: JSON data to validate
        
    Returns:
        Security validation results
    """
    if isinstance(data, str):
        json_str = data
    else:
        json_str = json_module.dumps(data)
    
    # Check for suspicious patterns
    suspicious_patterns = [
        (r';\s*DROP\s+TABLE', 'SQL DROP statement'),
        (r';\s*DELETE\s+FROM', 'SQL DELETE statement'),
        (r';\s*UPDATE\s+.*SET', 'SQL UPDATE statement'),
        (r';\s*INSERT\s+INTO', 'SQL INSERT statement'),
        (r'\bUNION\b.*\bSELECT\b', 'SQL UNION injection'),
        (r'--.*$', 'SQL comment'),
        (r'/\*.*\*/', 'SQL block comment'),
        (r'<script.*?>', 'XSS script tag'),
        (r'javascript:', 'JavaScript protocol')
    ]
    
    detected_patterns = []
    for pattern, description in suspicious_patterns:
        if re.search(pattern, json_str, re.IGNORECASE | re.MULTILINE):
            detected_patterns.append(description)
    
    return {
        'safe': len(detected_patterns) == 0,
        'detected_patterns': detected_patterns,
        'risk_level': 'high' if detected_patterns else 'low'
    }
