# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .asset_lite_response import AssetLiteResponse

__all__ = ["AssetExistenceResponse"]


class AssetExistenceResponse(BaseModel):
    assets: List[AssetLiteResponse]
    """List of assets matching the query criteria"""
