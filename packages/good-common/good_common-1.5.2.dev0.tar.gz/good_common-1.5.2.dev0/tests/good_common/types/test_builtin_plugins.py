"""Tests for built-in URL plugins."""


from good_common.types.builtin_plugins import (
    AnalyticsTrackingPlugin,
    DocumentSharingPlugin,
    ECommerceURLPlugin,
    SearchEnginePlugin,
    VideoStreamingPlugin,
    load_builtin_plugins,
)
from good_common.types.url_plugins import url_plugin_registry
from good_common.types.web import URL


class TestECommercePlugin:
    """Test e-commerce URL plugin."""
    
    def setup_method(self):
        """Clear registry before each test."""
        self._original_plugins = url_plugin_registry.plugins.copy()
        url_plugin_registry.plugins.clear()
        url_plugin_registry._invalidate_caches()
    
    def teardown_method(self):
        """Restore registry after each test."""
        url_plugin_registry.plugins = self._original_plugins
        url_plugin_registry._invalidate_caches()
    
    def test_amazon_url_cleaning(self):
        """Test Amazon URL canonicalization."""
        plugin = ECommerceURLPlugin()
        URL.register_plugin(plugin)
        
        # Test Amazon product URL with tracking
        url = URL("https://www.amazon.com/dp/B08XYZ123/ref=sr_1_1?keywords=product&qid=1234567890")
        canonical = url.canonicalize()
        
        assert "ref" not in canonical.query
        assert "qid" not in canonical.query
        assert "/dp/B08XYZ123" in str(canonical)
    
    def test_amazon_mobile_transform(self):
        """Test Amazon mobile URL transformation."""
        plugin = ECommerceURLPlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://www.amazon.com/gp/aw/d/B08XYZ123")
        from good_common.types.web import UrlParseConfig
        config = UrlParseConfig()
        transformed = plugin.transform_url(url, config)
        
        assert transformed is not None
        assert "/dp/B08XYZ123" in str(transformed)
    
    def test_ebay_url_cleaning(self):
        """Test eBay URL canonicalization."""
        plugin = ECommerceURLPlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://www.ebay.com/itm/123456789012?hash=item1234567890:g:ABCDefGHIjk&_trkparms=test")
        canonical = url.canonicalize()
        
        assert "hash" not in canonical.query
        assert "_trkparms" not in canonical.query
        assert "/itm/123456789012" in str(canonical)
    
    def test_ecommerce_classification(self):
        """Test e-commerce URL classification."""
        plugin = ECommerceURLPlugin()
        patterns = plugin.get_classification_patterns()
        
        # Product page
        assert patterns["product_page"].search("/product/abc-123")
        assert patterns["product_page"].search("/dp/B0123456")
        
        # Category page
        assert patterns["category_page"].search("/category/electronics")
        
        # Search results
        assert patterns["search_results"].search("/search?q=laptop")
        
        # Shopping cart
        assert patterns["shopping_cart"].search("/cart")
        assert patterns["shopping_cart"].search("/checkout/cart")


class TestAnalyticsTrackingPlugin:
    """Test analytics tracking plugin."""
    
    def setup_method(self):
        """Clear registry before each test."""
        self._original_plugins = url_plugin_registry.plugins.copy()
        url_plugin_registry.plugins.clear()
        url_plugin_registry._invalidate_caches()
    
    def teardown_method(self):
        """Restore registry after each test."""
        url_plugin_registry.plugins = self._original_plugins
        url_plugin_registry._invalidate_caches()
    
    def test_google_analytics_removal(self):
        """Test removal of Google Analytics parameters."""
        plugin = AnalyticsTrackingPlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://example.com/page?utm_source=google&utm_medium=cpc&utm_campaign=spring&id=123")
        canonical = url.canonicalize()
        
        assert "utm_source" not in canonical.query
        assert "utm_medium" not in canonical.query
        assert "utm_campaign" not in canonical.query
        assert "id" in canonical.query
    
    def test_facebook_tracking_removal(self):
        """Test removal of Facebook tracking parameters."""
        plugin = AnalyticsTrackingPlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://example.com/article?fbclid=IwAR123456&title=test")
        canonical = url.canonicalize()
        
        assert "fbclid" not in canonical.query
        assert "title" in canonical.query
    
    def test_multiple_trackers_removal(self):
        """Test removal of multiple tracking systems."""
        plugin = AnalyticsTrackingPlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://example.com/?gclid=123&fbclid=456&msclkid=789&content=important")
        canonical = url.canonicalize()
        
        assert "gclid" not in canonical.query
        assert "fbclid" not in canonical.query
        assert "msclkid" not in canonical.query
        assert "content" in canonical.query
    
    def test_tracking_detection_patterns(self):
        """Test tracking detection patterns."""
        plugin = AnalyticsTrackingPlugin()
        patterns = plugin.get_classification_patterns()
        
        assert patterns["has_google_tracking"].search("?utm_source=google")
        assert patterns["has_google_tracking"].search("&gclid=123")
        assert patterns["has_facebook_tracking"].search("?fbclid=456")
        assert patterns["has_email_tracking"].search("?mc_cid=789")


class TestVideoStreamingPlugin:
    """Test video streaming plugin."""
    
    def setup_method(self):
        """Clear registry before each test."""
        self._original_plugins = url_plugin_registry.plugins.copy()
        url_plugin_registry.plugins.clear()
        url_plugin_registry._invalidate_caches()
    
    def teardown_method(self):
        """Restore registry after each test."""
        url_plugin_registry.plugins = self._original_plugins
        url_plugin_registry._invalidate_caches()
    
    def test_youtube_url_cleaning(self):
        """Test YouTube URL canonicalization."""
        plugin = VideoStreamingPlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be&ab_channel=RickAstley")
        canonical = url.canonicalize()
        
        assert "v" in canonical.query
        assert canonical.query["v"] == "dQw4w9WgXcQ"
        assert "feature" not in canonical.query
        assert "ab_channel" not in canonical.query
    
    def test_youtube_timestamp_preservation(self):
        """Test YouTube timestamp parameter preservation."""
        plugin = VideoStreamingPlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://youtu.be/dQw4w9WgXcQ?t=42")
        canonical = url.canonicalize()
        
        assert "t" in canonical.query
        assert canonical.query["t"] == "42"
    
    def test_youtube_mobile_transform(self):
        """Test YouTube mobile URL transformation."""
        plugin = VideoStreamingPlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://m.youtube.com/watch?v=dQw4w9WgXcQ")
        from good_common.types.web import UrlParseConfig
        config = UrlParseConfig()
        transformed = plugin.transform_url(url, config)
        
        assert transformed is not None
        assert transformed.host == "www.youtube.com"
    
    def test_video_classification(self):
        """Test video URL classification."""
        plugin = VideoStreamingPlugin()
        patterns = plugin.get_classification_patterns()
        
        assert patterns["video_watch"].search("/watch/abc123")
        assert patterns["video_watch"].search("/video/def456")
        assert patterns["video_embed"].search("/embed/123")
        assert patterns["channel"].search("/channel/UC123")
        assert patterns["channel"].search("/@username")


class TestSearchEnginePlugin:
    """Test search engine plugin."""
    
    def setup_method(self):
        """Clear registry before each test."""
        self._original_plugins = url_plugin_registry.plugins.copy()
        url_plugin_registry.plugins.clear()
        url_plugin_registry._invalidate_caches()
    
    def teardown_method(self):
        """Restore registry after each test."""
        url_plugin_registry.plugins = self._original_plugins
        url_plugin_registry._invalidate_caches()
    
    def test_google_search_cleaning(self):
        """Test Google search URL canonicalization."""
        plugin = SearchEnginePlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://www.google.com/search?q=python&ei=abc123&ved=xyz789&source=hp")
        canonical = url.canonicalize()
        
        assert "q" in canonical.query
        assert canonical.query["q"] == "python"
        assert "ei" not in canonical.query
        assert "ved" not in canonical.query
        assert "source" not in canonical.query
    
    def test_search_type_preservation(self):
        """Test search type parameter preservation."""
        plugin = SearchEnginePlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://www.google.com/search?q=cat&tbm=isch&ved=123")
        canonical = url.canonicalize()
        
        assert "q" in canonical.query
        assert "tbm" in canonical.query  # Image search
        assert "ved" not in canonical.query
    
    def test_search_classification(self):
        """Test search URL classification."""
        plugin = SearchEnginePlugin()
        patterns = plugin.get_classification_patterns()
        
        assert patterns["search_results"].search("/search?q=test")
        assert patterns["image_search"].search("?tbm=isch")
        assert patterns["video_search"].search("&tbm=vid")
        assert patterns["maps_search"].search("/maps/search")


class TestDocumentSharingPlugin:
    """Test document sharing plugin."""
    
    def setup_method(self):
        """Clear registry before each test."""
        self._original_plugins = url_plugin_registry.plugins.copy()
        url_plugin_registry.plugins.clear()
        url_plugin_registry._invalidate_caches()
    
    def teardown_method(self):
        """Restore registry after each test."""
        url_plugin_registry.plugins = self._original_plugins
        url_plugin_registry._invalidate_caches()
    
    def test_google_docs_cleaning(self):
        """Test Google Docs URL canonicalization."""
        plugin = DocumentSharingPlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://docs.google.com/document/d/1234567890/edit?usp=sharing&ouid=123")
        canonical = url.canonicalize()
        
        assert "usp" not in canonical.query
        assert "ouid" not in canonical.query
        assert "/d/1234567890/" in str(canonical)
    
    def test_dropbox_cleaning(self):
        """Test Dropbox URL canonicalization."""
        plugin = DocumentSharingPlugin()
        URL.register_plugin(plugin)
        
        url = URL("https://www.dropbox.com/s/abc123/file.pdf?dl=0&raw=1")
        canonical = url.canonicalize()
        
        assert "dl" not in canonical.query
        assert "raw" not in canonical.query
    
    def test_document_classification(self):
        """Test document URL classification."""
        plugin = DocumentSharingPlugin()
        patterns = plugin.get_classification_patterns()
        
        assert patterns["google_doc"].search("https://docs.google.com/document/d/123")
        assert patterns["google_sheet"].search("https://docs.google.com/spreadsheets/d/456")
        assert patterns["google_drive"].search("https://drive.google.com/file/d/789")
        assert patterns["shared_document"].search("/share/document123")


class TestBuiltinPluginLoading:
    """Test loading of built-in plugins."""
    
    def setup_method(self):
        """Clear registry before each test."""
        self._original_plugins = url_plugin_registry.plugins.copy()
        url_plugin_registry.plugins.clear()
        url_plugin_registry._invalidate_caches()
    
    def teardown_method(self):
        """Restore registry after each test."""
        url_plugin_registry.plugins = self._original_plugins
        url_plugin_registry._invalidate_caches()
    
    def test_load_all_builtin_plugins(self):
        """Test loading all built-in plugins."""
        load_builtin_plugins()
        
        # Should have loaded all 5 plugins
        assert len(url_plugin_registry.plugins) == 5
    
    def test_load_specific_plugins(self):
        """Test loading specific plugins."""
        load_builtin_plugins(["ecommerce", "analytics"])
        
        # Should have loaded only 2 plugins
        assert len(url_plugin_registry.plugins) == 2
        
        # Test that they work
        url = URL("https://www.amazon.com/dp/B123?ref=test&utm_source=google")
        canonical = url.canonicalize()
        
        # Both plugins should have removed their parameters
        assert "ref" not in canonical.query
        assert "utm_source" not in canonical.query
    
    def test_comprehensive_url_cleaning(self):
        """Test comprehensive URL cleaning with all plugins."""
        load_builtin_plugins()
        
        # Complex URL with multiple tracking systems
        url = URL(
            "https://www.amazon.com/dp/B08XYZ123/ref=sr_1_1?"
            "keywords=product&qid=1234567890&"
            "utm_source=google&utm_medium=cpc&"
            "fbclid=IwAR123&gclid=456"
        )
        canonical = url.canonicalize()
        
        # All tracking should be removed
        assert "ref" not in canonical.query
        assert "qid" not in canonical.query
        assert "utm_source" not in canonical.query
        assert "utm_medium" not in canonical.query
        assert "fbclid" not in canonical.query
        assert "gclid" not in canonical.query
        
        # Product ID should remain in path
        assert "/dp/B08XYZ123" in str(canonical)