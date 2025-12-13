from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from secrets_sdk.secret_uri import parse as parse_uri
from secrets_sdk.vault_strategies.base_vault_strategy import BaseVaultStrategy
from secrets_sdk.vault_strategies.errors import (
    VaultAuthenticationError,
    VaultOperationError,
    VaultSecretNotFoundError,
    VaultSecretVersionDeletedError,
    VaultSecretVersionDestroyedError,
    VaultTimeoutError,
)


@dataclass
class VaultConfigData:
    url: str
    token: str | None
    timeout: int = 30
    verify_ssl: bool = True
    allowed_mounts: List[str] = field(default_factory=lambda: ["secret"])


class HashiCorpVaultStrategy(BaseVaultStrategy):
    def __init__(self, config: Dict[str, Any]):
        self.config = VaultConfigData(
            url=config["url"],
            token=config.get("token"),
            timeout=int(config.get("timeout", 30)),
            verify_ssl=bool(config.get("verify_ssl", True)),
            allowed_mounts=config.get("allowed_mounts", ["secret"]),
        )
        self._skip_auth_check = bool(config.get("skip_auth_check", False))
        self._http_client: httpx.AsyncClient | None = None
        self._authenticated = False

    async def _ensure_http_client(self) -> None:
        """Lazy initialization of HTTP client and authentication."""
        if self._http_client is not None:
            return

        self._http_client = httpx.AsyncClient(
            timeout=float(self.config.timeout),
            verify=self.config.verify_ssl,
        )

        if not self._skip_auth_check:
            await self._verify_authentication()

    async def _verify_authentication(self) -> None:
        """Verify token is valid via token lookup-self."""
        if not self.config.token:
            raise VaultAuthenticationError("No token provided for HashiCorp Vault")

        url = f"{self.config.url}/v1/auth/token/lookup-self"
        try:
            response = await self._http_client.get(
                url,
                headers={"X-Vault-Token": self.config.token},
            )
            if response.status_code == 403:
                raise VaultAuthenticationError("Failed to authenticate with HashiCorp Vault")
            response.raise_for_status()
            self._authenticated = True
        except httpx.RequestError as e:
            raise VaultAuthenticationError(f"Failed to authenticate with HashiCorp Vault: {e}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type((ConnectionError, TimeoutError, VaultTimeoutError, httpx.RequestError)),
        reraise=True,
    )
    async def _read_secret_kvv2(self, path: str, version: Optional[int]) -> Dict[str, Any]:
        await self._ensure_http_client()

        # Build URL - path includes mount (e.g., "secret/datacollector/name")
        # Insert /data/ for KVv2 API
        parts = path.split("/", 1)
        if len(parts) == 2:
            mount, secret_path = parts[0], parts[1]
        else:
            mount, secret_path = path, ""

        url = f"{self.config.url}/v1/{mount}/data/{secret_path}"
        params: Dict[str, Any] = {"version": version} if version is not None else {}

        try:
            response = await self._http_client.get(
                url,
                headers={"X-Vault-Token": self.config.token},
                params=params,
            )

            if response.status_code == 404:
                raise VaultSecretNotFoundError(f"Secret not found at '{path}'")
            if response.status_code == 403:
                raise VaultAuthenticationError(f"Access denied to secret at '{path}'")

            response.raise_for_status()
            resp = response.json()

            if not resp or "data" not in resp:
                raise VaultOperationError("Invalid response format from Vault")

            return resp

        except httpx.TimeoutException as e:
            raise VaultTimeoutError(f"Timeout reading secret at '{path}'") from e
        except httpx.RequestError as e:
            raise VaultOperationError(f"Failed to read secret: {e}") from e

    async def get_credentials(self, credential_reference: str) -> Dict[str, Any]:
        version: Optional[int] = None
        fragment_key: Optional[str] = None
        path = credential_reference
        if "://" in credential_reference:
            uri = parse_uri(credential_reference, tenant_id="dev", allowed_mounts=self.config.allowed_mounts)  # type: ignore[arg-type]
            if uri.engine and uri.engine != "kv2":
                raise VaultOperationError(f"Unsupported engine '{uri.engine}' for HashiCorp Vault")
            path = "/".join([uri.mount] + list(uri.path_segments))
            fragment_key = uri.fragment_key
            for k, v in uri.params:
                if k == "version":
                    version = int(v)
                    break
        resp = await self._read_secret_kvv2(path, version)
        inner = (resp or {}).get("data", {})
        metadata = inner.get("metadata", {})
        if version is not None:
            if metadata.get("destroyed") is True:
                raise VaultSecretVersionDestroyedError(f"Version {version} destroyed for '{path}'")
            deletion_time = metadata.get("deletion_time")
            if deletion_time and str(deletion_time).strip():
                raise VaultSecretVersionDeletedError(f"Version {version} deleted for '{path}'")
        payload = inner.get("data")
        if payload is None:
            raise VaultOperationError("Malformed response from Vault")
        if fragment_key:
            return {fragment_key: payload.get(fragment_key)} if isinstance(payload, dict) else {fragment_key: None}
        return payload

    async def close(self) -> None:
        """Close HTTP client."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None
