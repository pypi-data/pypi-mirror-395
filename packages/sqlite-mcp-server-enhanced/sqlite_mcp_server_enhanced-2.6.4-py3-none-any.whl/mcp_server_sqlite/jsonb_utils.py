"""JSONB utilities for SQLite with JSON auto-normalization"""
import json as json_module
import sqlite3
import re
import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

# Configuration for strict mode
SQLITE_JSON_STRICT_MODE = os.getenv('SQLITE_JSON_STRICT_MODE', 'false').lower() == 'true'

def normalize_json(json_str, strict_mode=None):
    """
    Auto-repair common JSON formatting issues with security safeguards.
    
    Args:
        json_str: The JSON string to normalize
        strict_mode: Override global strict mode setting
        
    Returns:
        Normalized JSON string
        
    Raises:
        ValueError: If suspicious input is detected or strict mode rejects input
    """
    if strict_mode is None:
        strict_mode = SQLITE_JSON_STRICT_MODE
    
    if not isinstance(json_str, str):
        return json_str
    
    # In strict mode, no normalization is performed
    if strict_mode:
        return json_str
    
    # Security check: Detect obvious SQL injection patterns
    sql_injection_patterns = [
        r';\s*(DROP|DELETE|INSERT|UPDATE|CREATE|ALTER)\s+',
        r'--\s*$',
        r'/\*.*\*/',
        r'UNION\s+SELECT',
        r'OR\s+1\s*=\s*1',
        r'AND\s+1\s*=\s*1',
    ]
    
    for pattern in sql_injection_patterns:
        if re.search(pattern, json_str, re.IGNORECASE):
            logger.warning(f"Potential SQL injection detected in JSON input: {json_str[:100]}...")
            raise ValueError("Suspicious input detected - normalization rejected for security")
    
    original_str = json_str
    normalization_applied = []
    
    # 1. Replace single quotes with double quotes (comprehensive approach)
    original_before_quotes = json_str
    
    # Replace all single quotes with double quotes
    # This simple regex works well for most JSON-like structures
    json_str = re.sub(r"'([^']*)'", r'"\1"', json_str)
    
    if json_str != original_before_quotes:
        normalization_applied.append("single quotes to double quotes for keys")
        normalization_applied.append("single quotes to double quotes for values")
    
    # 3. Remove trailing commas before closing braces/brackets
    if re.search(r',(\s*[}\]])', json_str):
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        normalization_applied.append("removed trailing commas")
    
    # 4. Replace Python boolean values with JSON boolean values
    if 'True' in json_str or 'False' in json_str:
        json_str = json_str.replace('True', 'true').replace('False', 'false')
        normalization_applied.append("Python booleans to JSON booleans")
    
    # 5. Replace Python None with JSON null
    if 'None' in json_str:
        json_str = json_str.replace('None', 'null')
        normalization_applied.append("Python None to JSON null")
    
    # Log normalization if any was applied
    if normalization_applied and json_str != original_str:
        logger.info(f"JSON auto-normalization applied: {', '.join(normalization_applied)}")
        logger.debug(f"Original: {original_str[:200]}...")
        logger.debug(f"Normalized: {json_str[:200]}...")
    
    return json_str

def validate_json(json_str, auto_normalize=True, strict_mode=None):
    """
    Validate JSON string with optional auto-normalization.
    
    Args:
        json_str: The JSON string to validate
        auto_normalize: Whether to attempt auto-normalization on invalid JSON
        strict_mode: Override global strict mode setting
        
    Returns:
        tuple: (is_valid, normalized_json_str)
    """
    if strict_mode is None:
        strict_mode = SQLITE_JSON_STRICT_MODE
    
    # First, try to validate as-is
    try:
        json_module.loads(json_str)
        return True, json_str
    except (json_module.JSONDecodeError, TypeError):
        pass
    
    # If auto-normalization is disabled or strict mode is enabled, return failure
    if not auto_normalize or strict_mode:
        return False, json_str
    
    # Try to normalize and validate again
    try:
        normalized_str = normalize_json(json_str, strict_mode=strict_mode)
        json_module.loads(normalized_str)
        return True, normalized_str
    except (json_module.JSONDecodeError, TypeError, ValueError) as e:
        logger.debug(f"JSON normalization failed: {e}")
        return False, json_str

def convert_to_jsonb(conn, json_str, auto_normalize=True):
    """
    Convert JSON string to JSONB binary format with optional auto-normalization.
    
    Args:
        conn: SQLite database connection
        json_str: The JSON string to convert
        auto_normalize: Whether to attempt auto-normalization
        
    Returns:
        JSONB binary data or None if conversion fails
    """
    try:
        # Validate and potentially normalize the JSON
        is_valid, normalized_json = validate_json(json_str, auto_normalize=auto_normalize)
        
        if not is_valid:
            logger.warning(f"Invalid JSON cannot be converted to JSONB: {json_str[:100]}...")
            return None
        
        cursor = conn.cursor()
        cursor.execute("SELECT jsonb(?)", (normalized_json,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"Error converting to JSONB: {e}")
        return None

def convert_from_jsonb(conn, jsonb_data):
    """Convert JSONB binary data back to JSON string"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT json(?)", (jsonb_data,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"Error converting from JSONB: {e}")
        return None

# Legacy function for backward compatibility
def validate_json_legacy(json_str):
    """Legacy validate function - kept for backward compatibility"""
    is_valid, _ = validate_json(json_str)
    return is_valid