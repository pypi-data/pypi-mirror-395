from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from secrets_sdk.grants.grant_cache import Grant


class SecretPolicyService:
    """Minimal PDP facade for dev/embedded usage.

    Production deployments can swap this class with a real PDP client while keeping
    the same return type and behavior contract.
    """

    def __init__(self) -> None:
        self.default_ttl = int(os.getenv("GRANT_TTL_DEFAULT", "300"))
        self.default_max_uses = int(os.getenv("GRANT_MAX_USES_DEFAULT", "1"))
        self.pdp_available = os.getenv("PDP_AVAILABLE", "true").lower() in ("true", "1", "yes")
        enable_flag = os.getenv("ENABLE_AUTHORIZATION")
        if enable_flag is not None:
            self.enable_authorization = enable_flag.lower() in ("true", "1", "yes")
        else:
            # Default safe-off for dev if no explicit configuration
            self.enable_authorization = False

    async def authorize_use(
        self,
        subject_arn: str,
        tenant_id: str,
        canonical_uri: str,
        purpose: str | None,
        cnf_binding: str | None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Grant:
        if self.enable_authorization:
            if not self.pdp_available:
                raise RuntimeError("PDP_UNAVAILABLE")
            if "deny" in canonical_uri:
                raise PermissionError("DENY")
        wrap_ttl = None
        if context and isinstance(context, dict):
            wrap_ttl = context.get("wrap_ttl")
        return Grant(
            grant_id=str(uuid.uuid4()),
            ttl_s=self.default_ttl,
            max_uses=self.default_max_uses,
            uses=0,
            decision_id=str(uuid.uuid4()),
            policy_version="local-dev",
            classification=None,
            must_revalidate_on=None,
            cnf_binding=cnf_binding,
            wrap_ttl=wrap_ttl,  # type: ignore[arg-type]
        )

    @dataclass
    class BatchFailure:
        uri: str
        code: str  # "DENY" | "PDP_UNAVAILABLE" | other
        reason: str

    async def authorize_batch(
        self,
        subject_arn: str,
        tenant_id: str,
        required: List[str],
        optional: List[str] | None = None,
        *,
        purpose: str | None = None,
        cnf_binding: str | None = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, Grant], List[BatchFailure]]:
        optional = optional or []
        # De-duplicate keeping first occurrence preference (required first)
        seen: set[str] = set()
        ordered: List[Tuple[str, bool]] = []
        for uri in required:
            if uri not in seen:
                seen.add(uri)
                ordered.append((uri, True))
        for uri in optional:
            if uri not in seen:
                seen.add(uri)
                ordered.append((uri, False))

        grants: Dict[str, Grant] = {}
        failures: List[SecretPolicyService.BatchFailure] = []
        for uri, _is_required in ordered:
            try:
                g = await self.authorize_use(subject_arn, tenant_id, uri, purpose, cnf_binding, context=context)
                grants[uri] = g
            except PermissionError:
                failures.append(SecretPolicyService.BatchFailure(uri=uri, code="DENY", reason="policy"))
            except RuntimeError:
                failures.append(SecretPolicyService.BatchFailure(uri=uri, code="PDP_UNAVAILABLE", reason="unavailable"))
        return grants, failures


