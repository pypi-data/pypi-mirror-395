"""URL Plugin System for extensible URL processing."""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, Optional, Pattern, Protocol, Set

from loguru import logger

if TYPE_CHECKING:
    from .web import URL, UrlParseConfig


class URLPluginProtocol(Protocol):
    """Protocol for URL extension plugins."""

    def get_tracking_params(self) -> Set[str]:
        """Return additional tracking parameters to filter."""
        return set()

    def get_canonical_params(self) -> Set[str]:
        """Return additional canonical parameters to preserve."""
        return set()

    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        """Return domain-specific canonicalization rules."""
        return {}

    def get_short_url_providers(self) -> Set[str]:
        """Return additional short URL provider domains."""
        return set()

    def get_html_redirect_domains(self) -> Set[str]:
        """Return additional HTML redirect domains."""
        return set()

    def get_cdn_domains(self) -> Set[str]:
        """Return additional CDN domains."""
        return set()

    def get_short_url_exclusions(self) -> Set[str]:
        """Return domains that should not be treated as short URLs."""
        return set()

    def get_bio_link_domains(self) -> Set[str]:
        """Return additional bio link domains."""
        return set()

    def get_classification_patterns(self) -> Dict[str, Pattern]:
        """Return custom classification regex patterns."""
        return {}

    def transform_url(self, url: "URL", config: "UrlParseConfig") -> Optional["URL"]:
        """Apply custom URL transformation logic."""
        return None


class URLPlugin(ABC):
    """Base class for URL plugins with default implementations."""

    def get_tracking_params(self) -> Set[str]:
        """Return additional tracking parameters to filter."""
        return set()

    def get_canonical_params(self) -> Set[str]:
        """Return additional canonical parameters to preserve."""
        return set()

    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        """Return domain-specific canonicalization rules."""
        return {}

    def get_short_url_providers(self) -> Set[str]:
        """Return additional short URL provider domains."""
        return set()

    def get_html_redirect_domains(self) -> Set[str]:
        """Return additional HTML redirect domains."""
        return set()

    def get_cdn_domains(self) -> Set[str]:
        """Return additional CDN domains."""
        return set()

    def get_short_url_exclusions(self) -> Set[str]:
        """Return domains that should not be treated as short URLs."""
        return set()

    def get_bio_link_domains(self) -> Set[str]:
        """Return additional bio link domains."""
        return set()

    def get_classification_patterns(self) -> Dict[str, Pattern]:
        """Return custom classification regex patterns."""
        return {}

    def transform_url(self, url: "URL", config: "UrlParseConfig") -> Optional["URL"]:
        """Apply custom URL transformation logic."""
        return None


@dataclass
class URLPluginRegistry:
    """Central registry for URL plugins."""

    plugins: list[URLPluginProtocol] = field(default_factory=list)
    _compiled_tracking_params: Optional[Pattern] = None
    _compiled_canonical_params: Optional[Pattern] = None
    _domain_rules_cache: Optional[Dict] = None
    _classification_cache: Dict[str, Pattern] = field(default_factory=dict)
    _short_url_providers_cache: Optional[Set[str]] = None
    _html_redirect_domains_cache: Optional[Set[str]] = None
    _cdn_domains_cache: Optional[Set[str]] = None
    _short_url_exclusions_cache: Optional[Set[str]] = None
    _bio_link_domains_cache: Optional[Set[str]] = None

    def register(self, plugin: URLPluginProtocol) -> None:
        """Register a new plugin and invalidate caches."""
        self.plugins.append(plugin)
        self._invalidate_caches()
        logger.debug(f"Registered URL plugin: {plugin.__class__.__name__}")

    def unregister(self, plugin: URLPluginProtocol) -> None:
        """Unregister a plugin and invalidate caches."""
        if plugin in self.plugins:
            self.plugins.remove(plugin)
            self._invalidate_caches()
            logger.debug(f"Unregistered URL plugin: {plugin.__class__.__name__}")

    def clear(self) -> None:
        """Clear all registered plugins and invalidate caches."""
        self.plugins.clear()
        self._invalidate_caches()
        logger.debug("Cleared all URL plugins")

    def _invalidate_caches(self) -> None:
        """Clear compiled patterns when plugins change."""
        self._compiled_tracking_params = None
        self._compiled_canonical_params = None
        self._domain_rules_cache = None
        self._classification_cache.clear()
        self._short_url_providers_cache = None
        self._html_redirect_domains_cache = None
        self._cdn_domains_cache = None
        self._short_url_exclusions_cache = None
        self._bio_link_domains_cache = None

    def get_tracking_params(self) -> Set[str]:
        """Get all tracking parameters from plugins."""
        params = set()
        for plugin in self.plugins:
            params.update(plugin.get_tracking_params())
        return params

    def get_canonical_params(self) -> Set[str]:
        """Get all canonical parameters from plugins."""
        params = set()
        for plugin in self.plugins:
            params.update(plugin.get_canonical_params())
        return params

    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        """Get merged domain rules from all plugins."""
        # Always rebuild cache if we have no plugins - this ensures clean state
        if self._domain_rules_cache is None or len(self.plugins) == 0:
            self._domain_rules_cache = {}
            for plugin in self.plugins:
                rules = plugin.get_domain_rules()
                for domain_pattern, domain_rules in rules.items():
                    if domain_pattern in self._domain_rules_cache:
                        # Merge rules for the same domain pattern
                        existing = self._domain_rules_cache[domain_pattern]
                        for key, value in domain_rules.items():
                            if key in ["canonical", "non_canonical"]:
                                # Merge sets
                                if key not in existing:
                                    existing[key] = set()
                                existing[key].update(value)
                            else:
                                # Override other values
                                existing[key] = value
                    else:
                        self._domain_rules_cache[domain_pattern] = domain_rules.copy()
        return self._domain_rules_cache

    def get_short_url_providers(self) -> Set[str]:
        """Get all short URL providers from plugins."""
        if self._short_url_providers_cache is None:
            self._short_url_providers_cache = set()
            for plugin in self.plugins:
                self._short_url_providers_cache.update(plugin.get_short_url_providers())
        return self._short_url_providers_cache

    def get_html_redirect_domains(self) -> Set[str]:
        """Get all HTML redirect domains from plugins."""
        if self._html_redirect_domains_cache is None:
            self._html_redirect_domains_cache = set()
            for plugin in self.plugins:
                self._html_redirect_domains_cache.update(
                    plugin.get_html_redirect_domains()
                )
        return self._html_redirect_domains_cache

    def get_cdn_domains(self) -> Set[str]:
        """Get all CDN domains from plugins."""
        if self._cdn_domains_cache is None:
            self._cdn_domains_cache = set()
            for plugin in self.plugins:
                self._cdn_domains_cache.update(plugin.get_cdn_domains())
        return self._cdn_domains_cache

    def get_short_url_exclusions(self) -> Set[str]:
        """Get all short URL exclusions from plugins."""
        if self._short_url_exclusions_cache is None:
            self._short_url_exclusions_cache = set()
            for plugin in self.plugins:
                self._short_url_exclusions_cache.update(
                    plugin.get_short_url_exclusions()
                )
        return self._short_url_exclusions_cache

    def get_bio_link_domains(self) -> Set[str]:
        """Get all bio link domains from plugins."""
        if self._bio_link_domains_cache is None:
            self._bio_link_domains_cache = set()
            for plugin in self.plugins:
                self._bio_link_domains_cache.update(plugin.get_bio_link_domains())
        return self._bio_link_domains_cache

    def get_classification_patterns(self) -> Dict[str, Pattern]:
        """Get all classification patterns from plugins."""
        patterns = {}
        for plugin in self.plugins:
            plugin_patterns = plugin.get_classification_patterns()
            for name, pattern in plugin_patterns.items():
                if name in patterns:
                    logger.warning(
                        f"Classification pattern '{name}' defined by multiple plugins"
                    )
                patterns[name] = pattern
        return patterns

    def apply_transformations(self, url: "URL", config: "UrlParseConfig") -> "URL":
        """Apply all plugin transformations to a URL."""
        for plugin in self.plugins:
            transformed = plugin.transform_url(url, config)
            if transformed is not None:
                url = transformed
        return url


# Global registry instance
url_plugin_registry = URLPluginRegistry()


def load_plugins() -> None:
    """Load all registered URL plugins via entry points."""
    try:
        import importlib.metadata

        for entry_point in importlib.metadata.entry_points(
            group="good_common.url_plugins"
        ):
            try:
                plugin_class = entry_point.load()
                plugin = plugin_class()
                url_plugin_registry.register(plugin)
                logger.info(f"Loaded URL plugin: {entry_point.name}")
            except Exception as e:
                logger.error(f"Failed to load URL plugin {entry_point.name}: {e}")
    except ImportError:
        # Fall back to pkg_resources for older Python versions
        try:
            import pkg_resources

            for pkg_entry_point in pkg_resources.iter_entry_points(
                "good_common.url_plugins"
            ):
                try:
                    plugin_class = pkg_entry_point.load()
                    plugin = plugin_class()
                    url_plugin_registry.register(plugin)
                    logger.info(f"Loaded URL plugin: {pkg_entry_point.name}")
                except Exception as e:
                    logger.error(
                        f"Failed to load URL plugin {pkg_entry_point.name}: {e}"
                    )
        except ImportError:
            logger.warning("No entry point loading mechanism available")


__all__ = [
    "URLPlugin",
    "URLPluginProtocol",
    "URLPluginRegistry",
    "url_plugin_registry",
    "load_plugins",
]
