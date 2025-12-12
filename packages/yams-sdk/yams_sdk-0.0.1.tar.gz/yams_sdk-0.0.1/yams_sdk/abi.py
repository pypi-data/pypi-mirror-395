"""C ABI plugin helpers for Python plugins that wrap native interfaces.

This module provides Python bindings and helpers for implementing YAMS plugins
that conform to the C ABI specification defined in include/yams/plugins/abi.h.

While most Python plugins will use the JSON-RPC BasePlugin approach (see base.py),
this module supports creating Python wrappers around C ABI interfaces for cases
where Python plugins need to expose C-compatible vtables.
"""

from __future__ import annotations

from enum import IntEnum
from typing import Any


class PluginABIVersion(IntEnum):
    """YAMS Plugin ABI version constants."""

    VERSION_1 = 1


class PluginErrorCode(IntEnum):
    """Standard YAMS plugin error codes matching abi.h definitions."""

    OK = 0
    ERR_INCOMPATIBLE = -1
    ERR_NOT_FOUND = -2
    ERR_INIT_FAILED = -3
    ERR_INVALID = -4
    ERR_IO = -5
    ERR_INTERNAL = -6
    ERR_UNSUPPORTED = -7


class InterfaceVersion:
    """Standard interface IDs and versions."""

    # Content extractor interface
    CONTENT_EXTRACTOR_V1_ID = "content_extractor_v1"
    CONTENT_EXTRACTOR_V1_VERSION = 1

    # Model provider interface
    MODEL_PROVIDER_V1_ID = "model_provider_v1"
    MODEL_PROVIDER_V1_VERSION = 2

    # Symbol extractor interface
    SYMBOL_EXTRACTOR_V1_ID = "symbol_extractor_v1"
    SYMBOL_EXTRACTOR_V1_VERSION = 1

    # Graph adapter interface
    GRAPH_ADAPTER_V1_ID = "graph_adapter_v1"
    GRAPH_ADAPTER_V1_VERSION = 1

    # Object storage interface
    OBJECT_STORAGE_V1_ID = "object_storage_v1"
    OBJECT_STORAGE_V1_VERSION = 1

    # Search provider interface
    SEARCH_PROVIDER_V1_ID = "search_provider_v1"
    SEARCH_PROVIDER_V1_VERSION = 1


class PluginManifest:
    """Plugin manifest structure for C ABI plugins.

    Represents the JSON manifest returned by yams_plugin_get_manifest_json().
    """

    def __init__(
        self,
        name: str,
        version: str,
        interfaces: list[dict[str, Any]],
        description: str | None = None,
        author: str | None = None,
        license: str | None = None,
        **extra: Any,
    ):
        """Initialize a plugin manifest.

        Args:
            name: Plugin name
            version: Plugin version (semver recommended)
            interfaces: List of interface dicts with "id" and "version" keys
            description: Optional plugin description
            author: Optional author information
            license: Optional license identifier
            **extra: Additional metadata fields
        """
        self.name = name
        self.version = version
        self.interfaces = interfaces
        self.description = description
        self.author = author
        self.license = license
        self.extra = extra

    def to_json(self) -> dict[str, Any]:
        """Convert manifest to JSON-serializable dict."""
        manifest = {
            "name": self.name,
            "version": self.version,
            "interfaces": self.interfaces,
        }
        if self.description:
            manifest["description"] = self.description
        if self.author:
            manifest["author"] = self.author
        if self.license:
            manifest["license"] = self.license
        manifest.update(self.extra)
        return manifest

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> PluginManifest:
        """Parse manifest from JSON dict."""
        name = data.pop("name")
        version = data.pop("version")
        interfaces = data.pop("interfaces")
        description = data.pop("description", None)
        author = data.pop("author", None)
        license = data.pop("license", None)
        return cls(
            name=name,
            version=version,
            interfaces=interfaces,
            description=description,
            author=author,
            license=license,
            **data,
        )


def validate_interface_descriptor(desc: dict[str, Any]) -> bool:
    """Validate an interface descriptor has required fields.

    Args:
        desc: Interface descriptor dict

    Returns:
        True if valid, False otherwise
    """
    return (
        isinstance(desc, dict)
        and "id" in desc
        and "version" in desc
        and isinstance(desc["id"], str)
        and isinstance(desc["version"], int)
    )


def create_interface_descriptor(iface_id: str, version: int) -> dict[str, Any]:
    """Create a standard interface descriptor.

    Args:
        iface_id: Interface ID (e.g., "content_extractor_v1")
        version: Interface version number

    Returns:
        Interface descriptor dict
    """
    return {"id": iface_id, "version": version}
