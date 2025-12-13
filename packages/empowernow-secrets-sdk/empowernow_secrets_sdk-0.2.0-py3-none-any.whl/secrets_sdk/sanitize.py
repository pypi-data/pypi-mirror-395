from __future__ import annotations

from typing import Dict, Iterable


SENSITIVE_DEFAULT: set[str] = {
    "authorization",
    "x-downstream-password",
    "x-api-key",
    "password",
    "token",
    "secret",
}


def redact_dict(headers: Dict[str, str], sensitive_keys: Iterable[str] | None = None) -> Dict[str, str]:
    """Return a copy with sensitive values redacted for logging/metrics.

    This function never mutates the input mapping.
    """
    keys = set(sensitive_keys) if sensitive_keys is not None else SENSITIVE_DEFAULT
    out: Dict[str, str] = {}
    for k, v in headers.items():
        if k.lower() in keys:
            out[k] = "<redacted>"
        else:
            out[k] = v
    return out


