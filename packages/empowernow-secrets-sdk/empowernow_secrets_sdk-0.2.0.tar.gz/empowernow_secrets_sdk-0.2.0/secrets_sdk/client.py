"""
SecretsClient - Direct vault access for service configuration.

Unlike VaultClient (PDP-enforced, request-scoped), SecretsClient is for
services resolving their own credentials at startup/config time.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
from opentelemetry import trace

from secrets_sdk.bootstrap import BootstrapConfig, load_bootstrap
from secrets_sdk.secret_uri import parse as parse_uri, SecretURI
from secrets_sdk.vault_strategies.errors import VaultAuthenticationError, VaultOperationError

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)


@dataclass
class CachedSecret:
    """Cached secret with TTL."""
    value: Any
    fetched_at: float  # time.time()
    ttl_seconds: int

    @property
    def is_expired(self) -> bool:
        return time.time() > self.fetched_at + self.ttl_seconds


@dataclass
class CacheConfig:
    """Memory cache configuration."""
    ttl_seconds: int = 300
    cache_file_secrets: bool = True  # Cache file:// URIs (disable for CSI rotation)


class SecretsClient:
    """
    Direct vault client for service configuration.

    Architecture:
    - Bootstrap: File-based (no HTTP) - solves chicken-egg problem
    - Secrets: Provider-based (file:// or openbao+kv2://) - no fallbacks

    Usage:
        # From file-based bootstrap (SYNC - no async operations)
        client = SecretsClient.create()

        # Resolve vault URI (dynamic secrets) - async
        value = await client.resolve("openbao+kv2://secret/datacollector/sapias#password")

        # Resolve file URI (static/CSI-mounted secrets) - async API, sync internally
        value = await client.resolve("file://dc-infra/kafka-password")
    """

    def __init__(
        self,
        config: BootstrapConfig,
        cache_config: CacheConfig,
        allowed_mounts: List[str],
        file_mount_path: str,
    ):
        self._config = config
        self._cache_config = cache_config
        self._allowed_mounts = allowed_mounts
        self._file_mount_path = file_mount_path
        self._cache: Dict[str, CachedSecret] = {}  # Memory cache for HTTP results
        self._token: Optional[str] = None
        self._token_expires_at: Optional[float] = None
        self._http_client: Optional[httpx.AsyncClient] = None
        self._lock = asyncio.Lock()

    @classmethod
    def create(
        cls,
        bootstrap_path: Optional[str] = None,
        cache_ttl_seconds: int = 300,
        cache_file_secrets: bool = True,
        allowed_mounts: Optional[List[str]] = None,
        file_mount_path: Optional[str] = None,
    ) -> "SecretsClient":
        """
        Create client from file-based bootstrap config.

        Bootstrap is loaded from file (no HTTP) - solves chicken-egg problem.
        Authentication is LAZY - happens on first vault access, not here.
        This allows file:// URIs to work without vault being available.

        Args:
            bootstrap_path: Path to bootstrap.json
                Precedence: explicit > SECRETS_BOOTSTRAP_PATH env > /vault/secrets/bootstrap.json > env vars

            cache_ttl_seconds: TTL for cached secrets (default: 300)

            cache_file_secrets: Cache file:// URIs (default: True)
                Set to False in environments with CSI/Docker secret rotation
                openbao+kv2:// secrets always cached regardless of this setting

            allowed_mounts: List of allowed vault mounts
                Precedence: explicit > SECRETS_ALLOWED_MOUNTS env var (required)

            file_mount_path: Base path for file:// secrets
                Precedence: explicit > FILE_MOUNT_PATH env > "/run/secrets"

        Returns:
            SecretsClient instance (authentication is lazy)

        Raises:
            FileNotFoundError: No bootstrap config found
            ValueError: Invalid bootstrap or missing allowed_mounts

        NOTE: This method is SYNC because:
        - load_bootstrap() is sync (file read only)
        - No authentication happens here (lazy auth)
        - Enables simple DI container integration
        """
        config = load_bootstrap(bootstrap_path)  # File-based, no HTTP
        cache_config = CacheConfig(
            ttl_seconds=cache_ttl_seconds,
            cache_file_secrets=cache_file_secrets,
        )

        # Fallback: parameter > environment variable
        if allowed_mounts is None:
            mounts_env = os.getenv("SECRETS_ALLOWED_MOUNTS")
            if not mounts_env:
                raise ValueError(
                    "allowed_mounts parameter or SECRETS_ALLOWED_MOUNTS env var required"
                )
            allowed_mounts = [m.strip() for m in mounts_env.split(",") if m.strip()]

        # Default file mount path
        if file_mount_path is None:
            file_mount_path = os.getenv("FILE_MOUNT_PATH", "/run/secrets")

        client = cls(config, cache_config, allowed_mounts, file_mount_path)
        # NOTE: No authentication here - lazy auth on first vault access
        # This allows file:// resolution without requiring vault
        return client

    async def _init_http_client(self) -> None:
        """Initialize HTTP client with TLS config."""
        verify: bool | str = True

        if self._config.skip_verify:
            # Check if production environment
            if os.getenv("ENVIRONMENT", "").lower() in ("production", "prod"):
                raise ValueError(
                    "skip_verify=True is not allowed in production. "
                    "Set ca_cert_path or use valid TLS certificates."
                )
            logger.warning(
                "TLS certificate verification is disabled (skip_verify=True). "
                "This is insecure and should only be used in development."
            )
            verify = False
        elif self._config.ca_cert_path:
            ca_path = Path(self._config.ca_cert_path)
            if not ca_path.exists():
                logger.warning(
                    "CA certificate file not found: %s. Using system certs.",
                    self._config.ca_cert_path
                )
                verify = True
            else:
                logger.debug("Using custom CA certificate: %s", self._config.ca_cert_path)
                verify = self._config.ca_cert_path

        self._http_client = httpx.AsyncClient(timeout=30.0, verify=verify)

    async def _authenticate(self) -> None:
        """Authenticate to vault and get token."""
        async with self._lock:
            logger.info("Authenticating to vault using method: %s", self._config.auth_method)

            if self._config.auth_method == "token":
                if self._config.token:
                    self._token = self._config.token
                    logger.debug("Using inline token for authentication")
                elif self._config.token_file:
                    self._token = Path(self._config.token_file).read_text().strip()
                    logger.debug("Using token from file: %s", self._config.token_file)
                else:
                    logger.error("Token auth configured but no token or token_file provided")
                    raise ValueError("Token auth requires token or token_file")

            elif self._config.auth_method == "kubernetes":
                self._token = await self._kubernetes_login()

            elif self._config.auth_method == "approle":
                self._token = await self._approle_login()

            else:
                logger.error("Unknown auth method: %s", self._config.auth_method)
                raise ValueError(f"Unknown auth method: {self._config.auth_method}")

            # Get token TTL
            await self._refresh_token_ttl()
            logger.info("Successfully authenticated to vault")

    async def _kubernetes_login(self) -> str:
        """Authenticate using Kubernetes ServiceAccount."""
        logger.debug("Performing Kubernetes authentication")
        jwt_path = Path(self._config.service_account_token_path)
        if not jwt_path.exists():
            logger.error("Kubernetes ServiceAccount token not found: %s", jwt_path)
            raise FileNotFoundError(f"ServiceAccount token not found: {jwt_path}")

        jwt = jwt_path.read_text().strip()
        url = f"{self._config.vault_addr}/v1/auth/{self._config.kubernetes_mount}/login"

        try:
            response = await self._http_client.post(url, json={
                "role": self._config.kubernetes_role,
                "jwt": jwt,
            })
            response.raise_for_status()
            logger.info("Successfully authenticated using Kubernetes")
            return response.json()["auth"]["client_token"]
        except httpx.HTTPStatusError as e:
            logger.error("Kubernetes authentication failed (HTTP %d)", e.response.status_code)
            raise

    async def _approle_login(self) -> str:
        """Authenticate using AppRole."""
        logger.debug("Performing AppRole authentication")
        url = f"{self._config.vault_addr}/v1/auth/{self._config.approle_mount}/login"

        try:
            response = await self._http_client.post(url, json={
                "role_id": self._config.approle_role_id,
                "secret_id": self._config.approle_secret_id,
            })
            response.raise_for_status()
            logger.info("Successfully authenticated using AppRole")
            return response.json()["auth"]["client_token"]
        except httpx.HTTPStatusError as e:
            logger.error("AppRole authentication failed (HTTP %d)", e.response.status_code)
            raise

    async def _refresh_token_ttl(self) -> None:
        """
        Look up token TTL from vault.

        Raises:
            VaultAuthenticationError: If token lacks permissions (403)
            VaultOperationError: On other HTTP errors
        """
        url = f"{self._config.vault_addr}/v1/auth/token/lookup-self"

        try:
            response = await self._http_client.get(
                url,
                headers={"X-Vault-Token": self._token},
            )

            if response.status_code == 403:
                raise VaultAuthenticationError(
                    "Token lacks permissions for token/lookup-self. "
                    "Ensure token has 'read' capability on 'auth/token/lookup-self' path."
                )

            response.raise_for_status()

            data = response.json()
            ttl = data.get("data", {}).get("ttl", 3600)
            self._token_expires_at = time.time() + ttl
            logger.debug("Token TTL refreshed: %d seconds", ttl)

        except httpx.HTTPStatusError as e:
            raise VaultOperationError(
                f"Failed to lookup token TTL (HTTP {e.response.status_code})"
            ) from e
        except httpx.RequestError as e:
            logger.warning(
                "Failed to lookup token TTL due to network error: %s. Using default 300s.",
                str(e)
            )
            self._token_expires_at = time.time() + 300
        except (json.JSONDecodeError, KeyError) as e:
            raise VaultOperationError(f"Invalid response format: {e}") from e

    async def _ensure_authenticated(self) -> None:
        """Ensure token is valid, renew if needed. Lazy initialization."""
        # Initialize HTTP client on first vault access
        if self._http_client is None:
            await self._init_http_client()

        # Check if current token is still valid
        if self._token and self._token_expires_at:
            if time.time() < self._token_expires_at - 60:
                return  # Token valid for > 1 minute

        await self._authenticate()

    async def resolve(self, uri: str, *, refresh: bool = False) -> Any:
        """
        Resolve URI to secret value.

        Provider determined by URI scheme (no fallbacks):
        - file:// → CSI-mounted file read
        - openbao+kv2:// → Vault HTTP API
        """
        with tracer.start_as_current_span("secrets_sdk.resolve") as span:
            span.set_attribute("vault.uri_hash", hashlib.sha256(uri.encode()).hexdigest()[:8])

            # Check memory cache
            if not refresh:
                cached = self._get_cached(uri)
                if cached is not None:
                    span.set_attribute("vault.cache_hit", True)
                    return cached

            span.set_attribute("vault.cache_hit", False)

            # Fetch based on provider
            value = await self._fetch_secret(uri)

            # Cache in memory
            self._set_cached(uri, value)

            return value

    def resolve_file_sync(self, uri: str) -> Any:
        """
        Synchronous resolution for file:// URIs only.

        This method is for config loading and other synchronous contexts where
        async operations are not available or practical. Only supports file://
        provider (no vault authentication needed).

        Args:
            uri: Secret URI (must be file:// provider)

        Returns:
            Secret value (dict for JSON files, str for plain text)

        Raises:
            ValueError: If URI is not file:// provider
            KeyError: If file not found
            SecretURIError: If URI is invalid or mount not allowed

        Example:
            client = SecretsClient.create()
            config = client.resolve_file_sync("file://dc-infra/kafka-password.txt")
        """
        # Parse and validate URI
        parsed = parse_uri(uri, tenant_id="local", allowed_mounts=self._allowed_mounts)

        # Enforce file:// only
        if parsed.provider != "file":
            raise ValueError(
                f"resolve_file_sync only supports file:// URIs. "
                f"Got: {parsed.provider}. Use async resolve() for vault providers."
            )

        # Read file (synchronous operation)
        return self._read_file_secret(parsed)

    async def _fetch_secret(self, uri: str) -> Any:
        """Fetch secret based on URI provider."""
        with tracer.start_as_current_span("secrets_sdk.fetch") as span:
            # Parse URI
            parsed = parse_uri(uri, tenant_id="local", allowed_mounts=self._allowed_mounts)

            span.set_attribute("vault.provider", parsed.provider)
            span.set_attribute("vault.mount", parsed.mount)

            # File provider - CSI-mounted file read
            if parsed.provider == "file":
                return self._read_file_secret(parsed)

            # Vault providers - HTTP API
            elif parsed.provider in ("openbao", "hashicorp"):
                await self._ensure_authenticated()
                return await self._fetch_vault_secret(parsed)

            else:
                raise ValueError(f"Unsupported provider: {parsed.provider}")

    def _read_file_secret(self, parsed: SecretURI) -> Any:
        """Read secret from CSI-mounted file."""
        filename = parsed.path_segments[-1] if parsed.path_segments else ""
        file_path = Path(self._file_mount_path) / parsed.mount / filename

        if not file_path.exists():
            raise KeyError(f"File not found: {file_path}")

        content = file_path.read_text()

        # Try JSON parsing, fall back to plain text
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            data = content.strip()

        # Extract fragment if specified
        if parsed.fragment_key:
            if not isinstance(data, dict):
                raise ValueError(f"Fragment '{parsed.fragment_key}' requested but file is not JSON")
            if parsed.fragment_key not in data:
                raise KeyError(f"Fragment '{parsed.fragment_key}' not found in secret")
            return data[parsed.fragment_key]

        return data

    async def _fetch_vault_secret(self, parsed: SecretURI) -> Any:
        """Fetch secret from vault via KVv2 API."""
        mount = parsed.mount
        path = "/".join(parsed.path_segments)
        fragment = parsed.fragment_key
        version = None
        for k, v in parsed.params:
            if k == "version":
                version = int(v)

        # KVv2 API
        url = f"{self._config.vault_addr}/v1/{mount}/data/{path}"
        params = {"version": version} if version else {}

        try:
            response = await self._http_client.get(
                url,
                headers={"X-Vault-Token": self._token},
                params=params,
            )

            if response.status_code == 404:
                logger.debug("Secret not found: %s", parsed.original)
                raise KeyError(f"Secret not found: {parsed.original}")

            if response.status_code == 403:
                logger.error("Access denied to secret %s (HTTP 403)", parsed.original)
                raise VaultAuthenticationError(f"Access denied to secret: {parsed.original}")

            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            logger.error(
                "HTTP error fetching secret %s (status %d): %s",
                parsed.original,
                e.response.status_code,
                e.response.text[:200]
            )
            raise VaultOperationError(
                f"Failed to fetch secret (HTTP {e.response.status_code})"
            ) from e
        except httpx.RequestError as e:
            logger.error("Network error fetching secret %s: %s", parsed.original, str(e))
            raise VaultOperationError(
                f"Failed to fetch secret due to network error: {e}"
            ) from e

        # Parse response with error handling
        try:
            response_data = response.json()
        except json.JSONDecodeError as e:
            logger.error(
                "Invalid JSON response from vault for %s: %s",
                parsed.original,
                response.text[:500]
            )
            raise VaultOperationError(f"Invalid JSON response: {e}") from e

        # Extract nested data safely
        try:
            data = response_data["data"]["data"]
        except KeyError as e:
            logger.error(
                "Malformed vault response for %s, missing key %s. Response: %s",
                parsed.original,
                str(e),
                str(response_data)[:500]
            )
            raise VaultOperationError(f"Malformed vault response, missing key {e}") from e

        # Extract fragment
        if fragment:
            if fragment not in data:
                logger.debug("Fragment '%s' not found in secret %s", fragment, parsed.original)
                raise KeyError(f"Fragment '{fragment}' not found in secret")
            return data[fragment]

        return data

    # ─────────────────────────────────────────────────────────────
    # Memory cache (for both file and HTTP-fetched secrets)
    # ─────────────────────────────────────────────────────────────

    def _get_cached(self, uri: str) -> Optional[Any]:
        """Check memory cache for previously fetched secret."""
        if uri in self._cache:
            cached = self._cache[uri]
            if not cached.is_expired:
                return cached.value
            del self._cache[uri]
        return None

    def _set_cached(self, uri: str, value: Any) -> None:
        """Store secret in memory cache."""
        # Check if file URIs should be cached
        if not self._cache_config.cache_file_secrets and uri.startswith("file://"):
            return  # Skip caching file secrets

        self._cache[uri] = CachedSecret(
            value=value,
            fetched_at=time.time(),
            ttl_seconds=self._cache_config.ttl_seconds,
        )

    async def close(self) -> None:
        """Close HTTP client."""
        if self._http_client:
            await self._http_client.aclose()

    async def __aenter__(self) -> "SecretsClient":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()
