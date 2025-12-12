"""Mapping data for pyimport2pkg."""

from .hardcoded import (
    CLASSIC_MISMATCHES,
    PTH_INJECTED_MODULES,
    BINARY_PREFERENCES,
    PLATFORM_SPECIFIC,
    get_hardcoded_mapping,
    get_all_hardcoded_modules,
)

from .namespace import (
    NAMESPACE_PACKAGES,
    NAMESPACE_PREFIXES,
    resolve_namespace_package,
    is_namespace_package,
    get_all_namespace_mappings,
)

__all__ = [
    "CLASSIC_MISMATCHES",
    "PTH_INJECTED_MODULES",
    "BINARY_PREFERENCES",
    "PLATFORM_SPECIFIC",
    "get_hardcoded_mapping",
    "get_all_hardcoded_modules",
    "NAMESPACE_PACKAGES",
    "NAMESPACE_PREFIXES",
    "resolve_namespace_package",
    "is_namespace_package",
    "get_all_namespace_mappings",
]
