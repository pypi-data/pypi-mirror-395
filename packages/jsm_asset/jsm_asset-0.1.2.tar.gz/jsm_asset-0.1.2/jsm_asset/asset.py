from __future__ import annotations

"""Compatibility shim for the original ``asset`` module.

This package was refactored into smaller modules. To preserve the original
public import surface (for ``from python_jsm_asset import asset`` or
``from python_jsm_asset.asset import *``), this file re-exports the primary
symbols from the new modules.

Keep this file minimal to avoid import cycles.
"""

# Re-export stable public API from split modules
from .session import AssetSession
from .schema import (
    AssetSchema,
    AssetObjectType,
    AssetObjectTypeAttribute,
)
from .object import AssetObject, AssetAttributeValue
from .aql import AQLQuery

__all__ = [
    "AssetSession",
    "AssetSchema",
    "AssetObjectType",
    "AssetObjectTypeAttribute",
    "AssetObject",
    "AssetAttributeValue",
    "AQLQuery",
]
