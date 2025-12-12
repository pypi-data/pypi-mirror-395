"""Example URL plugin implementation for demonstration and testing."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Dict, Optional, Pattern, Set

from .url_plugins import URLPlugin

if TYPE_CHECKING:
    from .web import URL, UrlParseConfig


class SocialMediaURLPlugin(URLPlugin):
    """Example plugin for social media URL handling."""

    def get_tracking_params(self) -> Set[str]:
        """Social media specific tracking parameters."""
        return {
            "si",  # Instagram
            "igshid",  # Instagram
            "twclid",  # Twitter
            "fbclid",  # Facebook
            "li_fat_id",  # LinkedIn
            "__tn__",  # Facebook
            "sfnsn",  # Snapchat
            "wbraid",  # WhatsApp
        }

    def get_canonical_params(self) -> Set[str]:
        """Parameters that should be preserved for social media."""
        return {
            "tweet_id",
            "post_id",
            "story_id",
            "reel_id",
            "video_id",
            "photo_id",
            "comment_id",
            "reply_comment_id",
        }

    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        """Domain-specific rules for social media sites."""
        return {
            r".*\.instagram\.com": {
                "canonical": {"p", "reel", "tv"},
                "non_canonical": {"hl", "taken-by", "tagged"},
                "force_www": True,
            },
            r".*\.tiktok\.com": {
                "canonical": {"video", "t"},
                "non_canonical": {"is_copy_url", "is_from_webapp"},
                "force_www": True,
            },
            r".*\.linkedin\.com": {
                "canonical": {"articleId", "postId"},
                "non_canonical": {"lipi", "licu"},
                "force_www": True,
            },
            r".*\.pinterest\.com": {
                "canonical": {"pin"},
                "non_canonical": {"created_at", "method"},
                "force_www": True,
            },
        }

    def get_short_url_providers(self) -> Set[str]:
        """Social media short URL providers."""
        return {
            "fb.me",  # Facebook
            "fb.watch",  # Facebook Watch
            "instagr.am",  # Instagram
            "ig.me",  # Instagram
            "vm.tiktok.com",  # TikTok
            "pin.it",  # Pinterest
            "lnkd.in",  # LinkedIn
            "sc.link",  # Snapchat
            "wa.me",  # WhatsApp
        }

    def get_bio_link_domains(self) -> Set[str]:
        """Social media bio link services."""
        return {
            "linktr.ee",
            "beacons.ai",
            "bio.link",
            "lnk.bio",
            "linkin.bio",
            "campsite.bio",
            "biolinky.co",
            "tap.bio",
        }

    def get_classification_patterns(self) -> Dict[str, Pattern]:
        """Patterns for classifying social media URLs."""
        return {
            "social_profile": re.compile(
                r"/(user|profile|people|in|@[\w]+)(/[\w\-\.]+)?/?$", re.IGNORECASE
            ),
            "social_post": re.compile(
                r"/(status|posts?|watch|reel|video|tv|p|pin)/[\w\-]+", re.IGNORECASE
            ),
            "social_story": re.compile(
                r"/(stories|highlights?)/[\w\-]+", re.IGNORECASE
            ),
            "social_hashtag": re.compile(r"/(explore/)?tags?/[\w]+", re.IGNORECASE),
        }

    def transform_url(self, url: "URL", config: "UrlParseConfig") -> Optional["URL"]:
        """Apply social media specific transformations."""
        # Import URL locally to avoid circular imports
        from .web import URL

        # Transform Instagram mobile URLs to web URLs
        if "instagram.com" in url.host and "/s/" in url.path:
            # Mobile story URLs - extract story ID and convert
            match = re.search(r"/s/([a-zA-Z0-9_-]+)", url.path)
            if match:
                story_id = match.group(1)
                return URL.build(
                    scheme="https",
                    host="www.instagram.com",
                    path=f"/stories/highlights/{story_id}/",
                )

        # Transform TikTok mobile share URLs
        if url.host == "vm.tiktok.com":
            # These are short URLs that need resolution
            # In a real implementation, you'd resolve the redirect
            # For now, just mark them as needing resolution
            pass

        # Transform Facebook mobile URLs (m.facebook.com -> www.facebook.com)
        if url.host == "m.facebook.com":
            return URL.build(
                scheme="https",
                host="www.facebook.com",
                path=url.path,
                query=url.query_params(format="plain", flat_delimiter=","),
            )

        # Transform old Twitter URLs to X.com
        if url.host in ("twitter.com", "www.twitter.com"):
            return URL.build(
                scheme="https",
                host="x.com",
                path=url.path,
                query=url.query_params(format="plain", flat_delimiter=","),
            )

        return None


class NewsMediaURLPlugin(URLPlugin):
    """Example plugin for news media URL handling."""

    def get_tracking_params(self) -> Set[str]:
        """News media specific tracking parameters."""
        return {
            "ocid",  # Microsoft News
            "smid",  # New York Times social
            "smtyp",  # New York Times type
            "curator",  # Content curator
            "ncid",  # Newsletter campaign ID
            "cndid",  # Conde Nast ID
            "__twitter_impression",
            "fs",  # From source
            "sa",  # Source attribution
            "ved",  # Google News
        }

    def get_canonical_params(self) -> Set[str]:
        """Parameters that should be preserved for news sites."""
        return {
            "page",  # Pagination
            "pg",  # Page number
            "articleId",  # Article identifier
            "storyId",  # Story identifier
        }

    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        """Domain-specific rules for news sites."""
        return {
            r".*\.cnn\.com": {
                "canonical": {"video", "live"},
                "non_canonical": {"hpt", "iref"},
            },
            r".*\.bbc\.(com|co\.uk)": {
                "canonical": {"video", "item"},
                "non_canonical": {"ocid", "ns_source"},
            },
            r".*\.nytimes\.com": {
                "canonical": {"section", "story"},
                "non_canonical": {"smid", "smtyp", "partner"},
                "force_www": True,
            },
            r".*\.washingtonpost\.com": {
                "canonical": {"story", "video"},
                "non_canonical": {"itid", "lk"},
                "force_www": True,
            },
            r".*\.reuters\.com": {
                "canonical": {"article", "video"},
                "non_canonical": {"taid", "channel"},
                "force_www": True,
            },
        }

    def get_classification_patterns(self) -> Dict[str, Pattern]:
        """Patterns for classifying news URLs."""
        return {
            "news_article": re.compile(
                r"/(article|story|news|post)/[\w\-]+", re.IGNORECASE
            ),
            "news_video": re.compile(r"/(video|watch|clip)/[\w\-]+", re.IGNORECASE),
            "news_live": re.compile(r"/(live|breaking|updates)/", re.IGNORECASE),
            "news_opinion": re.compile(
                r"/(opinion|editorial|commentary|perspective)/", re.IGNORECASE
            ),
        }


# Export plugin classes
__all__ = [
    "SocialMediaURLPlugin",
    "NewsMediaURLPlugin",
]
