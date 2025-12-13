from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ExecutionContext:
    subject: Optional[str] = None
    aud: Optional[List[str]] = None
    token_jti: Optional[str] = None
    cnf_jkt: Optional[str] = None
    mtls_thumbprint: Optional[str] = None
    issuer: Optional[str] = None
    client_id: Optional[str] = None
    correlation_id: Optional[str] = None
    workflow_run_id: Optional[str] = None
    node_id: Optional[str] = None
    system_id: Optional[str] = None

    @staticmethod
    def from_fastapi_request(request: Any) -> "ExecutionContext":  # pragma: no cover - framework adapter
        state = getattr(request, "state", None)
        get = lambda k: getattr(state, k, None) if state is not None else None
        aud = get("aud")
        aud_list = list(aud) if isinstance(aud, (list, tuple, set)) else ([aud] if isinstance(aud, str) else None)
        return ExecutionContext(
            subject=get("subject"),
            aud=aud_list,
            token_jti=get("token_jti"),
            cnf_jkt=get("cnf_jkt"),
            mtls_thumbprint=get("mtls_thumbprint"),
            issuer=get("issuer"),
            client_id=get("client_id") or get("azp"),
            correlation_id=get("correlation_id"),
            workflow_run_id=get("workflow_run_id"),
            node_id=get("node_id"),
            system_id=get("system_id"),
        )

    @staticmethod
    def from_headers(headers: Dict[str, str]) -> "ExecutionContext":
        return ExecutionContext(
            subject=headers.get("x-subject"),
            aud=headers.get("x-aud").split(",") if headers.get("x-aud") else None,
            token_jti=headers.get("x-jti"),
            cnf_jkt=headers.get("x-cnf-jkt"),
            mtls_thumbprint=headers.get("x-mtls-thumbprint"),
            issuer=headers.get("x-issuer"),
            client_id=headers.get("x-client-id"),
            correlation_id=headers.get("x-correlation-id"),
        )


