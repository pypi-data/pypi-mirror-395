"""Backward-compatibility shim for the package rename.

This module provides a minimal shim so code that still imports
``python_jsm_asset`` will continue to work while emitting a
``DeprecationWarning`` instructing users to migrate to ``jsm_asset``.

The shim only re-exports the public API from the new package and should be
kept intentionally small to avoid import cycles.
"""

from __future__ import annotations

import warnings

warnings.warn(
    "The 'python_jsm_asset' package has been renamed to 'jsm_asset'. "
    "Please update your imports to 'jsm_asset'. This shim will be removed in a "
    "future release.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export the public API from the new package. Importing specific symbols
# (instead of wildcard) reduces risk of unexpected namespace pollution.
from jsm_asset.asset import AssetSession, AssetSchema, AssetObjectType
from jsm_asset.object import AssetObject, AssetAttributeValue
from jsm_asset.aql import AQLQuery
# also expose the original module object so `from python_jsm_asset import asset`
# continues to work for callers that import the module rather than symbols.
from jsm_asset import asset as asset

__all__ = [
    "AssetSession",
    "AssetSchema",
    "AssetObjectType",
    "AssetObject",
    "AssetAttributeValue",
    "AQLQuery",
    "asset",
]
