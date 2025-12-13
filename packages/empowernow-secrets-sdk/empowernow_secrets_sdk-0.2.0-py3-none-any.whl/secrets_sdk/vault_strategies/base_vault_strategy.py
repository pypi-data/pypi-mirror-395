from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseVaultStrategy(ABC):
    @abstractmethod
    async def get_credentials(self, credential_reference: str) -> Dict[str, Any]:
        """Return secret payload; for KVv2 path+version this is the inner data mapping."""

    async def get_credentials_wrapped(self, credential_reference: str, wrap_ttl: str) -> Dict[str, Any]:  # pragma: no cover - optional
        raise NotImplementedError

    async def unwrap_token(self, wrap_token: str) -> Dict[str, Any]:  # pragma: no cover - optional
        raise NotImplementedError

    async def read_secret_metadata(self, path: str) -> Dict[str, Any]:  # pragma: no cover - optional
        raise NotImplementedError

    async def list_keys(self, path: str) -> list[str]:  # pragma: no cover - optional
        raise NotImplementedError


