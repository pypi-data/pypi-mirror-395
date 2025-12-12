"""Performance benchmarks for URL class."""

import statistics
import time
from typing import Callable, Dict, List, Any

import pytest

from good_common.types.web import URL, UrlParseConfig
from good_common.types.url_plugins import URLPlugin, url_plugin_registry


# Test URL dataset representing different categories
TEST_URLS = [
    # Short URLs
    "https://bit.ly/3abc123",
    "https://tinyurl.com/xyz789",
    "https://t.co/abcdefghij",

    # Social media
    "https://twitter.com/user/status/1234567890?s=20&t=abc123",
    "https://www.facebook.com/photo.php?fbid=123456&set=a.789&type=3&utm_source=fb",
    "https://instagram.com/p/ABC123/?utm_medium=copy_link",
    "https://www.linkedin.com/in/john-doe/?utm_campaign=share",

    # News sites
    "https://www.cnn.com/2024/01/01/politics/article-title/index.html?utm_source=newsletter",
    "https://www.bbc.co.uk/news/world-europe-12345678?ocid=socialflow_twitter",
    "https://www.nytimes.com/2024/01/01/technology/tech-article.html?smid=tw-share",

    # E-commerce
    "https://www.amazon.com/dp/B08XYZ123/ref=sr_1_1?keywords=product&qid=1234567890",
    "https://www.ebay.com/itm/123456789012?hash=item1234567890:g:ABCDefGHIjk",

    # Blogs/personal
    "https://medium.com/@author/article-title-abc123?source=friends_link&sk=xyz789",
    "https://dev.to/username/article-slug-123?utm_source=twitter",
    "https://blog.example.com/2024/01/post-title/?ref=homepage",

    # Complex query parameters
    "https://example.com/page?utm_source=google&utm_medium=cpc&utm_campaign=spring&id=123&ref=abc&session=xyz",
    "https://shop.example.com/product?color=red&size=large&utm_content=banner&gclid=abc123&sort=price",

    # International/non-ASCII
    "https://www.example.co.jp/製品/詳細?id=123&lang=ja",
    "https://www.example.de/über-uns?source=newsletter&kampagne=2024",

    # Embedded redirects
    "https://www.google.com/url?q=https://example.com/page&source=web",
    "https://facebook.com/l.php?u=https://external.com/article",

    # Domain-specific rewrites
    "https://youtu.be/dQw4w9WgXcQ",
    "https://discord.gg/abc123xyz",
    "https://twitter.com/user/status/987654321",
]


class URLBenchmark:
    """Benchmark different URL implementations."""

    def __init__(self, test_urls: List[str] | None = None):
        self.test_urls = test_urls or TEST_URLS
        self.results: Dict[str, Dict[str, float]] = {}

    def benchmark_operation(
        self,
        name: str,
        operation: Callable[[URL], Any],
        iterations: int = 1000
    ) -> Dict[str, float]:
        """Benchmark a specific URL operation."""
        times = []

        for url_str in self.test_urls:
            url = URL(url_str)

            # Warm up
            for _ in range(10):
                operation(url)

            # Benchmark
            start = time.perf_counter()
            for _ in range(iterations):
                operation(url)
            end = time.perf_counter()

            time_per_op = (end - start) / iterations
            times.append(time_per_op)

        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times),
            'total': sum(times),
        }

    def compare_operations(self, operations: Dict[str, Callable], iterations: int = 1000):
        """Compare multiple operations."""
        for name, operation in operations.items():
            self.results[name] = self.benchmark_operation(name, operation, iterations)
        return self.results

    def print_comparison(self):
        """Print benchmark results in a readable format."""
        if not self.results:
            print("No results to display")
            return

        print("\n" + "="*60)
        print("URL Performance Benchmark Results")
        print("="*60)

        # Use first result as baseline
        baseline_name = list(self.results.keys())[0]
        baseline = self.results[baseline_name]['mean']

        for name, metrics in self.results.items():
            speedup = baseline / metrics['mean'] if metrics['mean'] > 0 else 0
            print(f"\n{name}:")
            print(f"  Mean:   {metrics['mean']*1000:.3f} ms")
            print(f"  Median: {metrics['median']*1000:.3f} ms")
            print(f"  StdDev: {metrics['stdev']*1000:.3f} ms")
            print(f"  Min:    {metrics['min']*1000:.3f} ms")
            print(f"  Max:    {metrics['max']*1000:.3f} ms")
            if name != baseline_name:
                print(f"  Speedup: {speedup:.2f}x vs {baseline_name}")


class TestPerformance:
    """Performance tests for URL operations."""

    def setup_method(self):
        """Clear registry before each test."""
        url_plugin_registry.plugins.clear()
        url_plugin_registry._invalidate_caches()

    def teardown_method(self):
        """Clean up after each test."""
        url_plugin_registry.plugins.clear()
        url_plugin_registry._invalidate_caches()

    @pytest.mark.benchmark
    def test_canonicalization_performance(self):
        """Benchmark URL canonicalization."""
        benchmark = URLBenchmark(TEST_URLS[:10])  # Use subset for faster testing

        config = UrlParseConfig(resolve_embedded_redirects=True)

        results = benchmark.compare_operations({
            'canonicalize': lambda url: url.canonicalize(config),
            'clean': lambda url: url.clean_url(config),
        })

        # Assert that operations complete in reasonable time
        assert results['canonicalize']['mean'] < 0.01  # Less than 10ms per URL
        assert results['clean']['mean'] < 0.005  # Less than 5ms per URL

    @pytest.mark.benchmark
    def test_classification_performance(self):
        """Benchmark URL classification."""
        benchmark = URLBenchmark(TEST_URLS[:10])

        results = benchmark.compare_operations({
            'is_short_url': lambda url: url.is_short_url,
            'is_adult': lambda url: url.is_adult,
            'is_homepage': lambda url: url.is_homepage,
            'classify_all': lambda url: url.classify(),
        })

        # Classification should be fast
        assert results['is_short_url']['mean'] < 0.001  # Less than 1ms
        assert results['classify_all']['mean'] < 0.005  # Less than 5ms

    @pytest.mark.benchmark
    def test_plugin_overhead(self):
        """Test performance overhead of plugin system."""
        benchmark = URLBenchmark(TEST_URLS[:10])

        # Benchmark without plugins
        config = UrlParseConfig(resolve_embedded_redirects=True)
        no_plugin_results = benchmark.benchmark_operation(
            'no_plugins',
            lambda url: url.canonicalize(config),
            iterations=100
        )

        # Add a simple plugin
        class SimplePlugin(URLPlugin):
            def get_tracking_params(self) -> set:
                return {"test_param"}

        url_plugin_registry.register(SimplePlugin())

        # Benchmark with plugin
        with_plugin_results = benchmark.benchmark_operation(
            'with_plugin',
            lambda url: url.canonicalize(config),
            iterations=100
        )

        # Calculate overhead
        overhead = (with_plugin_results['mean'] - no_plugin_results['mean']) / no_plugin_results['mean']

        # Plugin overhead should be minimal (less than 10%)
        assert overhead < 0.10, f"Plugin overhead too high: {overhead*100:.1f}%"

    @pytest.mark.benchmark
    def test_batch_processing(self):
        """Test batch URL processing performance."""
        urls = [URL(u) for u in TEST_URLS]
        config = UrlParseConfig(resolve_embedded_redirects=True)

        # Time batch processing
        start = time.perf_counter()
        _ = [url.canonicalize(config) for url in urls]
        batch_time = time.perf_counter() - start

        # Calculate throughput
        throughput = len(urls) / batch_time

        # Should process at least 100 URLs per second
        assert throughput > 100, f"Batch processing too slow: {throughput:.1f} URLs/sec"

    @pytest.mark.benchmark
    def test_caching_effectiveness(self):
        """Test that caching improves performance for repeated access."""

        # First access (cold cache)
        cold_times = []
        for _ in range(100):
            # Create new URL instance to avoid cached properties
            test_url = URL(TEST_URLS[0])
            start = time.perf_counter()
            _ = test_url.is_short_url
            cold_times.append(time.perf_counter() - start)

        # Repeated access (warm cache)
        warm_times = []
        test_url = URL(TEST_URLS[0])
        for _ in range(100):
            start = time.perf_counter()
            _ = test_url.is_short_url
            warm_times.append(time.perf_counter() - start)

        cold_mean = statistics.mean(cold_times)
        warm_mean = statistics.mean(warm_times)

        # Cached access should be at least 10x faster
        speedup = cold_mean / warm_mean if warm_mean > 0 else 0
        assert speedup > 10, f"Caching not effective enough: {speedup:.1f}x speedup"


@pytest.mark.benchmark
def test_url_benchmark_cli():
    """Run full benchmark suite (for CLI usage)."""
    # Store original plugins state
    original_plugins = url_plugin_registry.plugins.copy()

    try:
        # Clear any existing plugins for clean benchmark
        url_plugin_registry.plugins.clear()
        url_plugin_registry._invalidate_caches()

        print("\nRunning comprehensive URL performance benchmark...")

        benchmark = URLBenchmark()

        # Test different operations
        operations = {
            'parse': lambda url: (url.scheme, url.host, url.path, url.query),
            'clean': lambda url: url.clean,
            'canonicalize': lambda url: url.canonical,
            'classify': lambda url: url.classify(),
        }

        benchmark.compare_operations(operations, iterations=100)
        benchmark.print_comparison()

        # Test with plugins
        print("\n" + "="*60)
        print("Testing with plugins...")
        print("="*60)

        class TestPlugin(URLPlugin):
            def get_tracking_params(self):
                return {"fbclid", "gclid", "msclkid"}

            def get_canonical_params(self):
                return {"product_id", "article_id"}

        url_plugin_registry.register(TestPlugin())

        plugin_benchmark = URLBenchmark()
        plugin_benchmark.compare_operations(operations, iterations=100)

        # Compare overhead
        for op_name in operations:
            if op_name in benchmark.results and op_name in plugin_benchmark.results:
                base_time = benchmark.results[op_name]['mean']
                plugin_time = plugin_benchmark.results[op_name]['mean']
                overhead = ((plugin_time - base_time) / base_time) * 100
                print(f"\n{op_name} plugin overhead: {overhead:.1f}%")
    finally:
        # Restore original plugins state
        url_plugin_registry.plugins = original_plugins
        url_plugin_registry._invalidate_caches()


if __name__ == "__main__":
    # Run benchmark when executed directly
    test_url_benchmark_cli()
