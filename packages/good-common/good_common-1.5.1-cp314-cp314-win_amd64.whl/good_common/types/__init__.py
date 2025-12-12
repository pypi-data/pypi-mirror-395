"""
Good Common Types Module

This module provides type definitions and utilities, with optimized lazy loading
for heavy dependencies to improve import performance.
"""

import typing
from typing import TYPE_CHECKING

from ._base import PythonImportableObject, StringDict
from ._fields import (
    DateTimeField,
    StringDictField,
    UPPER_CASE_STRING,
    UUID,
    UUIDField,
    VALID_ZIP_CODE,
)
from .placeholder import placeholder

# Lazy imports - these will be loaded on first use
_URL = None
_Domain = None
_to_url = None
_Identifier = None
_URLPlugin = None
_URLPluginRegistry = None
_url_plugin_registry = None
_load_plugins = None
_load_builtin_plugins = None

if TYPE_CHECKING:
    # For type checking, import everything
    from .web import URL as _URLType, Domain as _DomainType, to_url as _to_url_func
    from ._base import Identifier as _IdentifierType
    from .url_plugins import (
        URLPlugin as _URLPluginType,
        URLPluginRegistry as _URLPluginRegistryType,
        url_plugin_registry as _url_plugin_registry_inst,
        load_plugins as _load_plugins_func,
    )
    from .builtin_plugins import load_builtin_plugins as _load_builtin_plugins_func

    URL = _URLType
    Domain = _DomainType
    to_url = _to_url_func
    Identifier = _IdentifierType
    URLPlugin = _URLPluginType
    URLPluginRegistry = _URLPluginRegistryType
    url_plugin_registry = _url_plugin_registry_inst
    load_plugins = _load_plugins_func
    load_builtin_plugins = _load_builtin_plugins_func
else:
    # Runtime lazy loading implementation
    def __getattr__(name: str) -> typing.Any:
        """Lazy load heavy modules on first access."""
        global _URL, _Domain, _to_url, _Identifier
        global \
            _URLPlugin, \
            _URLPluginRegistry, \
            _url_plugin_registry, \
            _load_plugins, \
            _load_builtin_plugins

        if name == "URL":
            if _URL is None:
                from .web import URL as _URL
            return _URL
        elif name == "Domain":
            if _Domain is None:
                from .web import Domain as _Domain
            return _Domain
        elif name == "to_url":
            if _to_url is None:
                from .web import to_url as _to_url
            return _to_url
        elif name == "Identifier":
            if _Identifier is None:
                from ._base import Identifier as _Identifier
            return _Identifier
        elif name == "URLPlugin":
            if _URLPlugin is None:
                from .url_plugins import URLPlugin as _URLPlugin
            return _URLPlugin
        elif name == "URLPluginRegistry":
            if _URLPluginRegistry is None:
                from .url_plugins import URLPluginRegistry as _URLPluginRegistry
            return _URLPluginRegistry
        elif name == "url_plugin_registry":
            if _url_plugin_registry is None:
                from .url_plugins import url_plugin_registry as _url_plugin_registry
            return _url_plugin_registry
        elif name == "load_plugins":
            if _load_plugins is None:
                from .url_plugins import load_plugins as _load_plugins
            return _load_plugins
        elif name == "load_builtin_plugins":
            if _load_builtin_plugins is None:
                from .builtin_plugins import (
                    load_builtin_plugins as _load_builtin_plugins,
                )
            return _load_builtin_plugins
        else:
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "UUID",
    "URL",
    "Domain",
    "to_url",
    "placeholder",
    "UUIDField",
    "StringDictField",
    "DateTimeField",
    "VALID_ZIP_CODE",
    "UPPER_CASE_STRING",
    "StringDict",
    "Identifier",
    "PythonImportableObject",
    "URLPlugin",
    "URLPluginRegistry",
    "url_plugin_registry",
    "load_plugins",
    "load_builtin_plugins",
]
