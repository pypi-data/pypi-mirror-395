from __future__ import annotations

import re
import warnings
from functools import cached_property
from typing import Any, ClassVar, Literal, Self, overload
from dataclasses import dataclass, field
from urllib.parse import parse_qsl, urlencode, urljoin, quote

import courlan
import orjson
import tldextract
from loguru import logger
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, Url, core_schema


from ._definitions import (
    ADULT_AND_VIDEOS,
    BIO_LINK_DOMAINS,
    EXTENSION_REGEX,
    HTML_REDIRECT_DOMAINS,
    INDEX_PAGE_FILTER,
    NAVIGATION_FILTER,
    NOT_CRAWLABLE,
    REGEXP_SHORT_URL_EXCLUSIONS,
    SHORT_URL_PROVIDERS,
)
from .url_plugins import url_plugin_registry, load_plugins
from .url_pipeline import (
    create_cleaning_pipeline,
    create_canonicalization_pipeline,
)

# Load plugins at module import
try:
    load_plugins()
except Exception as e:
    logger.warning(f"Failed to load URL plugins: {e}")


def safe_username(username: str) -> str:
    try:
        # Let pydantic_core.Url handle encoding to avoid double-encoding issues
        return username
    except Exception:
        logger.info(username)
        return ""


@dataclass(frozen=True)
class UrlParseConfig:
    remove_auth: bool = True
    remove_fragment: bool = True
    remove_standard_port: bool = True
    resolve_embedded_redirects: bool = False
    embedded_redirect_params: set[str] = field(
        default_factory=lambda: {"redirect", "redirect_to", "url"}
    )
    canonical_params: set[str] = field(
        default_factory=lambda: {"id", "q", "v", "chash", "action"}
    )
    force_https: bool = True
    short_url_exception_domains: set[str] = field(
        default_factory=lambda: {
            "fec.gov",
            "archive.is",
            "archive.org",
            "archive.today",
            "archive.ph",
        }
    )


_default_config = UrlParseConfig()


type URLSerializableValue = str | int | float | bool


class Domain(str):
    def __new__(cls, domain: str | Domain, validate: bool = True):
        if isinstance(domain, Domain):
            return domain
        if not validate:
            _instance = super(Domain, cls).__new__(cls, domain)
            return _instance
        if not re.match(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$", domain):
            raise ValueError("Invalid domain name")

        _instance = super(Domain, cls).__new__(cls, domain)
        return _instance

    @property
    def tld(self):
        return self.rsplit(".", 1)[-1]

    @property
    def subdomains(self):
        return tuple(self.split(".")[:-2])

    @property
    def root(self):
        return self.split(".")[-2] + "." + self.tld

    @property
    def canonical(self):
        # www subdomain removed by all other subdomains kept
        subdomains = self.subdomains
        if subdomains and subdomains[0] == "www":
            subdomains = subdomains[1:]
        return ".".join(list(subdomains) + [self.root])

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))


class URL(str):
    # Class-level plugin registry
    _plugin_registry = url_plugin_registry

    __match_args__ = (
        "scheme",
        "username",
        "password",
        "host",
        "host_no_www",
        "root_domain",
        "first_significant_subdomain",
        "port",
        "path",
        "path_parts",
        "query",
        "fragment",
        "clean",
        "canonical",
        "is_short_url",
        "is_html_redirect",
        "is_possible_short_url",
        "is_adult",
        "is_homepage",
        "is_bio_link_page",
        "is_not_crawlable",
        "is_navigation_page",
        "is_valid_url",
        "file_ext",
    )
    _strict: bool = False
    __clickhouse_type__: ClassVar[str] = "String"
    _url: Url

    @classmethod
    def build(
        cls,
        *,
        scheme: str,
        username: str | None = None,
        password: str | None = None,
        host: str,
        port: int | None = None,
        path: str | None = None,
        query: str
        | list[tuple[str, URLSerializableValue]]
        | dict[str, URLSerializableValue]
        | dict[str, tuple[URLSerializableValue]]
        | None = None,
        # flat_delimiter: str = ',',
        fragment: str | None = None,
    ) -> Self:
        _query: dict[str, Any] | list[tuple[str, Any]] = {}

        if isinstance(query, str) and len(query) > 0:
            _query = parse_qsl(query)

        elif isinstance(query, dict):
            # _query = {k: query[k] for k in sorted(query.keys())}
            _query = {k: query[k] for k in sorted(query.keys())}

        elif isinstance(query, list):
            _query = sorted(query, key=lambda x: x[0])

        # If credentials are provided, manually construct URL to avoid pydantic re-encoding
        if username is not None or password is not None:
            userinfo = ""
            if username:
                userinfo = quote(username, safe="._-~")
            if password:
                userinfo = f"{userinfo}:{quote(password, safe='._-~')}"
            authority = f"{userinfo}@{host}" if userinfo else host
            if port:
                authority = f"{authority}:{port}"

            _path = path.lstrip("/") if path else ""
            _qs = urlencode(_query, doseq=True) if _query else ""
            _frag = fragment or ""

            s = f"{scheme}://{authority}/" + (_path if _path else "")
            if _qs:
                s += "?" + _qs
            if _frag:
                s += "#" + _frag
            return cls(URL(s).unicode_string())
        else:
            _url = Url.build(
                scheme=scheme,
                username=None,
                password=None,
                host=host,
                port=port,
                path=path.lstrip("/") if path else None,
                # Ensure multi-value parameters are encoded correctly when dict values are sequences
                query=urlencode(_query, doseq=True) if _query else None,
                fragment=fragment,
            )
            return cls(_url.unicode_string())

    def __new__(cls, url: str | URL, strict: bool = False):
        if isinstance(url, URL):
            return url
        _url = Url(url)
        instance = super().__new__(cls, _url.unicode_string())
        instance._url = _url
        instance._strict = strict
        return instance

    @classmethod
    def create(cls, *urls: str | URL, strict: bool = False) -> list[Self]:
        return [
            cls(url, strict=strict) if isinstance(url, str) else url for url in urls
        ]

    def __str__(self) -> str:
        return super().__str__()

    def join(self, *paths):
        _paths = ([self.path] if self.path else []) + list(paths)
        return URL.build(
            scheme=self.scheme,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            path="/".join(_paths),
            query=self.query_params(format="flat"),
            fragment=self.fragment,
        )

    def update(
        self,
        *,
        scheme: str | None = None,
        username: str | None = None,
        password: str | None = None,
        host: str | None = None,
        port: int | None = None,
        path: str | None = None,
        query: dict[str, Any] | None = None,
        fragment: str | None = None,
        remove: set[str] | None = None,
    ):
        remove = remove or set()

        def _format_val(val):
            if isinstance(val, str) or isinstance(val, int) or isinstance(val, float):
                return val
            elif isinstance(val, list):
                return ",".join(val)
            else:
                return orjson.dumps(val).decode()

        # format query-string
        if query is not None:
            query = {
                k: _format_val(v) for k, v in sorted(query.items(), key=lambda x: x[0])
            }
        else:
            query = self.query_params(format="dict", flat_delimiter=",")

        return URL.build(
            scheme=scheme or self.scheme if "scheme" not in remove else "https",
            username=username or self.username if "username" not in remove else None,
            password=password or self.password if "password" not in remove else None,
            host=host or self.host if "host" not in remove else "",
            port=port or self.port if "port" not in remove else None,
            path=path or self.path if "path" not in remove else None,
            query=query,
            fragment=fragment or self.fragment if "fragment" not in remove else None,
        )

    @classmethod
    def from_base_url(cls, base_url: str, url: str) -> URL:
        return URL(urljoin(base_url, url))

    @cached_property
    def scheme(self) -> str:
        return self._url.scheme

    @cached_property
    def username(self) -> str | None:
        return self._url.username

    @cached_property
    def password(self) -> str | None:
        return self._url.password

    @cached_property
    def host(self) -> Domain:
        if not self._url.host:
            if self._strict:
                raise ValueError("Host is not present in the URL")
            else:
                return Domain("")
        return Domain(self._url.host)

    @cached_property
    def root_domain(self) -> Domain:
        return Domain(tldextract.extract(self.host).top_domain_under_public_suffix)

    @cached_property
    def host_root(self) -> Domain:
        if self.host.startswith("www."):
            return Domain(self.host[4:])
        return Domain(self.host)

    @cached_property
    def first_significant_subdomain(self) -> Domain | None:
        if self.root_domain == self.host_root:
            return None
        parts = [
            p for p in self.host_root[: -len(self.root_domain)].split(".") if p != ""
        ]
        return Domain(parts[-1])

    @cached_property
    def host_no_www(self) -> Domain:
        warnings.warn("host_no_www is deprecated, use host_root instead")
        return Domain(self.host_root)

    @cached_property
    def file_ext(self) -> str | None:
        if _match := EXTENSION_REGEX.search(self.path):
            return _match.group(0).strip("./")
        return None

    @cached_property
    def unicode_host(self) -> str | None:
        return self._url.unicode_host()

    @cached_property
    def port(self) -> int | None:
        return self._url.port

    @cached_property
    def path(self) -> str:
        return self._url.path or ""

    @cached_property
    def path_parts(self) -> tuple[str, ...]:
        return tuple(self.path.strip("/").split("/") if self.path else [])

    @cached_property
    def query_string(self) -> str:
        return self._url.query or ""

    @cached_property
    def query(self) -> dict[str, URLSerializableValue]:
        return self.query_params(format="flat")

    @cached_property
    def fragment(self) -> str | None:
        return self._url.fragment

    @overload
    def query_params(
        self,
        format: Literal["plain"],
        flat_delimiter: str,
    ) -> list[tuple[str, URLSerializableValue]]: ...

    @overload
    def query_params(
        self,
        format: Literal["dict"],
        flat_delimiter: str,
    ) -> dict[str, tuple[URLSerializableValue]]: ...

    @overload
    def query_params(
        self,
        format: Literal["flat"],
        flat_delimiter: str = ",",
    ) -> dict[str, URLSerializableValue]: ...

    def query_params(
        self,
        format: Literal["plain", "dict", "flat"] = "flat",
        flat_delimiter: str = ",",
    ) -> (
        list[tuple[str, URLSerializableValue]]
        | dict[str, tuple[URLSerializableValue]]
        | dict[str, URLSerializableValue]
    ):
        _params = self._url.query_params()
        if format == "plain":
            return _params  # type: ignore[return-value]
        else:
            _output: dict[str, list[Any]] = {}
            for key, value in _params:
                if key not in _output:
                    _output[key] = []
                _output[key].append(value)

            if format == "dict":
                return {key: tuple(value) for key, value in _output.items()}
            else:
                return {
                    key: flat_delimiter.join(value) if len(value) > 1 else value[0]
                    for key, value in sorted(_output.items(), key=lambda x: x[0])
                }

        return _params

    def unicode_string(self) -> str:
        return self._url.unicode_string()

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))

    def clean_url(self, config: UrlParseConfig = UrlParseConfig()) -> URL:
        # Use cytoolz pipeline
        pipeline = create_cleaning_pipeline(config)
        cleaned = pipeline(self)

        # Apply plugin transformations
        cleaned = self._plugin_registry.apply_transformations(cleaned, config)

        return cleaned

    @cached_property
    def clean(self) -> URL:
        return self.clean_url()

    def canonicalize(self, config: UrlParseConfig | None = None) -> URL:
        if config is None:
            config = UrlParseConfig(resolve_embedded_redirects=True)

        if self.scheme in ("http", "https"):
            # Use cytoolz pipeline
            pipeline = create_canonicalization_pipeline(config)
            _url = pipeline(self)

            # Apply plugin transformations
            _url = self._plugin_registry.apply_transformations(_url, config)

            # Clean the URL
            _url = _url.clean_url(config)

            if _url.scheme == "http":
                _url = URL.build(
                    scheme="https",
                    host=_url.host_root,
                    path=_url.path,
                    query=_url.query,
                )
            return _url
        return self

    @cached_property
    def canonical(self) -> URL:
        return self.canonicalize()

    @cached_property
    def is_short_url(self) -> bool:
        # Check built-in providers
        built_in = any(
            provider == self.host
            for provider in SHORT_URL_PROVIDERS
            | HTML_REDIRECT_DOMAINS
            | BIO_LINK_DOMAINS
        )
        if built_in:
            return True

        # Check plugin providers
        plugin_providers = (
            self._plugin_registry.get_short_url_providers()
            | self._plugin_registry.get_html_redirect_domains()
            | self._plugin_registry.get_bio_link_domains()
        )
        return self.host in plugin_providers

    @cached_property
    def is_html_redirect(self) -> bool:
        return self.host in (
            HTML_REDIRECT_DOMAINS | self._plugin_registry.get_html_redirect_domains()
        )

    @cached_property
    def is_possible_short_url(self) -> bool:
        if self.path is None:
            return False
        if self.is_short_url:
            return True
        return all(
            [
                (
                    (len(self.host.replace(".", "")) < 10)
                    or (self.host.endswith(".link"))
                    or (self.host.startswith("on."))
                    or (self.host.startswith("go."))
                    or (self.host.startswith("l."))
                ),
                self.host
                not in (
                    _default_config.short_url_exception_domains
                    | self._plugin_registry.get_short_url_exclusions()
                ),
                len(self.path.strip("/")) < 10,
                self.path.count("/") == 1,
            ]
        ) and not REGEXP_SHORT_URL_EXCLUSIONS.match(self.host)

    @cached_property
    def is_adult(self) -> bool:
        return bool(ADULT_AND_VIDEOS.search(self))

    @cached_property
    def is_homepage(self) -> bool:
        return bool(INDEX_PAGE_FILTER.match(self.path)) or self.path == "/"

    @cached_property
    def is_not_crawlable(self) -> bool:
        return bool(NOT_CRAWLABLE.search(self))

    @cached_property
    def is_navigation_page(self) -> bool:
        return bool(NAVIGATION_FILTER.search(self))

    @cached_property
    def is_valid_url(self) -> bool:
        return courlan.filters.is_valid_url(self)

    @cached_property
    def is_bio_link_page(self):
        return self.host_root in (
            BIO_LINK_DOMAINS | self._plugin_registry.get_bio_link_domains()
        )

    def lang_filter(
        self,
        language: str | None = None,
        strict: bool = False,
        trailing_slash: bool = True,
    ) -> bool:
        return courlan.filters.lang_filter(
            self, language=language, strict=strict, trailing_slash=trailing_slash
        )

    def type_filter(
        self,
        strict: bool = False,
        with_nav: bool = False,
    ) -> bool:
        return courlan.filters.type_filter(self, strict=strict, with_nav=with_nav)

    def search(
        self,
        pat: str,
        flags: int = 0,
    ):
        return re.search(pat, self, flags)

    def match(
        self,
        pat: str,
        flags: int = 0,
    ):
        return re.match(pat, self, flags)

    def __div__(self, other):
        return self.join(other)

    @classmethod
    def register_plugin(cls, plugin):
        """Register a plugin at class level."""
        cls._plugin_registry.register(plugin)

    @classmethod
    def unregister_plugin(cls, plugin):
        """Unregister a plugin at class level."""
        cls._plugin_registry.unregister(plugin)

    def classify(self) -> dict[str, bool]:
        """Classify the URL using built-in and plugin patterns."""
        classification = {
            "is_short_url": self.is_short_url,
            "is_html_redirect": self.is_html_redirect,
            "is_possible_short_url": self.is_possible_short_url,
            "is_adult": self.is_adult,
            "is_homepage": self.is_homepage,
            "is_bio_link_page": self.is_bio_link_page,
            "is_not_crawlable": self.is_not_crawlable,
            "is_navigation_page": self.is_navigation_page,
            "is_valid_url": self.is_valid_url,
        }

        # Add plugin classifications
        plugin_patterns = self._plugin_registry.get_classification_patterns()
        for name, pattern in plugin_patterns.items():
            classification[name] = bool(pattern.search(str(self)))

        return classification


def to_url(url: str | URL) -> URL:
    if isinstance(url, URL):
        return url
    return URL(url)


__all__ = ["URL", "to_url", "Domain"]


# Automatically enable Cython optimization if available
def _auto_init_optimization():
    """Initialize Cython optimization on module import."""
    import os

    # Check if explicitly disabled
    if os.environ.get("DISABLE_URL_CYTHON_OPTIMIZATION", "").lower() in (
        "true",
        "1",
        "yes",
    ):
        return

    # Auto-enable if available (now default behavior)
    try:
        from .url_cython_integration import auto_enable_optimization

        auto_enable_optimization()
    except ImportError:
        # Cython integration not available, continue with standard implementation
        pass
    except Exception as e:
        # Log but don't fail - continue with standard implementation
        import warnings

        warnings.warn(
            f"Failed to initialize URL Cython optimization: {e}", RuntimeWarning
        )


# Run auto-initialization
_auto_init_optimization()
