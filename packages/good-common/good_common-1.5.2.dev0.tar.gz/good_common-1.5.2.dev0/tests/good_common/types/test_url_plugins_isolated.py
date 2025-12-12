"""Isolated tests for URL plugin system to ensure no cross-contamination."""

from typing import Any, Dict, Set

import pytest

from good_common.types.url_plugins import (
    URLPlugin,
    url_plugin_registry,
)
from good_common.types.web import URL


@pytest.fixture(autouse=True)
def clean_registry():
    """Ensure clean registry for each test."""
    # Store original state
    original_plugins = url_plugin_registry.plugins.copy()
    
    # Clear registry and all caches
    url_plugin_registry.plugins.clear()
    url_plugin_registry._invalidate_caches()
    
    # Ensure URL class registry is synchronized
    from good_common.types.web import URL
    URL._plugin_registry = url_plugin_registry
    
    yield
    
    # Restore original state
    url_plugin_registry.plugins = original_plugins
    url_plugin_registry._invalidate_caches()
    
    # Ensure URL class registry is synchronized
    URL._plugin_registry = url_plugin_registry


class SimpleTestPlugin(URLPlugin):
    """Simple test plugin for isolated testing."""
    
    def get_tracking_params(self) -> Set[str]:
        return {"test_tracker"}
    
    def get_canonical_params(self) -> Set[str]:
        return {"test_id"}


def test_plugin_canonicalization():
    """Test that plugin tracking params are removed."""
    plugin = SimpleTestPlugin()
    URL.register_plugin(plugin)
    
    # Test tracking param removal
    url = URL("https://example.com/page?test_tracker=123&keep=yes")
    canonical = url.canonicalize()
    
    assert "test_tracker" not in canonical.query, f"test_tracker should be removed, got: {canonical.query}"
    assert "keep" in canonical.query, f"keep should be preserved, got: {canonical.query}"
    
    # Test canonical param preservation
    url = URL("https://example.com/page?test_id=456&remove=no")
    canonical = url.canonicalize()
    
    assert "test_id" in canonical.query, f"test_id should be preserved, got: {canonical.query}"


def test_plugin_domain_rules():
    """Test domain-specific rules from plugin."""
    
    class DomainPlugin(URLPlugin):
        def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
            return {
                r"(.*\.)?testsite\.com": {
                    "canonical": {"keep_me"},
                    "non_canonical": {"remove_me"},
                    "force_www": True,
                }
            }
    
    plugin = DomainPlugin()
    URL.register_plugin(plugin)
    
    url = URL("https://testsite.com/page?keep_me=1&remove_me=2")
    canonical = url.canonicalize()
    
    assert canonical.host == "www.testsite.com", f"Should add www, got: {canonical.host}"
    assert "keep_me" in canonical.query, f"keep_me should be preserved, got: {canonical.query}"
    assert "remove_me" not in canonical.query, f"remove_me should be removed, got: {canonical.query}"


def test_multiple_plugins():
    """Test that multiple plugins work together."""
    
    class Plugin1(URLPlugin):
        def get_tracking_params(self) -> Set[str]:
            return {"tracker1"}
    
    class Plugin2(URLPlugin):
        def get_tracking_params(self) -> Set[str]:
            return {"tracker2"}
    
    URL.register_plugin(Plugin1())
    URL.register_plugin(Plugin2())
    
    url = URL("https://example.com?tracker1=a&tracker2=b&keep=c")
    canonical = url.canonicalize()
    
    assert "tracker1" not in canonical.query, f"tracker1 should be removed, got: {canonical.query}"
    assert "tracker2" not in canonical.query, f"tracker2 should be removed, got: {canonical.query}"
    assert "keep" in canonical.query, f"keep should be preserved, got: {canonical.query}"


def test_plugin_isolation():
    """Test that plugins don't affect each other across tests."""
    # This test should have a clean registry due to the fixture
    assert len(url_plugin_registry.plugins) == 0, "Registry should be empty"
    
    # Add a plugin
    plugin = SimpleTestPlugin()
    URL.register_plugin(plugin)
    assert len(url_plugin_registry.plugins) == 1, "Should have 1 plugin"
    
    # Plugin should work
    url = URL("https://example.com?test_tracker=remove")
    canonical = url.canonicalize()
    assert "test_tracker" not in canonical.query, "Plugin should be active"


def test_registry_state_after_tests():
    """Verify registry is clean after previous tests."""
    # Due to fixture, this should always start clean
    assert len(url_plugin_registry.plugins) == 0, f"Registry should be empty, has {len(url_plugin_registry.plugins)} plugins"