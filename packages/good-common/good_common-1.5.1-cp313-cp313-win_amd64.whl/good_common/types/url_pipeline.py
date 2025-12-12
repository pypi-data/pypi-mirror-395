"""Lightweight URL processing pipeline using cytoolz."""

from __future__ import annotations

import base64
from copy import deepcopy
from typing import TYPE_CHECKING, Callable, Optional, cast

from cytoolz import pipe

from ._definitions import (
    DOMAIN_RULES,
    REGEXP_GLOBAL_CANONICAL_PARAMS,
    REGEXP_TRACKING_PARAMS,
    REGEXP_TRACKING_VALUES,
)

if TYPE_CHECKING:
    from .web import URL, UrlParseConfig


def basic_clean(url: "URL", config: "UrlParseConfig") -> "URL":
    """Apply basic URL cleaning operations."""
    from .web import URL

    _query = url.query_params(format="plain", flat_delimiter=",")
    return URL.build(
        scheme=url.scheme.lower() if not config.force_https else "https",
        username=url.username if not config.remove_auth else None,
        password=url.password if not config.remove_auth else None,
        host=url.host.lower(),
        port=url.port
        if url.port != 80 and url.port != 443 and not config.remove_standard_port
        else None,
        path=url.path,
        query=_query,
        fragment=url.fragment if not config.remove_fragment else None,
    )


def domain_specific_url_rewrites(url: "URL", config: "UrlParseConfig") -> "URL":
    """Apply domain-specific URL rewrites for known patterns."""
    from .web import URL

    match url:
        case URL(host="youtu.be", path=path) if path is not None:
            # Preserve original query parameters and add video ID
            query_params = list(url.query_params(format="plain", flat_delimiter=","))
            query_params.insert(0, ("v", path[1:]))  # Add video ID as first param
            return URL.build(
                scheme="https",
                host="www.youtube.com",
                path="/watch",
                query=query_params,
            )

        case URL(host="discord.gg", path=path) if path is not None:
            return URL.build(
                scheme="https",
                host="discord.com",
                path="/invite/" + path[1:],
            )

        case URL(host="twitter.com", path=path) if path is not None:
            return URL.build(
                scheme="https",
                host="x.com",
                path=path[1:],
                query=url.query_params(format="plain", flat_delimiter=","),
            )

    return url


def resolve_embedded_redirects(url: "URL", config: "UrlParseConfig") -> "URL":
    """Resolve embedded redirects in URLs."""
    from .web import URL

    if not config.resolve_embedded_redirects:
        return url

    query = url.query_params(format="flat")
    no_www_domain = url.host.lstrip("www.")

    keys_of_interest = config.embedded_redirect_params

    match (no_www_domain, query):
        case ("facebook.com", {"u": [u]}):
            return URL(u)

        case ("google.com", {"url": [u]}):
            return URL(u)

        case (str() as host, dict() as target_dict):
            for key, value in target_dict.items():
                if key in keys_of_interest:
                    if isinstance(value, str):
                        value = tuple([value])
                    for v in value:
                        if v.startswith("http"):
                            return URL(v)
                        elif v.startswith("//"):
                            return URL.build(
                                scheme=url.scheme,
                                host=host,
                                path=v[2:],
                            )
                        elif "/" not in value and isinstance(value, str):
                            try:
                                return URL(base64.urlsafe_b64decode(value).decode())
                            except Exception:
                                pass

    return url


def filter_canonical_params(url: "URL", config: "UrlParseConfig") -> "URL":
    """Filter query parameters to keep only canonical ones."""
    from .web import URL
    from .url_plugins import url_plugin_registry

    non_canonical_params = set()

    _config = deepcopy(config)
    _host = str(url.host)

    # Get built-in domain rules
    domain_rules = DOMAIN_RULES[_host] or {}

    # Merge with plugin domain rules
    plugin_rules = url_plugin_registry.get_domain_rules()
    for pattern, rules in plugin_rules.items():
        import re

        if re.match(pattern, _host):
            if "canonical" in rules:
                domain_rules.setdefault("canonical", set()).update(rules["canonical"])
            if "non_canonical" in rules:
                domain_rules.setdefault("non_canonical", set()).update(
                    rules["non_canonical"]
                )
            if "force_www" in rules:
                domain_rules["force_www"] = rules["force_www"]
            # If plugin provides rules, it should override the disable flag
            # Only set disable=True if plugin explicitly says so
            if "disable" in rules:
                domain_rules["disable"] = rules["disable"]
            elif "canonical" in rules or "non_canonical" in rules:
                # Plugin is providing canonicalization rules, so enable canonicalization
                domain_rules["disable"] = False

    if domain_rules.get("disable"):
        return url

    if domain_rules.get("canonical"):
        _config.canonical_params.update(domain_rules["canonical"])

    # Add plugin canonical params
    _config.canonical_params.update(url_plugin_registry.get_canonical_params())

    if domain_rules.get("non_canonical"):
        non_canonical_params.update(domain_rules["non_canonical"])

    if domain_rules.get("force_www") and not _host.startswith("www."):
        _host = f"www.{_host}"

    # Get plugin tracking params
    plugin_tracking_params = url_plugin_registry.get_tracking_params()

    new_query_params = []

    for raw_key, value in url.query_params(format="plain", flat_delimiter=","):
        # Normalize malformed keys that accidentally start with '?' due to double question marks in URL
        key = raw_key.lstrip("?") if isinstance(raw_key, str) else raw_key
        if key in _config.canonical_params:
            new_query_params.append((key, value))
        elif REGEXP_GLOBAL_CANONICAL_PARAMS.match(key) or (
            key not in non_canonical_params
            and key not in plugin_tracking_params
            and not REGEXP_TRACKING_PARAMS.match(key)
            and not REGEXP_TRACKING_VALUES.match(str(value))
        ):
            new_query_params.append((key, value))

    return URL.build(
        scheme=url.scheme,
        username=url.username,
        password=url.password,
        host=_host,
        port=url.port,
        path=url.path,
        query=new_query_params,
        fragment="",
    )


def create_cleaning_pipeline(
    config: Optional["UrlParseConfig"] = None,
) -> Callable[["URL"], "URL"]:
    """Create a URL cleaning pipeline with the given configuration."""
    from .web import UrlParseConfig

    if config is None:
        config = UrlParseConfig()

    def pipeline(url: "URL") -> "URL":
        return cast(
            "URL",
            pipe(
                url,
                lambda u: basic_clean(u, config),
                lambda u: domain_specific_url_rewrites(u, config),
            ),
        )

    return pipeline


def create_canonicalization_pipeline(
    config: Optional["UrlParseConfig"] = None,
) -> Callable[["URL"], "URL"]:
    """Create a URL canonicalization pipeline with the given configuration."""
    from .web import UrlParseConfig

    if config is None:
        config = UrlParseConfig(resolve_embedded_redirects=True)

    def pipeline(url: "URL") -> "URL":
        return cast(
            "URL",
            pipe(
                url,
                lambda u: basic_clean(u, config),
                lambda u: domain_specific_url_rewrites(u, config),
                lambda u: resolve_embedded_redirects(u, config),
                lambda u: canonicalize_path(u, config),
                lambda u: canonicalize_query(u, config),
                lambda u: filter_canonical_params(u, config),
            ),
        )

    return pipeline


def canonicalize_path(url: "URL", config: "UrlParseConfig") -> "URL":
    """Normalize duplicate slashes and trailing separators in the path."""
    from .web import URL

    path = url.path or "/"
    while "//" in path:
        path = path.replace("//", "/")
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")

    return URL.build(
        scheme=url.scheme,
        username=url.username,
        password=url.password,
        host=url.host,
        port=url.port,
        path=path or "/",
        query=url.query_params(format="plain", flat_delimiter=","),
        fragment=url.fragment,
    )


def canonicalize_query(url: "URL", config: "UrlParseConfig") -> "URL":
    """Sort query parameters for deterministic canonical form."""
    from .web import URL

    query_items = list(url.query_params(format="plain", flat_delimiter=","))
    normalized_query = sorted(query_items, key=lambda item: (item[0], item[1]))

    return URL.build(
        scheme=url.scheme,
        username=url.username,
        password=url.password,
        host=url.host,
        port=url.port,
        path=url.path,
        query=normalized_query,
        fragment=url.fragment,
    )


__all__ = [
    "basic_clean",
    "domain_specific_url_rewrites",
    "resolve_embedded_redirects",
    "filter_canonical_params",
    "canonicalize_path",
    "canonicalize_query",
    "create_cleaning_pipeline",
    "create_canonicalization_pipeline",
]
