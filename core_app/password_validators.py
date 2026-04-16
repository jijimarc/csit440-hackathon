"""
Password validation utilities for CertiRequest.
"""

def validate_password_strength(password):
    """
    Validate password strength and return validation result.
    
    Returns: {
        'is_valid': bool,
        'errors': [list of error messages]
    }
    """
    errors = []
    
    if not password:
        errors.append('Password cannot be empty.')
    elif len(password) < 8:
        errors.append('Password must be at least 8 characters long.')
    
    if not any(char.isupper() for char in password):
        errors.append('Password must contain at least one uppercase letter.')
    
    if not any(char.islower() for char in password):
        errors.append('Password must contain at least one lowercase letter.')
    
    if not any(char.isdigit() for char in password):
        errors.append('Password must contain at least one number.')
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }


def validate_password_match(password1, password2):
    """
    Validate that two passwords match.
    
    Returns: {
        'is_valid': bool,
        'error': error message or None
    }
    """
    if password1 != password2:
        return {
            'is_valid': False,
            'error': 'Passwords do not match.'
        }
    
    return {
        'is_valid': True,
        'error': None
    }
