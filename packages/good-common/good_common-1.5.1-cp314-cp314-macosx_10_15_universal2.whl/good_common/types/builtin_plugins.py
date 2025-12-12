"""Built-in URL plugins for common use cases."""

import re
from typing import TYPE_CHECKING, Any, Dict, Optional, Pattern, Set

from .url_plugins import URLPlugin

if TYPE_CHECKING:
    from .web import URL, UrlParseConfig


class ECommerceURLPlugin(URLPlugin):
    """Plugin for e-commerce website URL handling."""

    def get_tracking_params(self) -> Set[str]:
        """E-commerce tracking parameters to remove."""
        return {
            # Amazon
            "ref",
            "ie",
            "psc",
            "smid",
            "m",
            "qid",
            "sr",
            "srs",
            "spIA",
            "spLa",
            "sprefix",
            "crid",
            "cv_ct_cx",
            "cv_ct_id",
            "cv_ct_pg",
            "linkCode",
            "tag",
            "linkId",
            "camp",
            "creative",
            # eBay
            "hash",
            "_trkparms",
            "_trksid",
            "amdata",
            "epid",
            "itmprp",
            # Shopify/General
            "variant",
            "currency",
            "preview_theme_id",
            "pb",
            # Etsy
            "ga_order",
            "ga_search_type",
            "ga_view_type",
            "ga_search_query",
            "ref",
            "organic_search_click",
            "frs",
            # AliExpress
            "spm",
            "algo_expid",
            "algo_pvid",
            "btsid",
            "ws_ab_test",
            # Walmart
            "wmlspartner",
            "wl0",
            "wl1",
            "wl2",
            "wl3",
            "wl4",
        }

    def get_canonical_params(self) -> Set[str]:
        """E-commerce parameters that should be preserved."""
        return {
            # Product identifiers
            "id",
            "product_id",
            "item_id",
            "sku",
            "asin",
            "isbn",
            # Variation selectors
            "color",
            "size",
            "model",
            "style",
            "option",
            # Search/filter
            "q",
            "query",
            "search",
            "category",
            "brand",
            # Pagination
            "page",
            "p",
            "offset",
            "limit",
            # Sorting
            "sort",
            "order",
            "orderby",
        }

    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        """E-commerce specific domain rules."""
        return {
            r"(.*\.)?amazon\.(com|co\.uk|de|fr|it|es|ca|jp|in|com\.br|com\.mx)": {
                "canonical": {"dp"},  # Amazon product ID
                "non_canonical": {"ref", "th", "psc"},
                "force_www": True,
            },
            r"(.*\.)?ebay\.(com|co\.uk|de|fr|it|es|ca|com\.au)": {
                "canonical": {"itm", "epid"},
                "non_canonical": {"hash", "_trkparms"},
                "force_www": True,
            },
            r"(.*\.)?etsy\.com": {
                "canonical": {"listing_id"},
                "non_canonical": {"ga_order", "ref"},
                "force_www": True,
            },
            r"(.*\.)?aliexpress\.(com|us|ru)": {
                "canonical": {"item"},
                "non_canonical": {"spm", "algo_expid"},
                "force_www": False,
            },
        }

    def get_classification_patterns(self) -> Dict[str, Pattern]:
        """E-commerce URL classification patterns."""
        return {
            "product_page": re.compile(
                r"/(product|item|listing|dp|gp/product|itm|p|goods|commodity)/",
                re.IGNORECASE,
            ),
            "category_page": re.compile(
                r"/(category|categories|c|browse|shop|store)/[\w-]+", re.IGNORECASE
            ),
            "search_results": re.compile(
                r"/(search|s|find|results|query)\?", re.IGNORECASE
            ),
            "shopping_cart": re.compile(
                r"/(cart|basket|bag|checkout/cart)", re.IGNORECASE
            ),
            "checkout": re.compile(r"/(checkout|payment|order|buy)", re.IGNORECASE),
        }

    def transform_url(self, url: "URL", config: "UrlParseConfig") -> Optional["URL"]:
        """Clean up e-commerce URLs."""
        # Amazon mobile to desktop
        if "amazon.com/gp/aw/d/" in str(url):
            from .web import URL

            return URL(str(url).replace("/gp/aw/d/", "/dp/"))

        # eBay mobile to desktop
        if url.host == "m.ebay.com":
            from .web import URL

            return URL.build(
                scheme="https",
                host="www.ebay.com",
                path=url.path,
                query=url.query_params(format="plain", flat_delimiter=","),
            )

        return None


class AnalyticsTrackingPlugin(URLPlugin):
    """Plugin for removing analytics and tracking parameters."""

    def get_canonical_params(self) -> Set[str]:
        """Common parameters that should be preserved."""
        return {
            # Content identifiers
            "id",
            "title",
            "name",
            "content",
            "article",
            "post",
            "page",
            # User/author
            "user",
            "author",
            "by",
            # Common query params
            "q",
            "query",
            "search",
            "keyword",
            # Navigation
            "view",
            "tab",
            "section",
            # API params
            "key",
            "token",
            "format",
            "type",
        }

    def get_tracking_params(self) -> Set[str]:
        """Comprehensive list of analytics tracking parameters."""
        return {
            # Google Analytics
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "utm_term",
            "utm_content",
            "utm_id",
            "utm_source_platform",
            "utm_creative_format",
            "utm_marketing_tactic",
            "gclid",
            "gclsrc",
            "dclid",
            # Google Ads
            "gbraid",
            "wbraid",
            # Facebook
            "fbclid",
            "fb_action_ids",
            "fb_action_types",
            "fb_source",
            "fb_ref",
            "fb_comment_id",
            "fbid",
            # Microsoft/Bing
            "msclkid",
            # Twitter/X
            "twclid",
            "s",
            "t",
            "ref_src",
            "ref_url",
            # LinkedIn
            "li_fat_id",
            "trk",
            "trkInfo",
            "lipi",
            "licu",
            # TikTok
            "tt_content",
            "tt_medium",
            # Pinterest
            "epik",
            "_pct",
            # Reddit
            "rdt_cid",
            "context",
            # Snapchat
            "sc_cid",
            # Adobe Analytics
            "s_kwcid",
            "ef_id",
            # Mailchimp
            "mc_cid",
            "mc_eid",
            # HubSpot
            "_hsenc",
            "_hsmi",
            "__hssc",
            "__hstc",
            "__hsfp",
            "hsCtaTracking",
            # Klaviyo
            "_ke",
            # Marketo
            "mkt_tok",
            "trk_contact",
            "trk_msg",
            "trk_module",
            "trk_sid",
            # Salesforce
            "sfmc_id",
            # General tracking
            "ref",
            "referer",
            "referrer",
            "source",
            "share_id",
            "sid",
            "cid",
            "campaign",
            "ad",
            "affiliate",
            "click_id",
            "session_id",
        }

    def get_classification_patterns(self) -> Dict[str, Pattern]:
        """Patterns to identify tracked URLs."""
        return {
            "has_google_tracking": re.compile(r"[?&](utm_|gclid=)"),
            "has_facebook_tracking": re.compile(r"[?&](fbclid=|fb_)"),
            "has_email_tracking": re.compile(r"[?&](mc_|_hsenc=|mkt_tok=)"),
        }


class VideoStreamingPlugin(URLPlugin):
    """Plugin for video streaming platforms."""

    def get_tracking_params(self) -> Set[str]:
        """Video platform tracking parameters."""
        return {
            # YouTube
            "feature",
            "ab_channel",
            "pp",
            "si",
            "ei",
            "ved",
            # Vimeo
            "from",
            "came_from",
            # Twitch
            "tt_medium",
            "tt_content",
            # General
            "autoplay",
            "mute",
            "controls",
            "showinfo",
            "rel",
        }

    def get_canonical_params(self) -> Set[str]:
        """Video parameters to preserve."""
        return {
            # Video identifiers
            "v",
            "video",
            "id",
            "clip",
            # Timestamps
            "t",
            "time",
            "start",
            "end",
            # Quality
            "quality",
            "resolution",
            # Playlist
            "list",
            "playlist",
        }

    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        """Video platform specific rules."""
        return {
            r"(.*\.)?youtube\.com": {
                "canonical": {"v", "list", "t"},
                "non_canonical": {"feature", "ab_channel"},
                "force_www": True,
            },
            r"youtu\.be": {
                "canonical": {"t", "v", "list"},
                "non_canonical": {"feature"},
                "force_www": False,
            },
            r"(.*\.)?vimeo\.com": {
                "canonical": set(),
                "non_canonical": {"from"},
                "force_www": False,
            },
            r"(.*\.)?twitch\.tv": {
                "canonical": {"video", "clip"},
                "non_canonical": {"tt_medium"},
                "force_www": True,
            },
        }

    def get_short_url_providers(self) -> Set[str]:
        """Video platform short URLs."""
        return {"youtu.be", "dai.ly", "vine.co"}

    def get_classification_patterns(self) -> Dict[str, Pattern]:
        """Video URL patterns."""
        return {
            "video_watch": re.compile(r"/(watch|video|clip|v)/"),
            "video_embed": re.compile(r"/(embed|player)/"),
            "channel": re.compile(r"/(channel|c|user|@[\w-]+)"),
            "playlist": re.compile(r"/(playlist|list)/"),
        }

    def transform_url(self, url: "URL", config: "UrlParseConfig") -> Optional["URL"]:
        """Transform video URLs."""
        # YouTube mobile to desktop
        if url.host == "m.youtube.com":
            from .web import URL

            return URL.build(
                scheme="https",
                host="www.youtube.com",
                path=url.path,
                query=url.query_params(format="plain", flat_delimiter=","),
            )

        # YouTube Music to regular YouTube
        if url.host == "music.youtube.com" and "/watch" in url.path:
            from .web import URL

            return URL.build(
                scheme="https",
                host="www.youtube.com",
                path=url.path,
                query=url.query_params(format="plain", flat_delimiter=","),
            )

        return None


class SearchEnginePlugin(URLPlugin):
    """Plugin for search engine URLs."""

    def get_tracking_params(self) -> Set[str]:
        """Search engine tracking parameters."""
        return {
            # Google
            "ei",
            "ved",
            "uact",
            "sa",
            "source",
            "sxsrf",
            "iflsig",
            "gs_lcp",
            "sclient",
            "bih",
            "biw",
            "dpr",
            "aqs",
            "sourceid",
            # Bing
            "qs",
            "form",
            "sk",
            "sc",
            "sp",
            "pq",
            "cvid",
            # DuckDuckGo
            "t",
            "ia",
            "iax",
            # Baidu
            "rsv_bp",
            "rsv_idx",
            "tn",
            "rsv_pq",
            "rsv_t",
            # Yandex
            "lr",
            "clid",
            "win",
        }

    def get_canonical_params(self) -> Set[str]:
        """Search parameters to preserve."""
        return {
            # Query
            "q",
            "query",
            "search",
            "wd",
            "text",
            # Language/region
            "hl",
            "lang",
            "lr",
            "gl",
            "cc",
            # Pagination
            "start",
            "offset",
            "page",
            "from",
            # Search type
            "tbm",
            "type",
            "channel",
            # Safe search
            "safe",
            "safesearch",
        }

    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        """Search engine specific rules."""
        return {
            r"(.*\.)?google\.(com|[a-z]{2}|co\.[a-z]{2}|com\.[a-z]{2})": {
                "canonical": {"q", "hl", "start", "tbm"},
                "non_canonical": {"ei", "ved", "source"},
                "force_www": True,
                "disable": False,  # Override built-in disable=True
            },
            r"(.*\.)?bing\.com": {
                "canonical": {"q"},
                "non_canonical": {"form", "qs"},
                "force_www": True,
            },
            r"duckduckgo\.com": {
                "canonical": {"q"},
                "non_canonical": {"t", "ia"},
                "force_www": False,
            },
        }

    def get_classification_patterns(self) -> Dict[str, Pattern]:
        """Search engine URL patterns."""
        return {
            "search_results": re.compile(r"/(search|s)\?"),
            "image_search": re.compile(r"[?&]tbm=isch"),
            "video_search": re.compile(r"[?&]tbm=vid"),
            "news_search": re.compile(r"[?&]tbm=nws"),
            "maps_search": re.compile(r"/maps(/search)?"),
        }


class DocumentSharingPlugin(URLPlugin):
    """Plugin for document sharing and cloud storage platforms."""

    def get_tracking_params(self) -> Set[str]:
        """Document sharing tracking parameters."""
        return {
            # Google Drive/Docs
            "usp",
            "ouid",
            "rtpof",
            "sd",
            "ltmpl",
            # Dropbox
            "dl",
            "raw",
            "lst",
            "preview",
            # OneDrive
            "e",
            "v",
            "ct",
            "wt",
            "wx",
            # Box
            "shared_link",
            "sharedlink",
            # General
            "download",
            "export",
            "print",
        }

    def get_canonical_params(self) -> Set[str]:
        """Document parameters to preserve."""
        return {
            # Document identifiers
            "id",
            "docid",
            "file",
            "doc",
            # View settings
            "view",
            "mode",
            "action",
            # Sharing
            "sharing",
            "share",
        }

    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        """Document platform specific rules."""
        return {
            r"docs\.google\.com": {
                "canonical": {"id"},
                "non_canonical": {"usp", "ouid"},
                "force_www": False,
            },
            r"drive\.google\.com": {
                "canonical": {"id"},
                "non_canonical": {"usp"},
                "force_www": False,
            },
            r"(.*\.)?dropbox\.com": {
                "canonical": set(),
                "non_canonical": {"dl", "raw"},
                "force_www": True,
            },
            r"(.*\.)?box\.com": {
                "canonical": {"shared_link"},
                "non_canonical": set(),
                "force_www": True,
            },
        }

    def get_classification_patterns(self) -> Dict[str, Pattern]:
        """Document URL patterns."""
        return {
            "google_doc": re.compile(r"docs\.google\.com/document/"),
            "google_sheet": re.compile(r"docs\.google\.com/spreadsheets/"),
            "google_slide": re.compile(r"docs\.google\.com/presentation/"),
            "google_drive": re.compile(r"drive\.google\.com/"),
            "dropbox_file": re.compile(r"dropbox\.com/.*/.*\.[a-z]{2,4}"),
            "shared_document": re.compile(r"/(share|shared|s)/"),
        }


# Registry of all built-in plugins
BUILTIN_PLUGINS = {
    "ecommerce": ECommerceURLPlugin,
    "analytics": AnalyticsTrackingPlugin,
    "video": VideoStreamingPlugin,
    "search": SearchEnginePlugin,
    "documents": DocumentSharingPlugin,
}


def load_builtin_plugins(plugins: list[str] | None = None) -> None:
    """Load built-in plugins into the registry.

    Args:
        plugins: List of plugin names to load. If None, loads all.
    """
    from .url_plugins import url_plugin_registry

    if plugins is None:
        plugins = list(BUILTIN_PLUGINS.keys())

    for plugin_name in plugins:
        if plugin_name in BUILTIN_PLUGINS:
            plugin_class = BUILTIN_PLUGINS[plugin_name]
            url_plugin_registry.register(plugin_class())
