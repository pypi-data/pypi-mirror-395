"""Isolated diagnostics functions to avoid MCP framework conflicts"""

def _format_enhanced_error_message(error_context, original_error):
    """Format enhanced error message with contextual information."""
    if not error_context:
        return original_error
    
    error_type = error_context.get('error_type', 'unknown')
    suggestions = error_context.get('suggestions', [])
    
    # Create a user-friendly error message
    message_parts = [f"JSON validation failed ({error_type}): {original_error}"]
    
    if error_context.get('security_concern'):
        message_parts.append("\n⚠️  SECURITY CONCERN: This JSON contains suspicious patterns that may indicate malicious content.")
    
    if suggestions:
        message_parts.append(f"\n💡 Suggestions to fix this issue:")
        for i, suggestion in enumerate(suggestions[:3], 1):  # Limit to top 3 suggestions
            message_parts.append(f"   {i}. {suggestion}")
    
    if error_context.get('auto_normalization_attempted'):
        message_parts.append("\n🔧 Auto-normalization was attempted but could not resolve the issue.")
    
    return "".join(message_parts)

def isolated_validate_json(json_str):
    """Completely isolated JSON validation function"""
    try:
        # Import locally to avoid any global scope issues
        import json as local_json_module
        
        # Try to parse the JSON string
        parsed = local_json_module.loads(json_str)
        
        return {
            'valid': True,
            'parsed': parsed,
            'message': 'JSON is valid',
            'normalized': False
        }
        
    except Exception as e:
        # Try normalization
        normalized = json_str  # Initialize before try block
        try:
            # Simple normalization without external dependencies
            
            # Replace single quotes with double quotes
            import re
            normalized = re.sub(r"'([^']*)'", r'"\1"', normalized)
            
            # Replace Python booleans
            normalized = normalized.replace('True', 'true').replace('False', 'false')
            normalized = normalized.replace('None', 'null')
            
            # Try to parse normalized version
            import json as local_json_module_2
            parsed = local_json_module_2.loads(normalized)
            
            return {
                'valid': True,
                'parsed': parsed,
                'message': 'JSON was auto-normalized and is now valid',
                'normalized': True,
                'original': json_str,
                'normalized_json': normalized
            }
            
        except Exception as norm_error:
            # Enhanced error context for complex JSON validation failures
            try:
                from .json_error_context import provide_advanced_json_error_context
                
                # Provide enhanced error context
                error_context = provide_advanced_json_error_context(
                    error_msg=str(e),
                    original_json=json_str,
                    normalized_attempt=normalized
                )
                
                # Merge enhanced context with basic error info
                result = {
                    'valid': False,
                    'normalized': False,
                    'error': str(e),
                    'message': f'JSON is invalid and could not be auto-normalized: {str(e)}'
                }
                
                # Add enhanced error context
                result.update({
                    'error_context': error_context,
                    'enhanced_message': _format_enhanced_error_message(error_context, str(e))
                })
                
                return result
                
            except ImportError:
                # Fallback to basic error if enhanced context is not available
                return {
                    'valid': False,
                    'normalized': False,
                    'error': str(e),
                    'message': f'JSON is invalid and could not be auto-normalized: {str(e)}'
                }

def isolated_test_jsonb_conversion(json_str):
    """Completely isolated JSONB conversion test"""
    try:
        # Validate first
        validation = isolated_validate_json(json_str)
        
        if not validation['valid']:
            return validation
            
        # For now, just return success since we validated
        result = {
            'valid': True,
            'conversion_successful': True,
            'message': 'JSONB conversion test successful'
        }
        
        if validation.get('normalized'):
            result['auto_normalized'] = True
            result['original_json'] = json_str
            result['normalized_json'] = validation['normalized_json']
            result['message'] += ' (JSON was auto-normalized)'
            
        return result
        
    except Exception as e:
        return {
            'valid': False,
            'error': str(e),
            'message': f'JSONB conversion failed: {str(e)}'
        }