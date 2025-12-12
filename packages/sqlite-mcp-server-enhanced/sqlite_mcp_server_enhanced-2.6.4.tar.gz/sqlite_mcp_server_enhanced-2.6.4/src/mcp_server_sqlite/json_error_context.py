"""
Enhanced JSON error context analysis for complex validation failures.
Provides detailed, actionable error messages for JSON validation issues.
"""
import re
import json as json_module
from typing import Dict, List, Any, Optional


def provide_advanced_json_error_context(
    error_msg: str, 
    original_json: str, 
    normalized_attempt: Optional[str] = None
) -> Dict[str, Any]:
    """
    Provide detailed context for complex JSON validation failures.
    
    Args:
        error_msg: The original error message from JSON parsing
        original_json: The original JSON string that failed
        normalized_attempt: The normalized JSON string if normalization was attempted
        
    Returns:
        Dictionary with detailed error context and suggestions
    """
    context = {
        'auto_normalization_attempted': normalized_attempt is not None,
        'error_type': 'unknown',
        'suggestions': [],
        'security_concern': False,
        'error_details': {},
        'documentation': 'See JSON specification: https://www.json.org/'
    }
    
    # Security-related errors
    if _is_security_violation(error_msg, original_json):
        context.update({
            'error_type': 'security_violation',
            'security_concern': True,
            'suggestions': [
                'Remove SQL keywords and suspicious patterns from JSON content',
                'Use pure JSON data only - avoid database commands',
                'Ensure JSON content does not contain executable code',
                'Consider using parameter binding for dynamic content'
            ],
            'error_details': {
                'detected_patterns': _detect_suspicious_patterns(original_json),
                'risk_level': 'high'
            }
        })
        return context
    
    # Structural JSON errors
    if _is_structural_error(error_msg):
        suggestions, details = _analyze_structural_issues(error_msg, original_json)
        context.update({
            'error_type': 'structural_syntax',
            'suggestions': suggestions,
            'error_details': details
        })
    
    # Character encoding issues
    elif _is_encoding_error(error_msg):
        context.update({
            'error_type': 'encoding_issue',
            'suggestions': [
                'Check for invalid Unicode characters in the JSON string',
                'Ensure text is properly UTF-8 encoded',
                'Remove or escape special control characters (\\u0000-\\u001F)',
                'Verify that all text content uses valid character encodings'
            ],
            'error_details': {
                'encoding_analysis': _analyze_encoding_issues(original_json)
            }
        })
    
    # Value type mismatches
    elif _is_value_type_error(error_msg):
        context.update({
            'error_type': 'value_type_mismatch',
            'suggestions': [
                'Check for unquoted string values that should be quoted',
                'Verify numeric values are properly formatted',
                'Ensure boolean values use lowercase (true/false)',
                'Replace Python-style None with JSON null'
            ],
            'error_details': {
                'type_issues': _analyze_value_types(original_json)
            }
        })
    
    # Complex nested structure issues
    elif _is_nesting_error(error_msg):
        context.update({
            'error_type': 'nesting_structure',
            'suggestions': [
                'Check for unmatched brackets: {} [] ()',
                'Verify proper nesting of objects and arrays',
                'Ensure all opened brackets have corresponding closing brackets',
                'Review complex nested structures for syntax errors'
            ],
            'error_details': {
                'nesting_analysis': _analyze_nesting_structure(original_json)
            }
        })
    
    # Add general suggestions based on JSON characteristics
    _add_general_suggestions(context, original_json, normalized_attempt)
    
    return context


def _is_security_violation(error_msg: str, json_str: str) -> bool:
    """Check if the error is related to security violations."""
    security_indicators = [
        'suspicious input detected',
        'sql injection',
        'security',
        'malicious'
    ]
    
    return any(indicator in error_msg.lower() for indicator in security_indicators)


def _detect_suspicious_patterns(json_str: str) -> List[str]:
    """Detect suspicious patterns that might indicate security issues."""
    patterns = []
    
    sql_patterns = [
        (r';\s*(DROP|DELETE|INSERT|UPDATE|CREATE|ALTER)\s+', 'SQL DDL/DML commands'),
        (r'--\s*$', 'SQL comment patterns'),
        (r'/\*.*\*/', 'SQL block comments'),
        (r'UNION\s+SELECT', 'SQL UNION injection'),
        (r'OR\s+1\s*=\s*1', 'SQL boolean injection'),
        (r'AND\s+1\s*=\s*1', 'SQL boolean injection'),
    ]
    
    for pattern, description in sql_patterns:
        if re.search(pattern, json_str, re.IGNORECASE):
            patterns.append(description)
    
    return patterns


def _is_structural_error(error_msg: str) -> bool:
    """Check if the error is related to JSON structural issues."""
    structural_indicators = [
        'expecting',
        'unterminated',
        'invalid',
        'unexpected',
        'decode',
        'syntax error'
    ]
    
    return any(indicator in error_msg.lower() for indicator in structural_indicators)


def _analyze_structural_issues(error_msg: str, json_str: str):
    """Analyze structural issues in JSON and provide specific suggestions."""
    suggestions = []
    details = {}
    
    # Check for common structural problems
    if 'expecting' in error_msg.lower():
        if ':' in error_msg:
            suggestions.extend([
                'Check for missing colons (:) between keys and values',
                'Ensure all object keys are followed by a colon',
                'Verify proper key-value pair structure: "key": "value"'
            ])
        if ',' in error_msg:
            suggestions.extend([
                'Check comma placement between JSON elements',
                'Remove trailing commas before closing brackets',
                'Ensure commas separate array elements and object properties'
            ])
    
    # Check for trailing comma patterns in the JSON string itself
    if re.search(r',\s*[}\]]', json_str):
        suggestions.extend([
            'Remove trailing comma before closing bracket',
            'Trailing commas are not allowed in JSON',
            'Check comma placement between JSON elements'
        ])
    
    # Analyze bracket matching
    bracket_analysis = _analyze_bracket_matching(json_str)
    if bracket_analysis['unmatched']:
        suggestions.append('Fix unmatched brackets - ensure every opening bracket has a closing bracket')
        details['bracket_analysis'] = bracket_analysis
    
    # Check for quote issues
    quote_analysis = _analyze_quote_issues(json_str)
    if quote_analysis['issues']:
        suggestions.extend([
            'Ensure all strings are enclosed in double quotes (not single quotes)',
            'Check for escaped quotes within string values',
            'Verify that all object keys are properly quoted strings'
        ])
        details['quote_analysis'] = quote_analysis
    
    # Add line-specific error information if available
    if 'line' in error_msg.lower() or 'column' in error_msg.lower():
        line_info = _extract_line_column_info(error_msg)
        if line_info:
            details['position'] = line_info
            suggestions.append(f'Check syntax around line {line_info.get("line", "unknown")}')
    
    return suggestions, details


def _is_encoding_error(error_msg: str) -> bool:
    """Check if the error is related to character encoding."""
    encoding_indicators = [
        'decode',
        'utf',
        'unicode',
        'encoding',
        'character',
        'invalid character'
    ]
    
    return any(indicator in error_msg.lower() for indicator in encoding_indicators)


def _analyze_encoding_issues(json_str: str) -> Dict[str, Any]:
    """Analyze character encoding issues in the JSON string."""
    analysis = {
        'control_characters': [],
        'non_printable': [],
        'encoding_problems': []
    }
    
    # Check for control characters
    for i, char in enumerate(json_str):
        if ord(char) < 32 and char not in ['\t', '\n', '\r']:
            analysis['control_characters'].append({
                'position': i,
                'character': f'\\u{ord(char):04x}',
                'description': 'Control character'
            })
    
    # Check for non-printable characters
    for i, char in enumerate(json_str):
        if not char.isprintable() and char not in ['\t', '\n', '\r']:
            analysis['non_printable'].append({
                'position': i,
                'character': repr(char),
                'description': 'Non-printable character'
            })
    
    return analysis


def _is_value_type_error(error_msg: str) -> bool:
    """Check if the error is related to value type mismatches."""
    type_indicators = [
        'true',
        'false',
        'null',
        'none',
        'boolean',
        'number',
        'string'
    ]
    
    return any(indicator in error_msg.lower() for indicator in type_indicators)


def _analyze_value_types(json_str: str) -> Dict[str, List[Dict[str, Any]]]:
    """Analyze value type issues in the JSON string."""
    issues = {
        'python_booleans': [],
        'python_none': [],
        'unquoted_strings': [],
        'malformed_numbers': []
    }
    
    # Find Python-style booleans
    for match in re.finditer(r'\bTrue\b|\bFalse\b', json_str):
        issues['python_booleans'].append({
            'position': match.start(),
            'value': match.group(),
            'suggestion': match.group().lower()
        })
    
    # Find Python None
    for match in re.finditer(r'\bNone\b', json_str):
        issues['python_none'].append({
            'position': match.start(),
            'value': match.group(),
            'suggestion': 'null'
        })
    
    # Find potential unquoted strings (heuristic)
    for match in re.finditer(r':\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*[,}]', json_str):
        if match.group(1) not in ['true', 'false', 'null']:
            issues['unquoted_strings'].append({
                'position': match.start(1),
                'value': match.group(1),
                'suggestion': f'"{match.group(1)}"'
            })
    
    return issues


def _is_nesting_error(error_msg: str) -> bool:
    """Check if the error is related to nesting structure."""
    nesting_indicators = [
        'bracket',
        'brace',
        'parenthesis',
        'nested',
        'depth',
        'structure'
    ]
    
    return any(indicator in error_msg.lower() for indicator in nesting_indicators)


def _analyze_nesting_structure(json_str: str) -> Dict[str, Any]:
    """Analyze nesting structure issues."""
    analysis = {
        'max_depth': 0,
        'current_depth': 0,
        'bracket_stack': [],
        'unmatched_positions': []
    }
    
    bracket_pairs = {'(': ')', '[': ']', '{': '}'}
    stack = []
    
    for i, char in enumerate(json_str):
        if char in bracket_pairs:
            stack.append((char, i))
            analysis['current_depth'] = len(stack)
            analysis['max_depth'] = max(analysis['max_depth'], analysis['current_depth'])
        elif char in bracket_pairs.values():
            if stack:
                opening_char, opening_pos = stack.pop()
                expected_closing = bracket_pairs[opening_char]
                if char != expected_closing:
                    analysis['unmatched_positions'].append({
                        'position': i,
                        'found': char,
                        'expected': expected_closing,
                        'opening_position': opening_pos
                    })
            else:
                analysis['unmatched_positions'].append({
                    'position': i,
                    'found': char,
                    'expected': None,
                    'error': 'Closing bracket without matching opening bracket'
                })
    
    # Check for unclosed brackets
    for opening_char, opening_pos in stack:
        analysis['unmatched_positions'].append({
            'position': opening_pos,
            'found': opening_char,
            'expected': bracket_pairs[opening_char],
            'error': 'Opening bracket never closed'
        })
    
    return analysis


def _analyze_bracket_matching(json_str: str) -> Dict[str, Any]:
    """Analyze bracket matching in the JSON string."""
    brackets = {'(': 0, '[': 0, '{': 0, ')': 0, ']': 0, '}': 0}
    
    for char in json_str:
        if char in brackets:
            brackets[char] += 1
    
    return {
        'unmatched': (
            brackets['('] != brackets[')'] or
            brackets['['] != brackets[']'] or
            brackets['{'] != brackets['}']
        ),
        'counts': brackets,
        'analysis': {
            'parentheses': brackets['('] - brackets[')'],
            'square_brackets': brackets['['] - brackets[']'],
            'curly_braces': brackets['{'] - brackets['}']
        }
    }


def _analyze_quote_issues(json_str: str) -> Dict[str, Any]:
    """Analyze quote-related issues in the JSON string."""
    analysis = {
        'issues': False,
        'single_quotes': [],
        'unmatched_quotes': [],
        'escaped_quotes': []
    }
    
    # Find single quotes that might need to be double quotes
    single_quote_pattern = r"'([^']*)'"
    for match in re.finditer(single_quote_pattern, json_str):
        analysis['single_quotes'].append({
            'position': match.start(),
            'content': match.group(1),
            'suggestion': f'"{match.group(1)}"'
        })
        analysis['issues'] = True
    
    return analysis


def _extract_line_column_info(error_msg: str) -> Optional[Dict[str, int]]:
    """Extract line and column information from error message."""
    line_pattern = r'line\s+(\d+)'
    column_pattern = r'column\s+(\d+)'
    
    line_match = re.search(line_pattern, error_msg, re.IGNORECASE)
    column_match = re.search(column_pattern, error_msg, re.IGNORECASE)
    
    info = {}
    if line_match:
        info['line'] = int(line_match.group(1))
    if column_match:
        info['column'] = int(column_match.group(1))
    
    return info if info else None


def _add_general_suggestions(
    context: Dict[str, Any], 
    original_json: str, 
    normalized_attempt: Optional[str]
) -> None:
    """Add general suggestions based on JSON characteristics."""
    
    # Check for security patterns regardless of error type
    suspicious_patterns = _detect_suspicious_patterns(original_json)
    if suspicious_patterns:
        context['security_concern'] = True
        context['suggestions'].extend([
            'WARNING: Potential security risk detected in JSON content',
            'Review content for SQL injection patterns or malicious code',
            'Ensure user input is properly sanitized before processing'
        ])
        context['error_details']['security_patterns'] = suspicious_patterns
    
    # Large JSON suggestion
    if len(original_json) > 10000:
        context['suggestions'].append(
            'Consider breaking large JSON into smaller, manageable chunks'
        )
        context['error_details']['size_analysis'] = {
            'size': len(original_json),
            'recommendation': 'Split into smaller objects for better error diagnosis'
        }
    
    # Normalization attempt feedback
    if normalized_attempt:
        context['error_details']['normalization'] = {
            'attempted': True,
            'original_size': len(original_json),
            'normalized_size': len(normalized_attempt),
            'changes_made': original_json != normalized_attempt
        }
        
        if original_json != normalized_attempt:
            context['suggestions'].append(
                'Auto-normalization was attempted but the result is still invalid'
            )
    
    # Add context about JSON validation tools
    if context['error_type'] != 'security_violation':
        context['suggestions'].extend([
            'Use a JSON validator tool to identify the exact syntax error',
            'Check the JSON against the official specification at json.org',
            'Consider using a JSON formatter to identify structural issues'
        ])
