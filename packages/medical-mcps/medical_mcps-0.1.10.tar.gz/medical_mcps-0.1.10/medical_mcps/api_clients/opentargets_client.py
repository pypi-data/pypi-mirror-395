"""OpenTargets Platform API client."""

from __future__ import annotations

import logging
from typing import Any

from .base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class OpenTargetsClient(BaseAPIClient):
    """Minimal client for the OpenTargets Platform public API."""

    def __init__(self, enable_cache: bool | None = None) -> None:
        super().__init__(
            base_url="https://api.platform.opentargets.org/api/v4",
            api_name="OpenTargets",
            timeout=30.0,
            rate_limit_delay=0.2,
            enable_cache=enable_cache,
        )

    async def search(
        self, query: str, entity: str | None = None, size: int = 10
    ) -> dict[str, Any]:
        """Search across targets, diseases, and drugs."""
        params: dict[str, Any] = {"q": query, "size": size}
        if entity:
            params["entity"] = entity
        return await self._request("GET", endpoint="/platform/public/search", params=params)

    async def get_associations(
        self,
        target_id: str | None = None,
        disease_id: str | None = None,
        size: int = 50,
    ) -> dict[str, Any]:
        """Fetch target-disease associations."""
        if not target_id and not disease_id:
            raise ValueError("Provide at least one of target_id or disease_id")
        params: dict[str, Any] = {"size": size}
        if target_id:
            params["target"] = target_id
        if disease_id:
            params["disease"] = disease_id
        return await self._request(
            "GET", endpoint="/platform/public/association", params=params
        )

    async def get_evidence(
        self,
        target_id: str,
        disease_id: str,
        size: int = 25,
    ) -> dict[str, Any]:
        """Retrieve evidence linking a target to a disease."""
        params = {"target": target_id, "disease": disease_id, "size": size}
        return await self._request(
            "GET", endpoint="/platform/public/evidence/filter", params=params
        )
