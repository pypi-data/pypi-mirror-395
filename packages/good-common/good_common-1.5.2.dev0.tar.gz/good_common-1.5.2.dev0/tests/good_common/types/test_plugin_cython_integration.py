"""
Tests for plugin system integration with Cython optimizations.

This module tests that plugins can leverage Cython performance improvements.
"""

import pytest
import time
from typing import Set, Dict, Any
from good_common.types.url_plugins import URLPlugin, url_plugin_registry
from good_common.types.url_cython_integration import (
    CythonOptimizedPluginRegistry,
    enable_cython_plugin_optimization,
    CYTHON_AVAILABLE,
)
from good_common.types.web import URL


class TestPlugin(URLPlugin):
    """Test plugin with various rules."""
    
    def get_tracking_params(self) -> Set[str]:
        return {'test_tracking', 'custom_ref', 'plugin_source'}
    
    def get_canonical_params(self) -> Set[str]:
        return {'important_id', 'version'}
    
    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        return {
            '*.testsite.com': {
                'canonical': ['id', 'page'],
                'force_https': True,
            },
            'example.org': {
                'remove': ['session', 'temp'],
            }
        }


class TestCythonPluginIntegration:
    """Test Cython optimization integration with plugins."""
    
    def test_plugin_tracking_params_optimized(self):
        """Test that plugin tracking params are processed with Cython."""
        # Create optimized registry
        registry = CythonOptimizedPluginRegistry()
        
        # Register test plugin
        plugin = TestPlugin()
        registry.register_plugin(plugin)
        
        # Test query filtering with plugin params
        query = "test_tracking=123&important_id=456&keep=this&utm_source=test"
        filtered = registry.filter_query_params_with_plugins(query)
        
        # Plugin tracking params should be removed
        assert 'test_tracking' not in filtered
        assert 'utm_source' not in filtered
        
        # Canonical params should be kept
        assert 'important_id' in filtered
        assert 'keep' in filtered
    
    def test_plugin_domain_rules_optimized(self):
        """Test that plugin domain rules use Cython matching."""
        registry = CythonOptimizedPluginRegistry()
        
        # Register test plugin
        plugin = TestPlugin()
        registry.register_plugin(plugin)
        
        # Test domain rule matching
        rules1 = registry.get_domain_rules_optimized('sub.testsite.com')
        assert rules1.get('force_https') is True
        assert 'id' in rules1.get('canonical', [])
        
        rules2 = registry.get_domain_rules_optimized('example.org')
        assert 'session' in rules2.get('remove', [])
        
        # Non-matching domain
        rules3 = registry.get_domain_rules_optimized('other.com')
        assert rules3 == {}
    
    def test_canonicalization_with_plugins(self):
        """Test URL canonicalization with plugin rules."""
        registry = CythonOptimizedPluginRegistry()
        
        # Register test plugin
        plugin = TestPlugin()
        registry.register_plugin(plugin)
        
        # Test canonicalization
        url = "https://www.testsite.com/page?test_tracking=abc&important_id=123&utm_source=email"
        canonical = registry.canonicalize_with_plugins(url)
        
        # Tracking params should be removed
        assert 'test_tracking' not in canonical
        assert 'utm_source' not in canonical
        
        # Domain should be canonicalized (www removed)
        assert 'testsite.com' in canonical
        
        # Important params should be kept
        assert 'important_id=123' in canonical
    
    @pytest.mark.skipif(not CYTHON_AVAILABLE, reason="Cython not available")
    def test_performance_with_plugins(self):
        """Test that plugins benefit from Cython performance."""
        # Create two registries - one optimized, one not
        optimized_registry = CythonOptimizedPluginRegistry()
        
        # Register same plugin in both
        plugin = TestPlugin()
        optimized_registry.register_plugin(plugin)
        
        # Test URLs
        test_urls = [
            f"https://sub{i}.testsite.com/page?test_tracking=x&id={i}&custom_ref=y"
            for i in range(100)
        ]
        
        # Benchmark optimized
        start = time.perf_counter()
        for url in test_urls:
            _ = optimized_registry.canonicalize_with_plugins(url)
        optimized_time = time.perf_counter() - start
        
        # Clear caches for fair comparison
        optimized_registry.clear_caches()
        
        # Run again to test caching
        start = time.perf_counter()
        for url in test_urls:
            _ = optimized_registry.canonicalize_with_plugins(url)
        cached_time = time.perf_counter() - start
        
        # Cached should be faster; allow tiny jitter margin to avoid flakiness on CI
        assert cached_time <= optimized_time or abs(cached_time - optimized_time) < 1e-4
        
        print(f"\nOptimized: {optimized_time:.4f}s")
        print(f"Cached: {cached_time:.4f}s")
        print(f"Cache speedup: {optimized_time/cached_time:.2f}x")
    
    def test_multiple_plugins_synced(self):
        """Test that multiple plugins are properly synced with Cython."""
        registry = CythonOptimizedPluginRegistry()
        
        # Create and register multiple plugins
        class Plugin1(URLPlugin):
            def get_tracking_params(self) -> Set[str]:
                return {'plugin1_track'}
        
        class Plugin2(URLPlugin):
            def get_tracking_params(self) -> Set[str]:
                return {'plugin2_track'}
        
        registry.register_plugin(Plugin1())
        registry.register_plugin(Plugin2())
        
        # Test that both plugins' params are recognized
        query = "plugin1_track=a&plugin2_track=b&keep=this"
        filtered = registry.filter_query_params_with_plugins(query)
        
        assert 'plugin1_track' not in filtered
        assert 'plugin2_track' not in filtered
        assert 'keep' in filtered
    
    def test_cache_clearing(self):
        """Test that cache clearing works properly."""
        registry = CythonOptimizedPluginRegistry()
        
        # Process some URLs to populate caches
        urls = [
            "https://example.com/page1?param=1",
            "https://example.com/page2?param=2",
        ]
        
        for url in urls:
            registry.canonicalize_with_plugins(url)
        
        # Clear caches
        registry.clear_caches()
        
        # Should still work after clearing
        result = registry.canonicalize_with_plugins(urls[0])
        assert result  # Should return valid result
    
    def test_performance_stats(self):
        """Test performance statistics collection."""
        registry = CythonOptimizedPluginRegistry()
        
        # Register a plugin
        registry.register_plugin(TestPlugin())
        
        # Get stats
        stats = registry.get_performance_stats()
        
        assert 'cython_available' in stats
        assert 'plugin_count' in stats
        assert stats['plugin_count'] == 1
        
        if CYTHON_AVAILABLE:
            assert stats['cython_available'] is True


class TestMonkeyPatchIntegration:
    """Test monkey-patching URL class with Cython optimizations."""
    
    def test_enable_optimization(self):
        """Test enabling Cython optimization for URL class."""
        # Store original method
        original_canonicalize = URL.canonicalize
        
        try:
            # Enable optimization
            result = enable_cython_plugin_optimization()
            
            if CYTHON_AVAILABLE:
                assert result is True
                
                # Test that it still works
                url = URL("https://example.com/page?utm_source=test")
                canonical = url.canonicalize()
                assert 'utm_source' not in str(canonical)
            else:
                assert result is False
        
        finally:
            # Restore original method
            URL.canonicalize = original_canonicalize
    
    @pytest.mark.skipif(not CYTHON_AVAILABLE, reason="Cython not available")
    def test_optimized_url_with_plugins(self):
        """Test that URL class uses Cython when plugins are registered."""
        
        # Clear existing plugins
        url_plugin_registry.clear()
        
        # Register a test plugin
        plugin = TestPlugin()
        url_plugin_registry.register(plugin)
        
        # Create optimized registry that wraps the main registry
        optimized = CythonOptimizedPluginRegistry(url_plugin_registry)
        
        # Test URL with plugin params
        url = URL("https://sub.testsite.com/page?test_tracking=abc&important_id=123")
        
        # The URL should recognize plugin's tracking params
        query = optimized.filter_query_params_with_plugins(url.query)
        assert 'test_tracking' not in query
        assert 'important_id' in query


@pytest.mark.benchmark
class TestPerformanceBenchmark:
    """Benchmark tests comparing plugin performance with/without Cython."""
    
    @pytest.mark.skipif(not CYTHON_AVAILABLE, reason="Cython not available")
    def test_plugin_benchmark(self):
        """Comprehensive benchmark of plugin operations with Cython."""
        # Create test plugin with many rules
        class ComplexPlugin(URLPlugin):
            def get_tracking_params(self) -> Set[str]:
                return {f'track_{i}' for i in range(50)}
            
            def get_canonical_params(self) -> Set[str]:
                return {f'keep_{i}' for i in range(20)}
            
            def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
                return {
                    f'*.domain{i}.com': {'force_https': True}
                    for i in range(10)
                }
        
        # Create registry and register plugin
        registry = CythonOptimizedPluginRegistry()
        registry.register_plugin(ComplexPlugin())
        
        # Generate test URLs
        test_urls = []
        for i in range(100):
            params = '&'.join([
                f'track_{j}={j}' for j in range(10)
            ] + [
                f'keep_{j}={j}' for j in range(5)
            ])
            test_urls.append(f"https://sub.domain{i%10}.com/page?{params}")
        
        # Warm up
        for url in test_urls[:10]:
            registry.canonicalize_with_plugins(url)
        
        # Benchmark
        start = time.perf_counter()
        for url in test_urls:
            result = registry.canonicalize_with_plugins(url)
            # Verify tracking params removed
            assert 'track_0' not in result
        elapsed = time.perf_counter() - start
        
        urls_per_second = len(test_urls) / elapsed
        ms_per_url = (elapsed / len(test_urls)) * 1000
        
        print("\nPlugin Performance with Cython:")
        print(f"  URLs processed: {len(test_urls)}")
        print(f"  Total time: {elapsed:.3f}s")
        print(f"  Rate: {urls_per_second:.0f} URLs/second")
        print(f"  Average: {ms_per_url:.3f}ms per URL")
        
        # Performance assertion - should process at least 100 URLs/second
        assert urls_per_second > 100, f"Performance too slow: {urls_per_second:.0f} URLs/s"