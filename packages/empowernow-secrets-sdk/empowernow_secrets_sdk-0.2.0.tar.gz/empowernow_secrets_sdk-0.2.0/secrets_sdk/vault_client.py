from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from secrets_sdk.audit import AuditPublisher
from secrets_sdk.context import ExecutionContext
from secrets_sdk.errors import (
    AuthzDeniedError,
    BindingDriftError,
    PDPUnavailableError,
)
from secrets_sdk.grants.grant_cache import GrantCache
from secrets_sdk.secret_uri import SecretURI, SecretURIError, parse as parse_uri
from secrets_sdk.services.secret_policy_service import SecretPolicyService
from secrets_sdk.vault_strategies.base_vault_strategy import BaseVaultStrategy
from secrets_sdk.vault_strategies.hashicorp_vault_strategy import HashiCorpVaultStrategy
from secrets_sdk.vault_strategies.openbao_vault_strategy import OpenBaoVaultStrategy


def _bool_env(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.lower() in ("true", "1", "yes")


class VaultClient:
    def __init__(self, *, enable_kafka: bool | None = None) -> None:
        self.cache = GrantCache(
            negative_ttl_s=int(os.getenv("NEGATIVE_CACHE_TTL_S", "5")),
            anti_replay_ttl_s=int(os.getenv("ANTI_REPLAY_TTL_S", "300")),
        )
        self.policy = SecretPolicyService()
        self.audit = AuditPublisher()
        self.expected_aud = os.getenv("SECRETS_AUDIENCE", "crud.secrets")
        # Provider selection (prefer OpenBao if URL env points there)
        allowed_mounts = [
            m.strip()
            for m in os.getenv("TENANT_ALLOWED_MOUNTS", "secret").split(",")
            if m.strip()
        ]
        cfg = {
            "url": os.getenv("VAULT_URL", "http://localhost:8200"),
            "token": os.getenv("VAULT_TOKEN"),
            "timeout": int(os.getenv("VAULT_TIMEOUT", "30")),
            "verify_ssl": _bool_env("VAULT_VERIFY_SSL", True),
            "skip_auth_check": _bool_env("VAULT_SKIP_AUTH_CHECK", False),
            "allowed_mounts": allowed_mounts,
        }
        url = (cfg["url"] or "").lower()
        if "openbao" in url:
            self.strategy: BaseVaultStrategy = OpenBaoVaultStrategy(cfg)
        elif "vault" in url or True:
            # default to HashiCorp-compatible
            self.strategy = HashiCorpVaultStrategy(cfg)

    async def get_credentials(self, canonical_uri: str, ctx: ExecutionContext | None = None) -> Dict[str, Any] | str:
        # Parse/normalize and tenant guard
        tenant_id = os.getenv("TENANT_ID", "dev")
        allowed_mounts = [m.strip() for m in (os.getenv("TENANT_ALLOWED_MOUNTS", "secret").split(",")) if m.strip()]
        try:
            uri = parse_uri(canonical_uri, tenant_id=tenant_id, allowed_mounts=allowed_mounts)  # type: ignore[arg-type]
        except SecretURIError:
            raise

        canonical = uri.to_canonical()
        subject = (ctx.subject if ctx else None) or "anonymous"
        cnf_binding = (ctx.cnf_jkt if ctx and ctx.cnf_jkt else (ctx.mtls_thumbprint if ctx else None))
        token_jti = ctx.token_jti if ctx else None
        audiences = set(ctx.aud or []) if ctx and ctx.aud else set()
        # Key grants ignoring binding so we can detect binding drift when a different
        # binding attempts to reuse an active grant.
        grant_key = (subject, tenant_id, canonical, "execute", None)

        # Negative cache quick deny
        if self.cache.is_negative(grant_key):
            raise AuthzDeniedError("SECRET_AUTHZ_FAILED")

        grant = self.cache.get(grant_key)
        if grant is None:
            # Audience check (if provided)
            if audiences and self.expected_aud not in audiences:
                self.cache.set_negative(grant_key)
                raise AuthzDeniedError("SECRET_AUTHZ_FAILED")
            # Anti-replay (if JTI provided)
            if token_jti and not self.cache.mark_jti(str(token_jti)):
                self.cache.set_negative(grant_key)
                raise AuthzDeniedError("SECRET_AUTHZ_FAILED")
            # PDP grant
            try:
                grant = await self.policy.authorize_use(subject, tenant_id, canonical, "execute", cnf_binding)
            except PermissionError as e:
                self.cache.set_negative(grant_key)
                raise AuthzDeniedError("DENY") from e
            except RuntimeError as e:
                self.cache.set_negative(grant_key)
                raise PDPUnavailableError("PDP_UNAVAILABLE") from e
            self.cache.put(grant_key, grant)
        else:
            # Enforce sender binding drift
            if grant.cnf_binding and cnf_binding and grant.cnf_binding != cnf_binding:
                self.cache.set_negative(grant_key)
                raise BindingDriftError("BINDING_DRIFT")

        # Grant use-count
        if not self.cache.increment_uses_atomically(grant_key):
            self.cache.set_negative(grant_key)
            raise AuthzDeniedError("SECRET_AUTHZ_FAILED")

        # Provider read; optional fragment unwrap happened in strategy
        return await self.strategy.get_credentials(canonical)

    def get_credentials_sync(self, canonical_uri: str, ctx: ExecutionContext | None = None) -> Dict[str, Any] | str:  # pragma: no cover - thin wrapper
        import asyncio

        return asyncio.get_event_loop().run_until_complete(self.get_credentials(canonical_uri, ctx))


