"""
Integration layer between URL plugin system and Cython optimizations.

This module bridges the plugin system with Cython-optimized operations,
ensuring that plugin-registered rules benefit from the performance improvements.
"""

from typing import Any, Dict, Optional, Set

from loguru import logger

from .url_cython_optimized import (
    CYTHON_AVAILABLE,
    CompiledPatternMatcher,
    DomainRuleMatcher,
    URLCanonicalizer,
    URLClassifier,
    fast_filter_query_params,
)
from .url_plugins import URLPluginRegistry


class CythonOptimizedPluginRegistry:
    """
    Enhanced plugin registry that leverages Cython optimizations.

    This class wraps the standard URLPluginRegistry and integrates it with
    Cython-optimized components for maximum performance.
    """

    def __init__(self, base_registry: Optional[URLPluginRegistry] = None):
        """
        Initialize the optimized registry.

        Args:
            base_registry: Existing plugin registry to wrap
        """
        self.base_registry = base_registry or URLPluginRegistry()

        # Initialize Cython-optimized components
        self.canonicalizer = URLCanonicalizer() if CYTHON_AVAILABLE else None
        self.domain_matcher = DomainRuleMatcher() if CYTHON_AVAILABLE else None
        self.pattern_matcher = CompiledPatternMatcher() if CYTHON_AVAILABLE else None
        self.classifier = URLClassifier() if CYTHON_AVAILABLE else None

        # Sync initial state
        self._sync_with_plugins()

        logger.debug(
            f"CythonOptimizedPluginRegistry initialized "
            f"(Cython {'enabled' if CYTHON_AVAILABLE else 'disabled'})"
        )

    def register_plugin(self, plugin):
        """
        Register a plugin and update Cython components.

        This method ensures that plugin rules are integrated into
        the Cython-optimized components for maximum performance.
        """
        # Register with base registry
        self.base_registry.register(plugin)

        # Update Cython components with new plugin data
        self._sync_with_plugins()

        logger.debug("Plugin registered and synced with Cython optimizations")

    def _sync_with_plugins(self):
        """
        Synchronize Cython components with current plugin configuration.

        This method updates all Cython-optimized components with the latest
        tracking parameters, domain rules, and patterns from registered plugins.
        """
        if not CYTHON_AVAILABLE:
            return

        # Collect all tracking parameters from plugins
        all_tracking_params = set()
        all_canonical_params = set()

        for plugin in self.base_registry.plugins:
            all_tracking_params.update(plugin.get_tracking_params())
            all_canonical_params.update(plugin.get_canonical_params())

        # Update canonicalizer with tracking parameters
        if self.canonicalizer:
            # Combine with default tracking params
            default_tracking = {
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
            all_tracking_params.update(default_tracking)
            self.canonicalizer.set_tracking_params(all_tracking_params)
            self.canonicalizer.set_canonical_params(all_canonical_params)

        # Update domain matcher with plugin domain rules
        if self.domain_matcher:
            for plugin in self.base_registry.plugins:
                domain_rules = plugin.get_domain_rules()
                for domain_pattern, rules in domain_rules.items():
                    self.domain_matcher.add_domain_rule(domain_pattern, rules)

        # Update pattern matcher with classification patterns
        if self.pattern_matcher:
            classification_patterns = self.base_registry.get_classification_patterns()
            for name, pattern in classification_patterns.items():
                self.pattern_matcher.add_compiled_pattern(name, pattern)

        logger.debug(
            f"Synced Cython components: "
            f"{len(all_tracking_params)} tracking params, "
            f"{len(all_canonical_params)} canonical params"
        )

    def canonicalize_with_plugins(self, url: str) -> str:
        """
        Canonicalize URL using Cython optimizations and plugin rules.

        Args:
            url: URL to canonicalize

        Returns:
            Canonicalized URL string
        """
        if self.canonicalizer and CYTHON_AVAILABLE:
            # First sync tracking params with plugins
            all_tracking_params = set()
            for plugin in self.base_registry.plugins:
                all_tracking_params.update(plugin.get_tracking_params())

            # Add default tracking params
            default_tracking = {
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
            all_tracking_params.update(default_tracking)

            # Update canonicalizer with all tracking params
            self.canonicalizer.set_tracking_params(all_tracking_params)

            # Use Cython-optimized canonicalization
            result = self.canonicalizer.canonicalize(url)

            # Apply plugin transformations (if any)
            for plugin in self.base_registry.plugins:
                if hasattr(plugin, "transform_url"):
                    from .web import URL, UrlParseConfig

                    url_obj = URL(result)
                    config = UrlParseConfig()
                    transformed = plugin.transform_url(url_obj, config)
                    if transformed:
                        result = str(transformed)

            return result
        else:
            # Fallback to standard canonicalization
            from .web import URL

            return str(URL(url).canonicalize())

    def filter_query_params_with_plugins(
        self, query: str, keep_params: Optional[Set[str]] = None
    ) -> str:
        """
        Filter query parameters using Cython optimizations and plugin rules.

        Args:
            query: Query string to filter
            keep_params: Optional set of parameters to keep

        Returns:
            Filtered query string
        """
        # Convert dict to string if needed (for compatibility)
        if isinstance(query, dict):
            from urllib.parse import urlencode

            query = urlencode(query, doseq=True)

        # Collect tracking params to remove from plugins
        remove_params = set()
        for plugin in self.base_registry.plugins:
            remove_params.update(plugin.get_tracking_params())

        # Note: canonical params from plugins should be preserved,
        # but we shouldn't restrict to ONLY canonical params
        # (that would remove all non-canonical params)

        # Use Cython-optimized filtering
        # Only pass keep_params if explicitly provided
        return fast_filter_query_params(
            query,
            keep_params=keep_params,  # None means keep all non-tracking
            remove_params=remove_params,
        )

    def get_domain_rules_optimized(self, domain: str) -> Dict[str, Any]:
        """
        Get domain rules using Cython-optimized matching.

        Args:
            domain: Domain to get rules for

        Returns:
            Dictionary of domain-specific rules
        """
        if self.domain_matcher and CYTHON_AVAILABLE:
            return self.domain_matcher.get_rules_for_domain(domain)
        else:
            # Fallback to standard matching - get all rules and filter by domain
            all_rules = self.base_registry.get_domain_rules()
            return all_rules.get(domain, {})

    def classify_url_optimized(self, url: str) -> str:
        """
        Classify URL using Cython-optimized pattern matching.

        Args:
            url: URL to classify

        Returns:
            Classification string
        """
        if self.classifier and CYTHON_AVAILABLE:
            # First try built-in classifications
            result = self.classifier.classify_url(url)

            # If unknown, check plugin patterns
            if result == "unknown":
                patterns = self.base_registry.get_classification_patterns()
                for name, pattern in patterns.items():
                    if pattern.search(url):
                        return name

            return result
        else:
            # Fallback to standard classification
            from .web import URL

            url_obj = URL(url)
            classifications = url_obj.classify()
            # Return first true classification
            for name, is_match in classifications.items():
                if is_match:
                    return name
            return "unknown"

    def clear_caches(self):
        """Clear all Cython component caches."""
        if CYTHON_AVAILABLE:
            if self.canonicalizer:
                self.canonicalizer.clear_cache()
            if self.domain_matcher:
                self.domain_matcher.clear_cache()
            if self.pattern_matcher:
                self.pattern_matcher.clear_cache()
            if self.classifier:
                self.classifier.clear_cache()

        logger.debug("Cleared all Cython component caches")

    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics from Cython components.

        Returns:
            Dictionary with cache sizes and hit rates
        """
        stats = {
            "cython_available": CYTHON_AVAILABLE,
            "plugin_count": len(self.base_registry.plugins),
        }

        if CYTHON_AVAILABLE:
            if self.pattern_matcher:
                stats["pattern_cache_size"] = self.pattern_matcher.cache_size()

            # Add more stats as needed

        return stats


# Global optimized registry instance
_optimized_registry = None
_optimization_enabled = False


def get_optimized_registry() -> CythonOptimizedPluginRegistry:
    """
    Get or create the global optimized plugin registry.

    Returns:
        CythonOptimizedPluginRegistry instance
    """
    global _optimized_registry
    if _optimized_registry is None:
        from .url_plugins import url_plugin_registry

        _optimized_registry = CythonOptimizedPluginRegistry(url_plugin_registry)
    return _optimized_registry


def is_optimization_enabled() -> bool:
    """Check if Cython optimization is enabled."""
    global _optimization_enabled
    return _optimization_enabled


def enable_cython_plugin_optimization():
    """
    Enable Cython optimizations for the URL plugin system.

    This function marks that Cython is available and ready for use.
    The actual optimization happens on-demand when URL operations are performed.
    """
    global _optimization_enabled

    if not CYTHON_AVAILABLE:
        logger.warning("Cython extensions not available, optimization not enabled")
        return False

    if _optimization_enabled:
        logger.debug("Cython optimization already enabled")
        return True

    # Mark as enabled - actual optimization happens on-demand
    _optimization_enabled = True
    return True


def auto_enable_optimization():
    """
    Automatically enable Cython optimization based on availability and environment.

    This function checks:
    1. If Cython extensions are available
    2. If DISABLE_URL_CYTHON_OPTIMIZATION env var is NOT set
    3. If FORCE_URL_CYTHON_OPTIMIZATION env var IS set (forces even if risky)

    Returns:
        bool: True if optimization was enabled, False otherwise
    """
    import os

    # Check if explicitly disabled
    if os.environ.get("DISABLE_URL_CYTHON_OPTIMIZATION", "").lower() in (
        "true",
        "1",
        "yes",
    ):
        logger.debug("URL Cython optimization disabled by environment variable")
        return False

    # Check if forced
    force = os.environ.get("FORCE_URL_CYTHON_OPTIMIZATION", "").lower() in (
        "true",
        "1",
        "yes",
    )

    if not CYTHON_AVAILABLE and not force:
        logger.debug("Cython extensions not available, optimization not auto-enabled")
        return False

    # Try to enable
    try:
        result = enable_cython_plugin_optimization()

        return result
    except Exception as e:
        logger.warning(f"Failed to auto-enable Cython optimization: {e}")
        return False


def _auto_enable_on_import() -> None:
    """Enable optimization automatically when requested via environment variable."""
    import os

    if os.environ.get("ENABLE_URL_CYTHON_OPTIMIZATION", "").lower() in (
        "true",
        "1",
        "yes",
    ):
        auto_enable_optimization()


_auto_enable_on_import()


# Example usage demonstrating the performance benefits
if __name__ == "__main__":
    import time

    from .url_plugins import URLPlugin

    # Create a sample plugin
    class PerformanceTestPlugin(URLPlugin):
        def get_tracking_params(self) -> Set[str]:
            return {"test_param1", "test_param2", "test_param3"}

        def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
            return {
                "*.testdomain.com": {"canonical": ["id", "page"], "force_https": True}
            }

    # Register plugin
    registry = get_optimized_registry()
    registry.register_plugin(PerformanceTestPlugin())

    # Test URLs
    test_urls = [
        "https://www.testdomain.com/page?test_param1=abc&id=123&page=2",
        "http://sub.testdomain.com/resource?test_param2=xyz&keep=this",
    ] * 100

    # Benchmark
    start = time.perf_counter()
    for url in test_urls:
        result = registry.canonicalize_with_plugins(url)
    elapsed = time.perf_counter() - start

    print(f"Processed {len(test_urls)} URLs in {elapsed:.3f}s")
    print(f"Average: {(elapsed / len(test_urls)) * 1000:.3f}ms per URL")

    # Show stats
    stats = registry.get_performance_stats()
    print(f"Performance stats: {stats}")
