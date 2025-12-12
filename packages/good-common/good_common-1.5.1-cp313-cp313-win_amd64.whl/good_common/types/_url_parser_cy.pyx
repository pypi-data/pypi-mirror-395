# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False
"""
Cython-optimized URL parsing and manipulation functions.

This module provides high-performance URL parsing and canonicalization functions
using Cython optimizations for string operations.
"""

cimport cython
from libc.string cimport strlen, strchr, strncpy
from cpython.unicode cimport PyUnicode_AsUTF8String, PyUnicode_FromString
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from urllib.parse import unquote, quote, urlencode, parse_qs
import re

# Pre-compiled regex patterns
cdef object RE_SCHEME = re.compile(r'^([a-z][a-z0-9+.-]*):')
cdef object RE_WWW_PREFIX = re.compile(r'^www\d*\.')
cdef object RE_PORT_IN_HOST = re.compile(r':(\d+)$')
cdef object RE_TRACKING_PARAMS = re.compile(
    r'^(utm_|ga_|gclid|fbclid|msclkid|mc_|ml_|pk_|cb|_ga|_ke|hmb_|ref|referrer|source|campaign)'
)


@cython.final
cdef class FastURLComponents:
    """Fast container for URL components."""
    
    cdef public str scheme
    cdef public str netloc
    cdef public str path
    cdef public str query
    cdef public str fragment
    cdef public str host
    cdef public int port
    cdef dict _query_dict
    
    def __init__(self, str url):
        self._parse_url(url)
    
    cdef void _parse_url(self, str url):
        """Parse URL into components using fast string operations."""
        cdef str remaining = url
        cdef int idx
        
        # Extract scheme
        match = RE_SCHEME.match(remaining)
        if match:
            self.scheme = match.group(1).lower()
            remaining = remaining[match.end():]
            # Remove '//' after scheme
            if remaining.startswith('//'):
                remaining = remaining[2:]
        else:
            self.scheme = ''
        
        # Extract fragment
        idx = remaining.find('#')
        if idx >= 0:
            self.fragment = remaining[idx+1:]
            remaining = remaining[:idx]
        else:
            self.fragment = ''
        
        # Extract query
        idx = remaining.find('?')
        if idx >= 0:
            self.query = remaining[idx+1:]
            remaining = remaining[:idx]
        else:
            self.query = ''
        
        # Extract netloc and path
        if self.scheme:
            # Find path start
            idx = remaining.find('/')
            if idx >= 0:
                self.netloc = remaining[:idx]
                self.path = remaining[idx:]
            else:
                self.netloc = remaining
                self.path = ''
        else:
            self.netloc = ''
            self.path = remaining
        
        # Parse host and port from netloc
        if self.netloc:
            self._parse_netloc()
        else:
            self.host = ''
            self.port = 0
    
    cdef void _parse_netloc(self):
        """Parse netloc into host and port."""
        # Check for port
        port_match = RE_PORT_IN_HOST.search(self.netloc)
        if port_match:
            self.port = int(port_match.group(1))
            self.host = self.netloc[:port_match.start()]
        else:
            self.port = 0
            self.host = self.netloc
    
    cpdef dict get_query_dict(self):
        """Get query parameters as dictionary."""
        if self._query_dict is None and self.query:
            self._query_dict = parse_qs(self.query, keep_blank_values=True)
        return self._query_dict if self._query_dict is not None else {}
    
    cpdef str reconstruct(self):
        """Reconstruct URL from components."""
        cdef list parts = []
        
        if self.scheme:
            parts.append(self.scheme)
            parts.append('://')
        
        if self.netloc:
            parts.append(self.netloc)
        elif self.host:
            parts.append(self.host)
            if self.port:
                parts.append(':')
                parts.append(str(self.port))
        
        if self.path:
            parts.append(self.path)
        
        if self.query:
            parts.append('?')
            parts.append(self.query)
        
        if self.fragment:
            parts.append('#')
            parts.append(self.fragment)
        
        return ''.join(parts)


cpdef str fast_canonicalize_domain(str domain):
    """
    Fast domain canonicalization.
    
    Removes www prefix and converts to lowercase.
    """
    if not domain:
        return domain
    
    # Convert to lowercase
    domain = domain.lower()
    
    # Remove www prefix
    if RE_WWW_PREFIX.match(domain):
        domain = RE_WWW_PREFIX.sub('', domain, count=1)
    
    return domain


cpdef str fast_clean_path(str path):
    """
    Fast path cleaning.
    
    Removes trailing slashes and normalizes path separators.
    """
    if not path:
        return '/'
    
    # Remove multiple slashes
    while '//' in path:
        path = path.replace('//', '/')
    
    # Remove trailing slash unless it's the root
    if len(path) > 1 and path.endswith('/'):
        path_length = len(path)
        # Avoid negative slicing under wraparound=False by using explicit length
        path = path[:path_length - 1]
    
    return path


cpdef str fast_filter_query_params(str query, set keep_params=None, set remove_params=None):
    """
    Fast query parameter filtering.
    
    Args:
        query: Query string to filter
        keep_params: Set of parameter names to keep (if None, keep all)
        remove_params: Set of parameter names to remove
    
    Returns:
        Filtered query string
    """
    if not query:
        return ''
    
    # Parse query parameters
    params = parse_qs(query, keep_blank_values=True)
    
    # Filter parameters
    filtered = {}
    for key, values in params.items():
        # Skip if in remove list
        if remove_params and key in remove_params:
            continue
        
        # Skip tracking parameters by default
        if not keep_params and RE_TRACKING_PARAMS.match(key):
            continue
        
        # Keep if in keep list or no keep list specified
        if keep_params is None or key in keep_params:
            filtered[key] = values
    
    # Reconstruct query string
    if not filtered:
        return ''
    
    # Sort for consistent output
    sorted_params = []
    for key in sorted(filtered.keys()):
        for value in filtered[key]:
            if value:
                sorted_params.append(f"{key}={quote(value, safe='')}")
            else:
                sorted_params.append(key)
    
    return '&'.join(sorted_params)


cpdef str fast_normalize_url(str url, bint remove_fragment=True, bint remove_tracking=True):
    """
    Fast URL normalization combining multiple operations.
    
    Args:
        url: URL to normalize
        remove_fragment: Whether to remove fragment
        remove_tracking: Whether to remove tracking parameters
    
    Returns:
        Normalized URL
    """
    if not url:
        return url
    
    # Parse URL
    components = FastURLComponents(url)
    
    # Normalize components
    if components.host:
        components.host = fast_canonicalize_domain(components.host)
        # Update netloc
        if components.port:
            components.netloc = f"{components.host}:{components.port}"
        else:
            components.netloc = components.host
    
    if components.path:
        components.path = fast_clean_path(components.path)
    
    if components.query and remove_tracking:
        components.query = fast_filter_query_params(components.query)
    
    if remove_fragment:
        components.fragment = ''
    
    return components.reconstruct()


cpdef tuple split_url_parts(str url):
    """
    Fast URL splitting into main components.
    
    Returns:
        Tuple of (scheme, host, path, query, fragment)
    """
    components = FastURLComponents(url)
    return (
        components.scheme,
        components.host,
        components.path,
        components.query,
        components.fragment
    )


cpdef str join_url_parts(str scheme, str host, str path='', str query='', str fragment=''):
    """
    Fast URL reconstruction from parts.
    """
    cdef list parts = []
    
    if scheme:
        parts.append(scheme)
        parts.append('://')
    
    if host:
        parts.append(host)
    
    if path:
        if not path.startswith('/'):
            parts.append('/')
        parts.append(path)
    elif host:
        parts.append('/')
    
    if query:
        parts.append('?')
        parts.append(query)
    
    if fragment:
        parts.append('#')
        parts.append(fragment)
    
    return ''.join(parts)


cpdef bint is_tracking_param(str param_name):
    """
    Fast check if parameter name is a tracking parameter.
    """
    return bool(RE_TRACKING_PARAMS.match(param_name))


cdef class URLCanonicalizer:
    """Fast URL canonicalization with caching."""
    
    cdef dict _cache
    cdef int _cache_size
    cdef int _max_cache_size
    cdef set _tracking_params
    cdef set _canonical_params
    
    def __init__(self, int max_cache_size=10000):
        self._cache = {}
        self._cache_size = 0
        self._max_cache_size = max_cache_size
        self._tracking_params = {
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
            'gclid', 'fbclid', 'msclkid', 'mc_eid', 'ml_subscriber', 'ml_subscriber_hash',
            'pk_campaign', 'pk_kwd', 'pk_source', 'pk_medium', 'pk_content',
            'cb', '_ga', '_ke', 'hmb_source', 'hmb_medium', 'hmb_campaign',
            'ref', 'referrer', 'source', 'campaign'
        }
        self._canonical_params = set()
    
    cpdef str canonicalize(self, str url):
        """Canonicalize URL with caching."""
        # Check cache
        if url in self._cache:
            return self._cache[url]
        
        # Parse URL to filter with custom tracking params
        components = FastURLComponents(url)
        
        # Normalize components
        if components.host:
            components.host = fast_canonicalize_domain(components.host)
            if components.port:
                components.netloc = f"{components.host}:{components.port}"
            else:
                components.netloc = components.host
        
        if components.path:
            components.path = fast_clean_path(components.path)
        
        # Filter query with our tracking params
        if components.query:
            components.query = fast_filter_query_params(
                components.query,
                remove_params=self._tracking_params,
                keep_params=self._canonical_params if self._canonical_params else None
            )
        
        # Remove fragment
        components.fragment = ''
        
        result = components.reconstruct()
        
        # Cache result
        self._add_to_cache(url, result)
        
        return result
    
    cdef void _add_to_cache(self, str key, str value):
        """Add to cache with LRU eviction."""
        if self._cache_size >= self._max_cache_size:
            # Simple eviction: remove first item (not true LRU but fast)
            first_key = next(iter(self._cache))
            del self._cache[first_key]
            self._cache_size -= 1
        
        self._cache[key] = value
        self._cache_size += 1
    
    cpdef void clear_cache(self):
        """Clear the cache."""
        self._cache.clear()
        self._cache_size = 0
    
    cpdef void set_tracking_params(self, set params):
        """Update tracking parameters set."""
        self._tracking_params = params
    
    cpdef void set_canonical_params(self, set params):
        """Update canonical parameters set."""
        self._canonical_params = params