#!/usr/bin/env python
"""
Performance profiling script for Cython URL optimizations.

This script compares the performance of:
1. Original Python URL implementation
2. Cython-optimized implementation
3. Pure Python fallback implementation

Run with: UV_PROJECT_ENVIRONMENT=.venv uv run python profile_url_cython.py
"""

import time
import statistics
from typing import List, Dict, Callable
from contextlib import contextmanager
import gc

# Import implementations to test
from good_common.types.web import URL as OriginalURL
from good_common.types.url_cython_optimized import (
    OptimizedURL,
    CYTHON_AVAILABLE,
    fast_canonicalize_domain,
    fast_clean_path,
    fast_filter_query_params,
    fast_normalize_url,
    URLCanonicalizer,
    URLClassifier,
)


# Test URLs representing different scenarios
TEST_URLS = [
    # Short URLs
    "https://bit.ly/abc123",
    "http://tinyurl.com/xyz789",
    # Social media with tracking
    "https://www.facebook.com/post/123?utm_source=twitter&utm_medium=social&fbclid=abc123",
    "https://twitter.com/user/status/123456789?s=20&t=xyz",
    "https://www.instagram.com/p/ABC123/?utm_source=ig_web_copy_link",
    # E-commerce with complex queries
    "https://www.amazon.com/dp/B08N5WRWNW?ref=ppx_yo_dt_b_asin_title_o00_s00&psc=1",
    "https://www.ebay.com/itm/123456789?hash=item1234567890:g:ABCDefGHIjk&var=456789",
    # News sites with tracking
    "https://www.cnn.com/2024/01/01/tech/article.html?utm_source=newsletter&utm_campaign=daily",
    "https://www.bbc.co.uk/news/technology-12345678?utm_medium=email&utm_source=govdelivery",
    # Complex paths
    "https://example.com/path/to/resource//with///multiple////slashes/?query=value",
    "https://www.example.com/path/to/file.pdf?download=true&version=2.0",
    # International domains
    "https://www.例え.jp/ページ?パラメータ=値",
    "https://münchen.de/veranstaltungen/2024/januar",
    # Various file types
    "https://cdn.example.com/images/photo.jpg?w=800&h=600&quality=85",
    "https://docs.example.com/files/document.pdf?page=1&zoom=100",
    "https://media.example.com/videos/movie.mp4?t=120&autoplay=1",
    # API endpoints
    "https://api.example.com/v2/users/123/posts?limit=10&offset=20&sort=date",
    'https://graphql.example.com/query?operation=GetUser&variables={"id":123}',
    # Long URLs with many parameters
    "https://www.google.com/search?q=python+cython+optimization&oq=python+cython&aqs=chrome.0.0i512l2j69i57j0i512l7.2827j0j7&sourceid=chrome&ie=UTF-8&utm_source=google&utm_medium=cpc&utm_campaign=search&gclid=abc123def456",
]


@contextmanager
def timer(name: str):
    """Context manager for timing operations."""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{name}: {elapsed * 1000:.3f}ms")


class BenchmarkSuite:
    """Benchmark suite for URL operations."""

    def __init__(self, urls: List[str], iterations: int = 1000):
        self.urls = urls
        self.iterations = iterations
        self.results: Dict[str, Dict[str, Dict[str, float]]] = {}

    def benchmark_function(
        self, name: str, func: Callable, *args, **kwargs
    ) -> Dict[str, float]:
        """Benchmark a single function."""
        times = []

        # Warm up
        for _ in range(10):
            func(*args, **kwargs)

        # Actual benchmark
        gc.collect()
        for _ in range(self.iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            times.append(elapsed)

        return {
            "mean": statistics.mean(times) * 1000,  # Convert to ms
            "median": statistics.median(times) * 1000,
            "stdev": statistics.stdev(times) * 1000 if len(times) > 1 else 0,
            "min": min(times) * 1000,
            "max": max(times) * 1000,
        }

    def run_url_parsing_benchmark(self):
        """Benchmark URL parsing operations."""
        print("\n" + "=" * 60)
        print("URL PARSING BENCHMARK")
        print("=" * 60)

        results: Dict[str, Dict[str, float]] = {}

        # Original implementation
        def parse_original():
            for url in self.urls:
                u = OriginalURL(url)
                _ = u.scheme
                _ = u.host
                _ = u.path
                _ = u.query

        results["Original"] = self.benchmark_function("Original", parse_original)

        # Cython implementation
        if CYTHON_AVAILABLE:

            def parse_cython():
                for url in self.urls:
                    u = OptimizedURL(url, use_cython=True)
                    _ = u.scheme
                    _ = u.host
                    _ = u.path
                    _ = u.query

            results["Cython"] = self.benchmark_function("Cython", parse_cython)

        # Pure Python fallback
        def parse_python():
            for url in self.urls:
                u = OptimizedURL(url, use_cython=False)
                _ = u.scheme
                _ = u.host
                _ = u.path
                _ = u.query

        results["Python Fallback"] = self.benchmark_function(
            "Python Fallback", parse_python
        )

        self.results["URL Parsing"] = results
        self._print_results("URL Parsing", results)

    def run_canonicalization_benchmark(self):
        """Benchmark URL canonicalization."""
        print("\n" + "=" * 60)
        print("URL CANONICALIZATION BENCHMARK")
        print("=" * 60)

        results: Dict[str, Dict[str, float]] = {}

        # Original implementation
        def canonicalize_original():
            for url in self.urls:
                u = OriginalURL(url)
                _ = u.canonicalize()

        results["Original"] = self.benchmark_function("Original", canonicalize_original)

        # Cython implementation
        if CYTHON_AVAILABLE:
            canonicalizer = URLCanonicalizer()

            def canonicalize_cython():
                for url in self.urls:
                    _ = canonicalizer.canonicalize(url)

            results["Cython"] = self.benchmark_function("Cython", canonicalize_cython)

        # Direct function call
        def canonicalize_direct():
            for url in self.urls:
                _ = fast_normalize_url(url)

        results["Direct Function"] = self.benchmark_function(
            "Direct Function", canonicalize_direct
        )

        self.results["Canonicalization"] = results
        self._print_results("Canonicalization", results)

    def run_classification_benchmark(self):
        """Benchmark URL classification."""
        print("\n" + "=" * 60)
        print("URL CLASSIFICATION BENCHMARK")
        print("=" * 60)

        results: Dict[str, Dict[str, float]] = {}

        # Original implementation
        def classify_original():
            for url in self.urls:
                u = OriginalURL(url)
                _ = u.classify()

        results["Original"] = self.benchmark_function("Original", classify_original)

        # Cython implementation
        if CYTHON_AVAILABLE:
            classifier = URLClassifier()

            def classify_cython():
                for url in self.urls:
                    _ = classifier.classify_url(url)

            results["Cython"] = self.benchmark_function("Cython", classify_cython)

        # Optimized URL class
        def classify_optimized():
            for url in self.urls:
                u = OptimizedURL(url)
                _ = u.classify()

        results["Optimized Class"] = self.benchmark_function(
            "Optimized Class", classify_optimized
        )

        self.results["Classification"] = results
        self._print_results("Classification", results)

    def run_query_filtering_benchmark(self):
        """Benchmark query parameter filtering."""
        print("\n" + "=" * 60)
        print("QUERY PARAMETER FILTERING BENCHMARK")
        print("=" * 60)

        results: Dict[str, Dict[str, float]] = {}

        # Test query strings
        queries = [
            "utm_source=google&utm_medium=cpc&page=1&sort=date",
            "fbclid=abc123&ref=homepage&category=tech&limit=10",
            "gclid=xyz789&q=search+term&filter=recent&lang=en",
        ]

        # Direct function benchmark
        def filter_direct():
            for query in queries * 10:
                _ = fast_filter_query_params(query)

        results["Direct Function"] = self.benchmark_function(
            "Direct Function", filter_direct
        )

        # With specific parameters
        keep_params = {"page", "sort", "category", "q", "filter", "limit", "lang"}

        def filter_with_params():
            for query in queries * 10:
                _ = fast_filter_query_params(query, keep_params=keep_params)

        results["With Keep Params"] = self.benchmark_function(
            "With Keep Params", filter_with_params
        )

        self.results["Query Filtering"] = results
        self._print_results("Query Filtering", results)

    def run_domain_operations_benchmark(self):
        """Benchmark domain operations."""
        print("\n" + "=" * 60)
        print("DOMAIN OPERATIONS BENCHMARK")
        print("=" * 60)

        results: Dict[str, Dict[str, float]] = {}

        domains = [
            "www.example.com",
            "WWW.EXAMPLE.COM",
            "www3.subdomain.example.co.uk",
            "example.com",
            "EXAMPLE.COM",
        ]

        # Canonicalize domain
        def canonicalize_domains():
            for domain in domains * 20:
                _ = fast_canonicalize_domain(domain)

        results["Canonicalize"] = self.benchmark_function(
            "Canonicalize", canonicalize_domains
        )

        # Clean paths
        paths = [
            "/path/to/resource/",
            "//path///to////resource//",
            "/",
            "",
            "/path/to/file.html",
        ]

        def clean_paths():
            for path in paths * 20:
                _ = fast_clean_path(path)

        results["Clean Path"] = self.benchmark_function("Clean Path", clean_paths)

        self.results["Domain Operations"] = results
        self._print_results("Domain Operations", results)

    def _print_results(self, category: str, results: Dict[str, Dict[str, float]]):
        """Print benchmark results in a formatted table."""
        if not results:
            return

        # Get baseline (first result)
        baseline_name = next(iter(results))
        baseline_mean = results[baseline_name]["mean"]

        print(f"\n{category} Results (averaged over {self.iterations} iterations):")
        print("-" * 60)
        print(
            f"{'Implementation':<20} {'Mean (ms)':<12} {'Median (ms)':<12} {'Speedup':<10}"
        )
        print("-" * 60)

        for name, metrics in results.items():
            speedup = baseline_mean / metrics["mean"] if metrics["mean"] > 0 else 0
            speedup_str = f"{speedup:.2f}x" if name != baseline_name else "baseline"
            print(
                f"{name:<20} {metrics['mean']:<12.3f} {metrics['median']:<12.3f} {speedup_str:<10}"
            )

    def print_summary(self):
        """Print overall summary."""
        print("\n" + "=" * 60)
        print("PERFORMANCE SUMMARY")
        print("=" * 60)

        if CYTHON_AVAILABLE:
            print("✓ Cython extensions are available and were tested")
        else:
            print(
                "✗ Cython extensions not available - only Python implementations tested"
            )

        print("\nTest configuration:")
        print(f"  - URLs tested: {len(self.urls)}")
        print(f"  - Iterations: {self.iterations}")

        # Calculate average speedups
        if CYTHON_AVAILABLE:
            speedups = []
            for category, category_results in self.results.items():
                if "Original" in category_results and "Cython" in category_results:
                    speedup = (
                        category_results["Original"]["mean"]
                        / category_results["Cython"]["mean"]
                    )
                    speedups.append(speedup)
                    print(f"\n{category} Cython speedup: {speedup:.2f}x")

            if speedups:
                avg_speedup = statistics.mean(speedups)
                print(f"\nAverage Cython speedup: {avg_speedup:.2f}x")


def main():
    """Run the benchmark suite."""
    print("URL Cython Optimization Performance Benchmark")
    print("=" * 60)

    # Create benchmark suite
    suite = BenchmarkSuite(TEST_URLS, iterations=1000)

    # Run benchmarks
    suite.run_url_parsing_benchmark()
    suite.run_canonicalization_benchmark()
    suite.run_classification_benchmark()
    suite.run_query_filtering_benchmark()
    suite.run_domain_operations_benchmark()

    # Print summary
    suite.print_summary()

    # Memory usage comparison (optional)
    print("\n" + "=" * 60)
    print("MEMORY USAGE COMPARISON")
    print("=" * 60)

    import sys

    # Create instances
    original_urls = [OriginalURL(url) for url in TEST_URLS]
    optimized_urls = [OptimizedURL(url) for url in TEST_URLS]

    print(f"Original URL instances: {sys.getsizeof(original_urls)} bytes")
    print(f"Optimized URL instances: {sys.getsizeof(optimized_urls)} bytes")

    # Test caching efficiency
    print("\n" + "=" * 60)
    print("CACHE EFFICIENCY TEST")
    print("=" * 60)

    canonicalizer = URLCanonicalizer(max_cache_size=100)

    # First pass - cache misses
    start = time.perf_counter()
    for url in TEST_URLS * 10:
        canonicalizer.canonicalize(url)
    first_pass = time.perf_counter() - start

    # Second pass - cache hits
    start = time.perf_counter()
    for url in TEST_URLS * 10:
        canonicalizer.canonicalize(url)
    second_pass = time.perf_counter() - start

    cache_speedup = first_pass / second_pass if second_pass > 0 else 0
    print(f"First pass (cache misses): {first_pass * 1000:.3f}ms")
    print(f"Second pass (cache hits): {second_pass * 1000:.3f}ms")
    print(f"Cache speedup: {cache_speedup:.2f}x")


if __name__ == "__main__":
    main()
