# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["AssetExistenceResponse", "Asset"]


class Asset(BaseModel):
    id: str
    """Unique asset identifier with 'asset\\__' prefix"""

    checksum: str
    """
    Base64-encoded SHA-256 hash of the asset contents for duplicate detection and
    integrity
    """

    device_asset_id: str
    """Original asset identifier from the device that uploaded this asset"""

    device_id: str
    """Identifier of the device that uploaded this asset"""

    checksum_sha1: Optional[str] = None
    """Base64-encoded SHA-1 hash for Immich client compatibility.

    May be null for older assets.
    """


class AssetExistenceResponse(BaseModel):
    assets: List[Asset]
    """List of assets matching the query criteria"""
