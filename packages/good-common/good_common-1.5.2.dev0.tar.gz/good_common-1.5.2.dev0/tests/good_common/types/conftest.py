"""Shared fixtures for types tests."""
import pytest
from good_common.types.url_plugins import url_plugin_registry


@pytest.fixture(autouse=True)
def clean_plugin_registry():
    """Ensure clean plugin registry state between tests."""
    # Store original plugins
    original_plugins = url_plugin_registry.plugins.copy()
    
    # Clear registry for clean state  
    url_plugin_registry.clear()
    
    # Yield for test execution
    yield
    
    # Restore original state
    url_plugin_registry.clear()
    for plugin in original_plugins:
        url_plugin_registry.register(plugin)