# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False
"""
Cython-optimized pattern matching for URL classification and domain rules.

This module provides high-performance regex pattern matching with caching
for URL classification and domain-specific rule matching.
"""

cimport cython
from cpython cimport bool
from cpython.dict cimport PyDict_GetItem, PyDict_SetItem
import re
from typing import Dict, Pattern, Optional, Set, List


@cython.final
cdef class CompiledPatternMatcher:
    """
    Pre-compiled pattern matching with Cython optimization and LRU caching.
    """
    
    cdef dict _patterns
    cdef dict _match_cache
    cdef list _cache_keys  # For LRU ordering
    cdef int _cache_size
    cdef int _max_cache_size
    cdef object _lock  # For thread safety
    
    def __init__(self, int max_cache_size=10000):
        self._patterns = {}
        self._match_cache = {}
        self._cache_keys = []
        self._cache_size = 0
        self._max_cache_size = max_cache_size
        self._lock = None  # Can add threading.Lock() if needed
    
    cpdef void add_pattern(self, str name, str pattern, int flags=0):
        """
        Add a named pattern to the matcher.
        
        Args:
            name: Pattern name for reference
            pattern: Regular expression pattern
            flags: Regex flags (e.g., re.IGNORECASE)
        """
        self._patterns[name] = re.compile(pattern, flags)
    
    cpdef void add_compiled_pattern(self, str name, object pattern):
        """
        Add an already compiled pattern.
        
        Args:
            name: Pattern name for reference
            pattern: Compiled regex pattern
        """
        self._patterns[name] = pattern
    
    cpdef bool matches(self, str text, str pattern_name):
        """
        Check if text matches a named pattern with caching.
        
        Args:
            text: Text to match
            pattern_name: Name of pattern to use
        
        Returns:
            True if matches, False otherwise
        """
        # Create cache key
        cdef str cache_key = f"{pattern_name}:{text}"
        
        # Check cache
        if cache_key in self._match_cache:
            # Move to end for LRU
            self._update_lru(cache_key)
            return self._match_cache[cache_key]
        
        # Get pattern
        pattern = self._patterns.get(pattern_name)
        if pattern is None:
            return False
        
        # Perform match
        cdef bool result = bool(pattern.search(text))
        
        # Cache result
        self._cache_result(cache_key, result)
        
        return result
    
    cpdef object match(self, str text, str pattern_name):
        """
        Get match object for pattern.
        
        Returns:
            Match object or None
        """
        pattern = self._patterns.get(pattern_name)
        if pattern is None:
            return None
        return pattern.search(text)
    
    cpdef str find_first_match(self, str text, list pattern_names):
        """
        Find first matching pattern from a list.
        
        Args:
            text: Text to match
            pattern_names: List of pattern names to try
        
        Returns:
            Name of first matching pattern or None
        """
        for pattern_name in pattern_names:
            if self.matches(text, pattern_name):
                return pattern_name
        return None
    
    cpdef list find_all_matches(self, str text, list pattern_names=None):
        """
        Find all matching patterns.
        
        Args:
            text: Text to match
            pattern_names: List of pattern names to try (or all if None)
        
        Returns:
            List of matching pattern names
        """
        if pattern_names is None:
            pattern_names = list(self._patterns.keys())
        
        cdef list matches = []
        for pattern_name in pattern_names:
            if self.matches(text, pattern_name):
                matches.append(pattern_name)
        
        return matches
    
    cdef void _cache_result(self, str key, bool value):
        """Add result to cache with LRU eviction."""
        if self._cache_size >= self._max_cache_size:
            self._evict_oldest()
        
        self._match_cache[key] = value
        self._cache_keys.append(key)
        self._cache_size += 1
    
    cdef void _update_lru(self, str key):
        """Update LRU order for existing key."""
        # Remove from current position and add to end
        try:
            self._cache_keys.remove(key)
            self._cache_keys.append(key)
        except ValueError:
            # Key not in list, shouldn't happen but handle gracefully
            pass
    
    cdef void _evict_oldest(self):
        """Evict oldest entry from cache."""
        if self._cache_keys:
            oldest_key = self._cache_keys.pop(0)
            del self._match_cache[oldest_key]
            self._cache_size -= 1
    
    cpdef void clear_cache(self):
        """Clear the match cache."""
        self._match_cache.clear()
        self._cache_keys.clear()
        self._cache_size = 0
    
    cpdef dict get_patterns(self):
        """Get all pattern names."""
        return {name: pattern.pattern for name, pattern in self._patterns.items()}
    
    cpdef int cache_size(self):
        """Get current cache size."""
        return self._cache_size


@cython.final
cdef class DomainRuleMatcher:
    """
    Fast domain-specific rule matching with caching.
    """
    
    cdef dict _domain_patterns  # domain pattern -> rules
    cdef dict _exact_domains    # exact domain -> rules
    cdef dict _cache
    cdef int _cache_size
    cdef int _max_cache_size
    
    def __init__(self, int max_cache_size=5000):
        self._domain_patterns = {}
        self._exact_domains = {}
        self._cache = {}
        self._cache_size = 0
        self._max_cache_size = max_cache_size
    
    cpdef void add_domain_rule(self, str domain_pattern, dict rules):
        """
        Add rules for a domain pattern.
        
        Args:
            domain_pattern: Domain pattern (can include wildcards)
            rules: Dictionary of rules for this domain
        """
        if '*' in domain_pattern or '?' in domain_pattern:
            # Convert to regex pattern
            import fnmatch
            regex_pattern = fnmatch.translate(domain_pattern)
            compiled = re.compile(regex_pattern, re.IGNORECASE)
            self._domain_patterns[compiled] = rules
        else:
            # Exact domain match
            self._exact_domains[domain_pattern.lower()] = rules
    
    cpdef dict get_rules_for_domain(self, str domain):
        """
        Get rules for a specific domain with caching.
        
        Args:
            domain: Domain to get rules for
        
        Returns:
            Dictionary of rules or empty dict
        """
        if not domain:
            return {}
        
        domain_lower = domain.lower()
        
        # Check cache
        if domain_lower in self._cache:
            return self._cache[domain_lower]
        
        # Check exact matches first
        if domain_lower in self._exact_domains:
            rules = self._exact_domains[domain_lower]
            self._add_to_cache(domain_lower, rules)
            return rules
        
        # Check pattern matches
        for pattern, rules in self._domain_patterns.items():
            if pattern.match(domain_lower):
                self._add_to_cache(domain_lower, rules)
                return rules
        
        # No match, cache empty result
        self._add_to_cache(domain_lower, {})
        return {}
    
    cdef void _add_to_cache(self, str key, dict value):
        """Add to cache with simple eviction."""
        if self._cache_size >= self._max_cache_size:
            # Simple eviction: clear half the cache
            keys_to_remove = list(self._cache.keys())[:self._cache_size // 2]
            for k in keys_to_remove:
                del self._cache[k]
            self._cache_size = len(self._cache)
        
        self._cache[key] = value
        self._cache_size += 1
    
    cpdef void clear_cache(self):
        """Clear the cache."""
        self._cache.clear()
        self._cache_size = 0


@cython.final
cdef class URLClassifier:
    """
    Fast URL classification using pattern matching.
    """
    
    cdef CompiledPatternMatcher _pattern_matcher
    cdef dict _classification_cache
    cdef int _cache_size
    cdef int _max_cache_size
    
    def __init__(self, int max_cache_size=5000):
        self._pattern_matcher = CompiledPatternMatcher(max_cache_size)
        self._classification_cache = {}
        self._cache_size = 0
        self._max_cache_size = max_cache_size
        self._initialize_patterns()
    
    cdef void _initialize_patterns(self):
        """Initialize default classification patterns."""
        # Navigation patterns
        self._pattern_matcher.add_pattern(
            'navigation',
            r'/(home|index|about|contact|privacy|terms|legal|sitemap|help|faq)(\.[a-z]+)?$',
            re.IGNORECASE
        )
        
        # File type patterns
        self._pattern_matcher.add_pattern(
            'document',
            r'\.(pdf|doc|docx|xls|xlsx|ppt|pptx|odt|ods|odp)$',
            re.IGNORECASE
        )
        self._pattern_matcher.add_pattern(
            'image',
            r'\.(jpg|jpeg|png|gif|bmp|svg|webp|ico)$',
            re.IGNORECASE
        )
        self._pattern_matcher.add_pattern(
            'video',
            r'\.(mp4|avi|mkv|mov|wmv|flv|webm|m4v|mpg|mpeg)$',
            re.IGNORECASE
        )
        self._pattern_matcher.add_pattern(
            'audio',
            r'\.(mp3|wav|flac|aac|ogg|wma|m4a)$',
            re.IGNORECASE
        )
        
        # Social media patterns
        self._pattern_matcher.add_pattern(
            'social_profile',
            r'/(user|profile|u|@|people)/[\w\-\.]+/?$',
            re.IGNORECASE
        )
        self._pattern_matcher.add_pattern(
            'social_post',
            r'/(status|post|posts|tweet|photo|video|watch|reel)/[\w\-]+',
            re.IGNORECASE
        )
        
        # E-commerce patterns
        self._pattern_matcher.add_pattern(
            'product',
            r'/(product|item|p|dp|gp/product)/[\w\-]+',
            re.IGNORECASE
        )
        self._pattern_matcher.add_pattern(
            'category',
            r'/(category|categories|c|browse|shop)/[\w\-/]+',
            re.IGNORECASE
        )
        self._pattern_matcher.add_pattern(
            'search',
            r'/(search|s|find|results|query)[?/]',
            re.IGNORECASE
        )
    
    cpdef str classify_url(self, str url):
        """
        Classify a URL into a category.
        
        Args:
            url: URL to classify
        
        Returns:
            Classification string or 'unknown'
        """
        # Check cache
        if url in self._classification_cache:
            return self._classification_cache[url]
        
        # Define classification priority order
        classification_order = [
            'document', 'image', 'video', 'audio',  # File types first
            'social_post', 'social_profile',        # Social media
            'product', 'category', 'search',        # E-commerce
            'navigation'                            # General navigation
        ]
        
        # Find first match
        result = self._pattern_matcher.find_first_match(url, classification_order)
        if result is None:
            result = 'unknown'
        
        # Cache result
        self._add_to_cache(url, result)
        
        return result
    
    cpdef list classify_batch(self, list urls):
        """
        Classify multiple URLs efficiently.
        
        Args:
            urls: List of URLs to classify
        
        Returns:
            List of classifications
        """
        cdef list results = []
        for url in urls:
            results.append(self.classify_url(url))
        return results
    
    cpdef void add_custom_pattern(self, str name, str pattern, int flags=0):
        """
        Add a custom classification pattern.
        
        Args:
            name: Classification name
            pattern: Regex pattern
            flags: Regex flags
        """
        self._pattern_matcher.add_pattern(name, pattern, flags)
        # Clear cache since patterns changed
        self._classification_cache.clear()
        self._cache_size = 0
    
    cdef void _add_to_cache(self, str key, str value):
        """Add to cache with simple eviction."""
        if self._cache_size >= self._max_cache_size:
            # Clear half the cache
            keys_to_remove = list(self._classification_cache.keys())[:self._cache_size // 2]
            for k in keys_to_remove:
                del self._classification_cache[k]
            self._cache_size = len(self._classification_cache)
        
        self._classification_cache[key] = value
        self._cache_size += 1
    
    cpdef void clear_cache(self):
        """Clear classification cache."""
        self._classification_cache.clear()
        self._cache_size = 0
        self._pattern_matcher.clear_cache()