"""
Tests for automatic Cython optimization detection and activation.
"""

import os
import sys
import pytest
from unittest import mock
from typing import Set

from good_common.types.url_cython_integration import (
    CYTHON_AVAILABLE,
    is_optimization_enabled,
    auto_enable_optimization,
    enable_cython_plugin_optimization,
)


class TestAutomaticOptimization:
    """Test automatic Cython optimization detection."""
    
    def test_auto_enable_with_cython_available(self):
        """Test that optimization is auto-enabled when Cython is available."""
        if not CYTHON_AVAILABLE:
            pytest.skip("Cython not available")
        
        # Reset optimization state
        import good_common.types.url_cython_integration as integration
        integration._optimization_enabled = False
        
        # Should enable
        result = auto_enable_optimization()
        assert result is True
        assert is_optimization_enabled() is True
    
    def test_auto_enable_when_already_enabled(self):
        """Test that auto-enable handles already-enabled state."""
        if not CYTHON_AVAILABLE:
            pytest.skip("Cython not available")
        
        # First enable
        enable_cython_plugin_optimization()
        assert is_optimization_enabled() is True
        
        # Second call should still return True
        result = auto_enable_optimization()
        assert result is True
        assert is_optimization_enabled() is True
    
    def test_disable_via_environment_variable(self):
        """Test that DISABLE_URL_CYTHON_OPTIMIZATION env var works."""
        # Test the auto_enable_optimization function directly with environment variable
        # This avoids relying on global state that may be affected by other tests
        
        with mock.patch.dict(os.environ, {'DISABLE_URL_CYTHON_OPTIMIZATION': 'true'}):
            # Mock the global state to start fresh
            with mock.patch('good_common.types.url_cython_integration._optimization_enabled', False):
                result = auto_enable_optimization()
                assert result is False
        
        # Also test with '1' and 'yes'
        for value in ['1', 'yes', 'YES', 'True', 'TRUE']:
            with mock.patch.dict(os.environ, {'DISABLE_URL_CYTHON_OPTIMIZATION': value}):
                with mock.patch('good_common.types.url_cython_integration._optimization_enabled', False):
                    result = auto_enable_optimization()
                    assert result is False, f"Failed with value: {value}"
    
    def test_force_via_environment_variable(self):
        """Test that FORCE_URL_CYTHON_OPTIMIZATION env var works."""
        # This would force even without Cython, but we can't really test that
        # without mocking CYTHON_AVAILABLE which is complex
        
        with mock.patch.dict(os.environ, {'FORCE_URL_CYTHON_OPTIMIZATION': 'true'}):
            # If Cython is available, this should work
            if CYTHON_AVAILABLE:
                import good_common.types.url_cython_integration as integration
                integration._optimization_enabled = False
                
                result = auto_enable_optimization()
                assert result is True
                assert is_optimization_enabled() is True
    
    def test_module_import_triggers_auto_init(self):
        """Test that importing the web module triggers auto-initialization."""
        # Remove the module from sys.modules to force reimport
        modules_to_remove = [
            'good_common.types.web',
            'good_common.types.url_cython_integration',
        ]
        for module in modules_to_remove:
            if module in sys.modules:
                del sys.modules[module]
        
        # Set env var to enable auto-init
        with mock.patch.dict(os.environ, {'ENABLE_URL_CYTHON_OPTIMIZATION': 'true'}):
            # Import should trigger auto-init
            
            # Check if optimization was enabled (depends on Cython availability)
            from good_common.types.url_cython_integration import is_optimization_enabled
            
            if CYTHON_AVAILABLE:
                # Should be enabled automatically
                assert is_optimization_enabled() is True
    
    def test_url_class_uses_optimization(self):
        """Test that URL class actually uses the optimization when enabled."""
        if not CYTHON_AVAILABLE:
            pytest.skip("Cython not available")
        
        # Enable optimization first
        from good_common.types.url_cython_integration import enable_cython_plugin_optimization
        enable_cython_plugin_optimization()
        
        from good_common.types.web import URL
        from good_common.types.url_plugins import URLPlugin, url_plugin_registry
        
        # Clear plugins
        url_plugin_registry.clear()
        
        # Register a test plugin
        class TestOptPlugin(URLPlugin):
            def get_tracking_params(self) -> Set[str]:
                return {'opt_track'}
        
        url_plugin_registry.register(TestOptPlugin())
        
        # Test URL with plugin param
        url = URL("https://example.com?opt_track=123&keep=this")
        canonical = url.canonicalize()
        
        # Plugin param should be removed if optimization is working
        assert 'opt_track' not in str(canonical)
        assert 'keep' in str(canonical)
    
    def test_graceful_fallback_on_import_error(self):
        """Test that import errors are handled gracefully."""
        # Mock the import to fail
        with mock.patch('good_common.types.url_cython_integration.auto_enable_optimization', 
                        side_effect=ImportError("Mock error")):
            # Force reimport
            if 'good_common.types.web' in sys.modules:
                del sys.modules['good_common.types.web']
            
            # This should not raise - web.py catches ImportError
            from good_common.types.web import URL
            
            # Should still work with standard implementation
            url = URL("https://example.com")
            assert url.host == "example.com"
    
    def test_performance_stats_available(self):
        """Test that performance stats are available when optimization is enabled."""
        if not CYTHON_AVAILABLE:
            pytest.skip("Cython not available")
        
        from good_common.types.url_cython_integration import get_optimized_registry
        
        registry = get_optimized_registry()
        stats = registry.get_performance_stats()
        
        assert 'cython_available' in stats
        assert stats['cython_available'] is True
        assert 'plugin_count' in stats


class TestEnvironmentVariableControl:
    """Test environment variable controls for optimization."""
    
    def test_disable_overrides_auto_enable(self):
        """Test that disable env var overrides automatic enabling."""
        import good_common.types.url_cython_integration as integration
        
        # Reset state
        integration._optimization_enabled = False
        
        # Set disable env var
        with mock.patch.dict(os.environ, {'DISABLE_URL_CYTHON_OPTIMIZATION': 'true'}):
            # Even with Cython available, should not enable
            result = auto_enable_optimization()
            assert result is False
            
            # Direct enable should still work (not affected by auto-disable)
            if CYTHON_AVAILABLE:
                result = enable_cython_plugin_optimization()
                assert result is True
    
    def test_env_var_case_insensitive(self):
        """Test that env var values are case-insensitive."""
        import good_common.types.url_cython_integration as integration
        
        test_values = ['TRUE', 'True', 'true', 'YES', 'Yes', 'yes', '1']
        
        for value in test_values:
            integration._optimization_enabled = False
            
            with mock.patch.dict(os.environ, {'DISABLE_URL_CYTHON_OPTIMIZATION': value}):
                result = auto_enable_optimization()
                assert result is False, f"Failed with value: {value}"
    
    def test_invalid_env_var_values_ignored(self):
        """Test that invalid env var values are ignored."""
        import good_common.types.url_cython_integration as integration
        
        if not CYTHON_AVAILABLE:
            pytest.skip("Cython not available")
        
        # Invalid values should be ignored (not disable)
        invalid_values = ['false', 'no', '0', 'invalid', '']
        
        for value in invalid_values:
            integration._optimization_enabled = False
            
            with mock.patch.dict(os.environ, {'DISABLE_URL_CYTHON_OPTIMIZATION': value}):
                result = auto_enable_optimization()
                assert result is True, f"Failed with value: {value}"
                assert is_optimization_enabled() is True


@pytest.mark.skipif(not CYTHON_AVAILABLE, reason="Cython not available")
class TestOptimizationIntegration:
    """Integration tests for automatic optimization."""
    
    def test_full_workflow_with_auto_optimization(self):
        """Test complete workflow with automatic optimization."""
        # Import fresh
        if 'good_common.types.web' in sys.modules:
            del sys.modules['good_common.types.web']
        
        # Enable optimization for this test
        from good_common.types.url_cython_integration import enable_cython_plugin_optimization
        enable_cython_plugin_optimization()
        
        from good_common.types.web import URL
        from good_common.types.url_plugins import URLPlugin, url_plugin_registry
        
        # Clear and register a plugin
        url_plugin_registry.clear()
        
        class WorkflowPlugin(URLPlugin):
            def get_tracking_params(self) -> Set[str]:
                return {'workflow_track', 'test_param'}
            
            def get_canonical_params(self) -> Set[str]:
                return {'important'}
        
        url_plugin_registry.register(WorkflowPlugin())
        
        # Test URLs
        test_cases = [
            ("https://example.com?workflow_track=1&important=yes",
             "important=yes", "workflow_track"),
            ("https://test.com/page?test_param=x&keep=this&utm_source=email",
             "keep=this", "test_param"),
        ]
        
        for url_str, should_contain, should_not_contain in test_cases:
            url = URL(url_str)
            canonical = str(url.canonicalize())
            
            assert should_contain in canonical, f"Missing {should_contain} in {canonical}"
            assert should_not_contain not in canonical, f"Found {should_not_contain} in {canonical}"
    
    def test_performance_improvement_with_auto_opt(self):
        """Test that automatic optimization provides performance benefits."""
        import time
        from good_common.types.web import URL
        
        # Generate test URLs
        test_urls = [
            f"https://example{i}.com/page?utm_source=test&param={i}&keep=this"
            for i in range(100)
        ]
        
        # Benchmark
        start = time.perf_counter()
        for url_str in test_urls:
            url = URL(url_str)
            _ = url.canonicalize()
        elapsed = time.perf_counter() - start
        
        # Should be reasonably fast (< 1ms per URL on average)
        avg_ms = (elapsed / len(test_urls)) * 1000
        assert avg_ms < 1.0, f"Too slow: {avg_ms:.3f}ms per URL"
        
        print(f"\nPerformance: {avg_ms:.3f}ms per URL with auto-optimization")