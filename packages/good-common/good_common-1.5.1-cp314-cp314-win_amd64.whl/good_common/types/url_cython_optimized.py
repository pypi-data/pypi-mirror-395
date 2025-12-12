"""
Python wrapper for Cython-optimized URL operations.

This module provides a clean Python interface to the Cython-optimized
URL parsing and pattern matching functions, with graceful fallback to
pure Python implementations if Cython modules are not available.
"""

from typing import Optional, Set, Dict, List, Tuple, Any
import warnings

# Try to import Cython modules, fall back to pure Python if not available
CYTHON_AVAILABLE = False
try:
    from ._url_parser_cy import (
        FastURLComponents,
        URLCanonicalizer,
        fast_canonicalize_domain,
        fast_clean_path,
        fast_filter_query_params,
        fast_normalize_url,
        split_url_parts,
        join_url_parts,
        is_tracking_param,
    )
    from ._url_patterns_cy import (
        CompiledPatternMatcher,
        DomainRuleMatcher,
        URLClassifier,
    )

    CYTHON_AVAILABLE = True
except ImportError:
    pass  # Will define fallbacks below

if not CYTHON_AVAILABLE:
    warnings.warn(
        "Cython URL extensions not available, falling back to pure Python",
        RuntimeWarning,
        stacklevel=2,
    )

    # Import pure Python fallbacks
    from urllib.parse import urlparse, urlunparse, parse_qs, quote
    import re

    # Fallback implementations
    class FastURLComponents:  # type: ignore[no-redef]
        """Pure Python fallback for URL components."""

        def __init__(self, url: str):
            parsed = urlparse(url)
            self.scheme = parsed.scheme
            self.netloc = parsed.netloc
            self.path = parsed.path or "/"
            self.query = parsed.query
            self.fragment = parsed.fragment
            self.host = parsed.hostname or ""
            self.port = parsed.port or 0
            self._query_dict: Optional[Dict[str, List[str]]] = None

        def get_query_dict(self) -> Dict[str, List[str]]:
            if self._query_dict is None and self.query:
                self._query_dict = parse_qs(self.query, keep_blank_values=True)
            return self._query_dict or {}

        def reconstruct(self) -> str:
            return urlunparse(
                (
                    self.scheme,
                    self.netloc,
                    self.path,
                    "",  # params (deprecated)
                    self.query,
                    self.fragment,
                )
            )

    class URLCanonicalizer:  # type: ignore[no-redef]
        """Pure Python fallback for URL canonicalization."""

        def __init__(self, max_cache_size: int = 10000):
            self._cache: Dict[str, str] = {}
            self._max_cache_size = max_cache_size
            self._tracking_params: Set[str] = {
                "utm_source",
                "utm_medium",
                "utm_campaign",
                "utm_term",
                "utm_content",
                "gclid",
                "fbclid",
                "msclkid",
                "mc_eid",
                "ml_subscriber",
                "pk_campaign",
                "pk_kwd",
                "pk_source",
                "pk_medium",
                "cb",
                "_ga",
                "_ke",
                "hmb_source",
                "ref",
                "referrer",
                "source",
            }

        def canonicalize(self, url: str) -> str:
            if url in self._cache:
                return self._cache[url]

            result = fast_normalize_url(url, remove_fragment=True, remove_tracking=True)

            if len(self._cache) < self._max_cache_size:
                self._cache[url] = result

            return result

        def clear_cache(self):
            self._cache.clear()

        def set_tracking_params(self, params: Set[str]):
            self._tracking_params = params

        def set_canonical_params(self, params: Set[str]):
            self._canonical_params = params

    class CompiledPatternMatcher:  # type: ignore[no-redef]
        """Pure Python fallback for pattern matching."""

        def __init__(self, max_cache_size: int = 10000):
            self._patterns: Dict[str, Any] = {}
            self._match_cache: Dict[str, bool] = {}
            self._max_cache_size = max_cache_size

        def add_pattern(self, name: str, pattern: str, flags: int = 0):
            self._patterns[name] = re.compile(pattern, flags)

        def add_compiled_pattern(self, name: str, pattern):
            self._patterns[name] = pattern

        def matches(self, text: str, pattern_name: str) -> bool:
            cache_key = f"{pattern_name}:{text}"
            if cache_key in self._match_cache:
                return self._match_cache[cache_key]

            pattern = self._patterns.get(pattern_name)
            if pattern is None:
                return False

            result = bool(pattern.search(text))

            if len(self._match_cache) < self._max_cache_size:
                self._match_cache[cache_key] = result

            return result

        def clear_cache(self):
            self._match_cache.clear()

        def cache_size(self) -> int:
            return len(self._match_cache)

    class DomainRuleMatcher:  # type: ignore[no-redef]
        """Pure Python fallback for domain rule matching."""

        def __init__(self, max_cache_size: int = 5000):
            self._domain_patterns: Dict[Any, Dict] = {}
            self._exact_domains: Dict[str, Dict] = {}
            self._cache: Dict[str, Dict] = {}
            self._max_cache_size = max_cache_size

        def add_domain_rule(self, domain_pattern: str, rules: Dict):
            if "*" in domain_pattern or "?" in domain_pattern:
                import fnmatch

                regex_pattern = fnmatch.translate(domain_pattern)
                compiled = re.compile(regex_pattern, re.IGNORECASE)
                self._domain_patterns[compiled] = rules
            else:
                self._exact_domains[domain_pattern.lower()] = rules

        def get_rules_for_domain(self, domain: str) -> Dict:
            if not domain:
                return {}

            domain_lower = domain.lower()

            if domain_lower in self._cache:
                return self._cache[domain_lower]

            if domain_lower in self._exact_domains:
                rules = self._exact_domains[domain_lower]
            else:
                rules = {}
                for pattern, pattern_rules in self._domain_patterns.items():
                    if pattern.match(domain_lower):
                        rules = pattern_rules
                        break

            if len(self._cache) < self._max_cache_size:
                self._cache[domain_lower] = rules

            return rules

        def clear_cache(self):
            self._cache.clear()

    class URLClassifier:  # type: ignore[no-redef]
        """Pure Python fallback for URL classification."""

        def __init__(self, max_cache_size: int = 5000):
            self._pattern_matcher = CompiledPatternMatcher(max_cache_size)
            self._classification_cache: Dict[str, str] = {}
            self._max_cache_size = max_cache_size
            self._initialize_patterns()

        def _initialize_patterns(self):
            patterns = {
                "navigation": r"/(home|index|about|contact|privacy|terms)(\.[a-z]+)?$",
                "document": r"\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
                "image": r"\.(jpg|jpeg|png|gif|bmp|svg|webp)$",
                "video": r"\.(mp4|avi|mkv|mov|wmv|webm)$",
                "audio": r"\.(mp3|wav|flac|aac|ogg|m4a)$",
                "social_profile": r"/(user|profile|u|@)/[\w\-\.]+/?$",
                "social_post": r"/(status|post|tweet|photo|video|reel)/[\w\-]+",
                "product": r"/(product|item|p|dp)/[\w\-]+",
                "category": r"/(category|c|browse|shop)/[\w\-/]+",
                "search": r"/(search|s|find|results)[?/]",
            }
            for name, pattern in patterns.items():
                self._pattern_matcher.add_pattern(name, pattern, re.IGNORECASE)

        def classify_url(self, url: str) -> str:
            if url in self._classification_cache:
                return self._classification_cache[url]

            classification_order = [
                "document",
                "image",
                "video",
                "audio",
                "social_post",
                "social_profile",
                "product",
                "category",
                "search",
                "navigation",
            ]

            for pattern_name in classification_order:
                if self._pattern_matcher.matches(url, pattern_name):
                    result = pattern_name
                    break
            else:
                result = "unknown"

            if len(self._classification_cache) < self._max_cache_size:
                self._classification_cache[url] = result

            return result

        def add_custom_pattern(self, name: str, pattern: str, flags: int = 0):
            self._pattern_matcher.add_pattern(name, pattern, flags)
            self._classification_cache.clear()

        def clear_cache(self):
            self._classification_cache.clear()
            self._pattern_matcher.clear_cache()

    # Fallback functions
    def fast_canonicalize_domain(domain: str) -> str:
        if not domain:
            return domain
        domain = domain.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain

    def fast_clean_path(path: str) -> str:
        if not path:
            return "/"
        while "//" in path:
            path = path.replace("//", "/")
        if len(path) > 1 and path.endswith("/"):
            path = path[:-1]
        return path

    def fast_filter_query_params(
        query: str,
        keep_params: Optional[Set[str]] = None,
        remove_params: Optional[Set[str]] = None,
    ) -> str:
        if not query:
            return ""

        params = parse_qs(query, keep_blank_values=True)
        filtered = {}

        tracking_pattern = re.compile(
            r"^(utm_|ga_|gclid|fbclid|msclkid|mc_|ml_|pk_|cb|_ga|_ke|hmb_|ref|referrer|source|campaign)"
        )

        for key, values in params.items():
            if remove_params and key in remove_params:
                continue
            if not keep_params and tracking_pattern.match(key):
                continue
            if keep_params is None or key in keep_params:
                filtered[key] = values

        if not filtered:
            return ""

        sorted_params = []
        for key in sorted(filtered.keys()):
            for value in filtered[key]:
                if value:
                    sorted_params.append(f"{key}={quote(value, safe='')}")
                else:
                    sorted_params.append(key)

        return "&".join(sorted_params)

    def fast_normalize_url(
        url: str, remove_fragment: bool = True, remove_tracking: bool = True
    ) -> str:
        if not url:
            return url

        components = FastURLComponents(url)

        if components.host:
            components.host = fast_canonicalize_domain(components.host)
            if components.port:
                components.netloc = f"{components.host}:{components.port}"
            else:
                components.netloc = components.host

        if components.path:
            components.path = fast_clean_path(components.path)

        if components.query and remove_tracking:
            components.query = fast_filter_query_params(components.query)

        if remove_fragment:
            components.fragment = ""

        return components.reconstruct()

    def split_url_parts(url: str) -> Tuple[str, str, str, str, str]:
        components = FastURLComponents(url)
        return (
            components.scheme,
            components.host,
            components.path,
            components.query,
            components.fragment,
        )

    def join_url_parts(
        scheme: str, host: str, path: str = "", query: str = "", fragment: str = ""
    ) -> str:
        parts = []
        if scheme:
            parts.append(f"{scheme}://")
        if host:
            parts.append(host)
        if path:
            if not path.startswith("/"):
                parts.append("/")
            parts.append(path)
        elif host:
            parts.append("/")
        if query:
            parts.append(f"?{query}")
        if fragment:
            parts.append(f"#{fragment}")
        return "".join(parts)

    def is_tracking_param(param_name: str) -> bool:
        tracking_pattern = re.compile(
            r"^(utm_|ga_|gclid|fbclid|msclkid|mc_|ml_|pk_|cb|_ga|_ke|hmb_|ref|referrer|source|campaign)"
        )
        return bool(tracking_pattern.match(param_name))


# Public API
__all__ = [
    "CYTHON_AVAILABLE",
    "FastURLComponents",
    "URLCanonicalizer",
    "CompiledPatternMatcher",
    "DomainRuleMatcher",
    "URLClassifier",
    "fast_canonicalize_domain",
    "fast_clean_path",
    "fast_filter_query_params",
    "fast_normalize_url",
    "split_url_parts",
    "join_url_parts",
    "is_tracking_param",
    "create_optimized_url_instance",
]


def create_optimized_url_instance(
    url: str, use_cython: Optional[bool] = None
) -> "OptimizedURL":
    """
    Create an optimized URL instance.

    Args:
        url: URL string to parse
        use_cython: Force use of Cython (True) or pure Python (False).
                   If None, uses Cython if available.

    Returns:
        OptimizedURL instance
    """
    if use_cython is None:
        use_cython = CYTHON_AVAILABLE

    if use_cython and not CYTHON_AVAILABLE:
        warnings.warn("Cython requested but not available, using pure Python")
        use_cython = False

    return OptimizedURL(url, use_cython=use_cython)


class OptimizedURL:
    """
    High-performance URL class using Cython optimizations when available.

    This class provides a clean interface to Cython-optimized URL operations
    with automatic fallback to pure Python implementations.
    """

    # Class-level shared instances for better performance
    _canonicalizer: Optional[URLCanonicalizer] = None
    _classifier: Optional[URLClassifier] = None
    _domain_matcher: Optional[DomainRuleMatcher] = None

    def __init__(self, url: str, use_cython: bool = True):
        """
        Initialize optimized URL instance.

        Args:
            url: URL string
            use_cython: Whether to use Cython optimizations
        """
        self._url = url
        self._use_cython = use_cython and CYTHON_AVAILABLE
        self._components: Optional[FastURLComponents] = None
        self._canonical: Optional[str] = None

        # Initialize shared instances if needed
        if OptimizedURL._canonicalizer is None:
            OptimizedURL._canonicalizer = URLCanonicalizer()
            OptimizedURL._classifier = URLClassifier()
            OptimizedURL._domain_matcher = DomainRuleMatcher()

    @property
    def components(self) -> FastURLComponents:
        """Get parsed URL components (cached)."""
        if self._components is None:
            self._components = FastURLComponents(self._url)
        return self._components

    @property
    def scheme(self) -> str:
        return self.components.scheme

    @property
    def host(self) -> str:
        return self.components.host

    @property
    def path(self) -> str:
        return self.components.path

    @property
    def query(self) -> str:
        return self.components.query

    @property
    def fragment(self) -> str:
        return self.components.fragment

    @property
    def port(self) -> int:
        return self.components.port

    def canonicalize(
        self, remove_fragment: bool = True, remove_tracking: bool = True
    ) -> str:
        """
        Get canonicalized URL.

        Args:
            remove_fragment: Remove URL fragment
            remove_tracking: Remove tracking parameters

        Returns:
            Canonicalized URL string
        """
        if self._canonical is None:
            if remove_fragment and remove_tracking and self._canonicalizer:
                # Use cached canonicalizer for common case
                self._canonical = self._canonicalizer.canonicalize(self._url)
            else:
                # Custom normalization
                self._canonical = fast_normalize_url(
                    self._url,
                    remove_fragment=remove_fragment,
                    remove_tracking=remove_tracking,
                )
        return self._canonical

    def classify(self) -> str:
        """
        Classify the URL type.

        Returns:
            Classification string (e.g., 'document', 'image', 'navigation')
        """
        if self._classifier:
            return self._classifier.classify_url(self._url)
        return "unknown"

    def get_domain_rules(self) -> Dict:
        """
        Get domain-specific rules for this URL.

        Returns:
            Dictionary of domain rules
        """
        if self._domain_matcher:
            return self._domain_matcher.get_rules_for_domain(self.host)
        return {}

    def is_tracking_param(self, param_name: str) -> bool:
        """
        Check if a parameter name is a tracking parameter.

        Args:
            param_name: Parameter name to check

        Returns:
            True if tracking parameter
        """
        return is_tracking_param(param_name)

    def filter_query_params(
        self,
        keep_params: Optional[Set[str]] = None,
        remove_params: Optional[Set[str]] = None,
    ) -> str:
        """
        Filter query parameters.

        Args:
            keep_params: Set of parameters to keep
            remove_params: Set of parameters to remove

        Returns:
            Filtered query string
        """
        return fast_filter_query_params(self.query, keep_params, remove_params)

    def __str__(self) -> str:
        return self._url

    def __repr__(self) -> str:
        return f"OptimizedURL('{self._url}', cython={self._use_cython})"

    @classmethod
    def clear_caches(cls):
        """Clear all class-level caches."""
        if cls._canonicalizer:
            cls._canonicalizer.clear_cache()
        if cls._classifier:
            cls._classifier.clear_cache()
        if cls._domain_matcher:
            cls._domain_matcher.clear_cache()
