# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
"""
Cython-optimized string utility functions.
"""

import re
cimport cython
from libc.string cimport strlen

# Compile regexes once
cdef object RE_UUID = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
cdef object RE_URL = re.compile(r'^https?://')
cdef object RE_EMAIL = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
cdef object RE_CAMEL_SPLIT = re.compile(r'(?<!^)(?=[A-Z])')


cpdef str camel_to_snake(str name):
    """
    Convert CamelCase to snake_case.
    
    Optimized with:
    - Pre-compiled regex
    - Direct string manipulation
    """
    # Insert underscores before uppercase letters
    return RE_CAMEL_SPLIT.sub('_', name).lower()


cpdef str snake_to_camel(str name):
    """
    Convert snake_case to CamelCase.
    
    Optimized with:
    - Direct string building
    - Reduced intermediate objects
    """
    cdef list parts = name.split('_')
    cdef list result = []
    cdef str part
    
    for part in parts:
        if part:
            result.append(part[0].upper() + part[1:] if len(part) > 1 else part.upper())
    
    return ''.join(result)


cpdef str camel_to_kebab(str name, list protected_acronyms=None):
    """
    Convert CamelCase to kebab-case.
    
    Optimized with:
    - Pre-compiled regex
    - Efficient string replacement
    """
    if protected_acronyms:
        # Handle protected acronyms
        name = RE_CAMEL_SPLIT.sub('-', name, count=1)
        for acronym in protected_acronyms:
            name = name.replace(acronym, f'_{acronym}_')
        return name.replace('_', '-').lower()
    else:
        return RE_CAMEL_SPLIT.sub('-', name).lower()


cpdef str snake_to_kebab(str name):
    """Convert snake_case to kebab-case."""
    return name.replace('_', '-')


cpdef str kebab_to_snake(str name):
    """Convert kebab-case to snake_case."""
    return name.replace('-', '_')


cpdef str kebab_to_camel(str name):
    """Convert kebab-case to CamelCase."""
    cdef list parts = name.split('-')
    cdef list result = []
    cdef str part
    
    for part in parts:
        if part:
            result.append(part[0].upper() + part[1:] if len(part) > 1 else part.upper())
    
    return ''.join(result)


cpdef bint is_uuid(str s):
    """
    Check if string is a valid UUID.
    
    Optimized with:
    - Pre-compiled regex
    - Fast pattern matching
    """
    return RE_UUID.match(s) is not None


cpdef str detect_string_type(str string):
    """
    Detect the type of a string.
    
    Optimized with:
    - Pre-compiled regexes
    - Early termination
    - Ordered by likelihood
    """
    cdef int length = len(string)
    
    # Quick checks first
    if length == 0:
        return "unknown"
    
    # Check for URLs (most common in web contexts)
    if RE_URL.match(string):
        if string.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            return "url-image"
        elif string.endswith(('.mp4', '.webm', '.ogv')):
            return "url-video"
        else:
            return "url"
    
    # Check for UUID (fixed length)
    if length == 36 and RE_UUID.match(string):
        return "uuid"
    
    # Check for email
    if '@' in string and RE_EMAIL.match(string):
        return "email-address"
    
    # Check for JSON (starts with { or [)
    if string[0] in '{[':
        try:
            import orjson
            orjson.loads(string)
            return "json-string"
        except:
            pass
    
    # Check for dates (common formats)
    if length == 10 and string[4] == '-' and string[7] == '-':
        try:
            import datetime
            datetime.datetime.strptime(string, "%Y-%m-%d")
            return "date-string"
        except:
            pass
    
    # Check for HTML
    if '<' in string and '>' in string:
        if string.strip().startswith('<') and string.strip().endswith('>'):
            return "html"
    
    # Default
    return "unknown"


cpdef str encode_base32(unsigned long long n):
    """
    Encode a 64-bit integer into a Base32 string.
    
    Optimized with:
    - Direct integer manipulation
    - Pre-allocated result
    """
    if n >= (1 << 64):
        raise ValueError("Input must be a 64-bit unsigned integer")
    
    cdef str alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    cdef list result = []
    cdef unsigned long long remainder
    
    # Convert to base32
    while n:
        n, remainder = divmod(n, 32)
        result.append(alphabet[remainder])
    
    # Handle zero case
    if not result:
        return "A"
    
    # Reverse and pad
    result.reverse()
    result_str = ''.join(result)
    
    # Left pad with 'A' to ensure 13-character length
    if len(result_str) < 13:
        result_str = 'A' * (13 - len(result_str)) + result_str
    
    return result_str


cpdef str camel_to_slug(str s, bint force_lower=True):
    """
    Convert CamelCase to slug format.
    
    Optimized with:
    - Direct string manipulation
    - Single pass conversion
    """
    # Insert underscores before capitals
    result = RE_CAMEL_SPLIT.sub('_', s)
    
    # Remove leading underscore
    if result and result[0] == '_':
        result = result[1:]
    
    # Clean up multiple underscores
    while '__' in result:
        result = result.replace('__', '_')
    
    return result.lower() if force_lower else result


cpdef str slug_to_camel(str s):
    """Convert slug to CamelCase."""
    return snake_to_camel(s)


cpdef str slug_to_snake(str s):
    """Convert slug to snake_case."""
    return s.replace('-', '_')


cpdef str slug_to_kebab(str s):
    """Convert slug to kebab-case."""
    return s.replace('_', '-')