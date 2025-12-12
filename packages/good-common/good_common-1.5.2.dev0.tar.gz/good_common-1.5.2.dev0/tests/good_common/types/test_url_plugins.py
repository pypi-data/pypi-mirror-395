"""Tests for URL plugin system."""

import re
from typing import Any, Dict, Optional, Pattern, Set


from good_common.types.url_plugins import (
    URLPlugin,
    URLPluginRegistry,
    url_plugin_registry,
)
from good_common.types.web import URL, UrlParseConfig


class TestURLPlugin(URLPlugin):
    """Test plugin implementation."""
    
    def get_tracking_params(self) -> Set[str]:
        return {"test_tracker", "test_campaign"}
    
    def get_canonical_params(self) -> Set[str]:
        return {"test_id", "test_version"}
    
    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        return {
            r"(.*\.)?testdomain\.com": {
                "canonical": {"test_param"},
                "non_canonical": {"test_remove"},
                "force_www": True,
            }
        }
    
    def get_short_url_providers(self) -> Set[str]:
        return {"test.ly", "tst.co"}
    
    def get_html_redirect_domains(self) -> Set[str]:
        return {"test.redirect"}
    
    def get_classification_patterns(self) -> Dict[str, Pattern]:
        return {
            "test_pattern": re.compile(r"/test/.*"),
        }
    
    def transform_url(self, url: URL, config: UrlParseConfig) -> Optional[URL]:
        if "test.transform" in url.host:
            return URL.build(
                scheme="https",
                host="transformed.com",
                path=url.path,
            )
        return None


class TestURLPluginRegistry:
    """Test URLPluginRegistry functionality."""
    
    def test_register_plugin(self):
        """Test plugin registration."""
        registry = URLPluginRegistry()
        plugin = TestURLPlugin()
        
        registry.register(plugin)
        assert plugin in registry.plugins
    
    def test_unregister_plugin(self):
        """Test plugin unregistration."""
        registry = URLPluginRegistry()
        plugin = TestURLPlugin()
        
        registry.register(plugin)
        assert plugin in registry.plugins
        
        registry.unregister(plugin)
        assert plugin not in registry.plugins
    
    def test_cache_invalidation(self):
        """Test that caches are invalidated on plugin changes."""
        registry = URLPluginRegistry()
        plugin = TestURLPlugin()
        
        # Access cached properties
        _ = registry.get_short_url_providers()
        assert registry._short_url_providers_cache is not None
        
        # Register plugin should invalidate cache
        registry.register(plugin)
        assert registry._short_url_providers_cache is None
        
        # Access again to populate cache
        providers = registry.get_short_url_providers()
        assert "test.ly" in providers
        assert registry._short_url_providers_cache is not None
        
        # Unregister should invalidate cache
        registry.unregister(plugin)
        assert registry._short_url_providers_cache is None
    
    def test_get_tracking_params(self):
        """Test getting tracking parameters from plugins."""
        registry = URLPluginRegistry()
        plugin = TestURLPlugin()
        
        # Initially empty
        params = registry.get_tracking_params()
        assert len(params) == 0
        
        # After registration
        registry.register(plugin)
        params = registry.get_tracking_params()
        assert "test_tracker" in params
        assert "test_campaign" in params
    
    def test_get_canonical_params(self):
        """Test getting canonical parameters from plugins."""
        registry = URLPluginRegistry()
        plugin = TestURLPlugin()
        
        registry.register(plugin)
        params = registry.get_canonical_params()
        assert "test_id" in params
        assert "test_version" in params
    
    def test_get_domain_rules(self):
        """Test getting domain rules from plugins."""
        registry = URLPluginRegistry()
        plugin = TestURLPlugin()
        
        registry.register(plugin)
        rules = registry.get_domain_rules()
        
        assert r"(.*\.)?testdomain\.com" in rules
        domain_rule = rules[r"(.*\.)?testdomain\.com"]
        assert "test_param" in domain_rule["canonical"]
        assert "test_remove" in domain_rule["non_canonical"]
        assert domain_rule["force_www"] is True
    
    def test_get_short_url_providers(self):
        """Test getting short URL providers from plugins."""
        registry = URLPluginRegistry()
        plugin = TestURLPlugin()
        
        registry.register(plugin)
        providers = registry.get_short_url_providers()
        assert "test.ly" in providers
        assert "tst.co" in providers
    
    def test_get_classification_patterns(self):
        """Test getting classification patterns from plugins."""
        registry = URLPluginRegistry()
        plugin = TestURLPlugin()
        
        registry.register(plugin)
        patterns = registry.get_classification_patterns()
        assert "test_pattern" in patterns
        assert patterns["test_pattern"].pattern == r"/test/.*"
    
    def test_apply_transformations(self):
        """Test applying URL transformations from plugins."""
        registry = URLPluginRegistry()
        plugin = TestURLPlugin()
        config = UrlParseConfig()
        
        registry.register(plugin)
        
        # URL that should be transformed
        url = URL("https://test.transform/path")
        transformed = registry.apply_transformations(url, config)
        assert transformed.host == "transformed.com"
        
        # URL that should not be transformed
        url = URL("https://example.com/path")
        transformed = registry.apply_transformations(url, config)
        assert transformed.host == "example.com"


class TestURLIntegration:
    """Test URL class integration with plugins."""
    
    def setup_method(self):
        """Clear registry before each test."""
        # Store original state
        self._original_plugins = url_plugin_registry.plugins.copy()
        # Clear any existing plugins
        url_plugin_registry.plugins.clear()
        url_plugin_registry._invalidate_caches()
        
        # Ensure URL class registry is synchronized
        from good_common.types.web import URL
        URL._plugin_registry = url_plugin_registry
    
    def teardown_method(self):
        """Clean up after each test."""
        # Restore original state
        url_plugin_registry.plugins = self._original_plugins
        url_plugin_registry._invalidate_caches()
        
        # Ensure URL class registry is synchronized
        from good_common.types.web import URL
        URL._plugin_registry = url_plugin_registry
    
    def test_url_register_plugin(self):
        """Test registering plugin via URL class."""
        plugin = TestURLPlugin()
        URL.register_plugin(plugin)
        
        assert plugin in URL._plugin_registry.plugins
    
    def test_url_with_plugin_short_urls(self):
        """Test URL short URL detection with plugins."""
        plugin = TestURLPlugin()
        URL.register_plugin(plugin)
        
        # Test plugin-provided short URL
        url = URL("https://test.ly/abc123")
        assert url.is_short_url is True
        
        # Test built-in short URL still works
        url = URL("https://bit.ly/xyz789")
        assert url.is_short_url is True
        
        # Test non-short URL
        url = URL("https://example.com/page")
        assert url.is_short_url is False
    
    def test_url_with_plugin_canonicalization(self):
        """Test URL canonicalization with plugin parameters."""
        plugin = TestURLPlugin()
        URL.register_plugin(plugin)
        
        # Test that plugin tracking params are removed
        url = URL("https://example.com/page?test_tracker=123&keep=yes")
        canonical = url.canonicalize()
        assert "test_tracker" not in canonical.query, f"test_tracker should be removed, but query is: {canonical.query}"
        assert "keep" in canonical.query, f"keep should be preserved, but query is: {canonical.query}"
        
        # Test that plugin canonical params are preserved
        url = URL("https://example.com/page?test_id=456&remove=no")
        canonical = url.canonicalize()
        assert "test_id" in canonical.query, f"test_id should be preserved, but query is: {canonical.query}"
    
    def test_url_classify_with_plugins(self):
        """Test URL classification with plugin patterns."""
        plugin = TestURLPlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://example.com/test/page")
        classification = url.classify()
        
        # Check built-in classifications
        assert "is_short_url" in classification
        assert "is_adult" in classification
        
        # Check plugin classification
        assert "test_pattern" in classification
        assert classification["test_pattern"] is True
        
        # Test URL that doesn't match plugin pattern
        url = URL("https://example.com/other/page")
        classification = url.classify()
        assert classification["test_pattern"] is False
    
    def test_url_with_plugin_domain_rules(self):
        """Test URL with plugin-provided domain rules."""
        plugin = TestURLPlugin()
        URL.register_plugin(plugin)
        
        # Test domain-specific canonicalization
        url = URL("https://sub.testdomain.com/page?test_param=keep&test_remove=drop")
        canonical = url.canonicalize()
        
        # Should have www added (force_www)
        assert canonical.host.startswith("www."), f"Host should start with www., but is: {canonical.host}"
        
        # Should keep canonical param
        assert "test_param" in canonical.query, f"test_param should be preserved, but query is: {canonical.query}"
        
        # Should remove non-canonical param
        assert "test_remove" not in canonical.query, f"test_remove should be removed, but query is: {canonical.query}"
    
    def test_multiple_plugins(self):
        """Test multiple plugins working together."""
        plugin1 = TestURLPlugin()
        
        class SecondPlugin(URLPlugin):
            def get_tracking_params(self) -> Set[str]:
                return {"second_tracker"}
            
            def get_short_url_providers(self) -> Set[str]:
                return {"second.ly"}
        
        plugin2 = SecondPlugin()
        
        URL.register_plugin(plugin1)
        URL.register_plugin(plugin2)
        
        # Both plugins' tracking params should be filtered
        url = URL("https://example.com?test_tracker=1&second_tracker=2&keep=yes")
        canonical = url.canonicalize()
        assert "test_tracker" not in canonical.query, f"test_tracker should be removed, but query is: {canonical.query}"
        assert "second_tracker" not in canonical.query, f"second_tracker should be removed, but query is: {canonical.query}"
        assert "keep" in canonical.query, f"keep should be preserved, but query is: {canonical.query}"
        
        # Both plugins' short URLs should be recognized
        assert URL("https://test.ly/abc").is_short_url, "test.ly should be recognized as short URL"
        assert URL("https://second.ly/xyz").is_short_url, "second.ly should be recognized as short URL"