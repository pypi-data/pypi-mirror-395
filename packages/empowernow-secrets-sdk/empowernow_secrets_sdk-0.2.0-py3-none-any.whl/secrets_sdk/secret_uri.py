from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .errors import SecretURIError


_ALLOWED_PROVIDERS = {"openbao", "hashicorp", "db", "bootstrap", "file", "yaml"}
_ALLOWED_ENGINES_BY_PROVIDER = {
    "openbao": {"kv2"},
    "hashicorp": {"kv2"},
    "db": {"cred", "db"},
    "bootstrap": set(),
    "file": set(),
    "yaml": set(),
}

_SEGMENT_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")


@dataclass(frozen=True)
class SecretURI:
    provider: str
    engine: Optional[str]
    mount: str
    path_segments: Tuple[str, ...]
    fragment_key: Optional[str]
    params: Tuple[Tuple[str, str], ...]
    original: str

    def to_canonical(self) -> str:
        scheme = self.provider if self.engine is None else f"{self.provider}+{self.engine}"
        path = "/".join((self.mount, *self.path_segments))
        canonical = f"{scheme}://{path}"
        if self.fragment_key:
            canonical += f"#{self.fragment_key}"
        if self.params:
            qp = "&".join([f"{k}={v}" for k, v in self.params])
            canonical += f"?{qp}"
        return canonical


def _split_once(s: str, sep: str) -> Tuple[str, Optional[str]]:
    idx = s.find(sep)
    if idx == -1:
        return s, None
    return s[:idx], s[idx + 1 :]


def _validate_and_split_scheme(pointer: str) -> Tuple[str, Optional[str], str]:
    if "://" not in pointer:
        raise SecretURIError(SecretURIError.ILLEGAL_SEGMENT, "Missing scheme delimiter ://")
    scheme, rest = pointer.split("://", 1)
    if not scheme:
        raise SecretURIError(SecretURIError.ILLEGAL_SEGMENT, "Empty scheme")
    scheme = scheme.lower()
    if "+" in scheme:
        provider, engine = _split_once(scheme, "+")
    else:
        provider, engine = scheme, None
    if provider not in _ALLOWED_PROVIDERS:
        raise SecretURIError(SecretURIError.UNSUPPORTED_ENGINE, f"Unsupported provider: {provider}")
    if engine:
        allowed = _ALLOWED_ENGINES_BY_PROVIDER.get(provider, set())
        if engine not in allowed:
            raise SecretURIError(SecretURIError.UNSUPPORTED_ENGINE, f"Unsupported engine {engine} for {provider}")
    return provider, engine, rest


def _parse_fragment_and_query(rest: str) -> Tuple[str, Optional[str], Dict[str, str]]:
    path_and_frag, query = _split_once(rest, "?")
    path_only, frag = _split_once(path_and_frag, "#")
    if frag and "#" in frag:
        raise SecretURIError(SecretURIError.ILLEGAL_SEGMENT, "Multiple fragments not allowed")
    params: Dict[str, str] = {}
    if query:
        for pair in query.split("&"):
            if not pair:
                continue
            if "=" not in pair:
                k, v = pair, ""
            else:
                k, v = pair.split("=", 1)
            if k in params:
                raise SecretURIError(SecretURIError.AMBIGUOUS_QUERY, f"Duplicate query key: {k}")
            params[k] = v
    if "mount" in params:
        raise SecretURIError(SecretURIError.DOUBLE_MOUNT_SOURCE, "Mount must not be provided via query")
    return path_only, frag, params


def _validate_path_and_segments(path: str) -> List[str]:
    lowered = path.lower()
    if "%2f" in lowered or ".." in path:
        raise SecretURIError(SecretURIError.ILLEGAL_SEGMENT, "Forbidden encoding or traversal in path")
    if path.endswith("/"):
        path = path[:-1]
    segments = path.split("/") if path else []
    if any(seg == "" for seg in segments):
        raise SecretURIError(SecretURIError.ILLEGAL_SEGMENT, "Empty path segment (duplicate slashes)")
    if not segments:
        raise SecretURIError(SecretURIError.ILLEGAL_SEGMENT, "Missing mount segment")
    for seg in segments:
        if "*" in seg:
            raise SecretURIError(SecretURIError.INVALID_WILDCARD, "Wildcard not allowed in path")
        if not _SEGMENT_PATTERN.match(seg):
            raise SecretURIError(SecretURIError.ILLEGAL_SEGMENT, f"Illegal characters in segment: {seg}")
    return segments


def parse(pointer: str, tenant_id: str, allowed_mounts: List[str]) -> SecretURI:
    provider, engine, rest = _validate_and_split_scheme(pointer)
    path_only, frag, params = _parse_fragment_and_query(rest)
    segments = _validate_path_and_segments(path_only)
    mount, tail = segments[0], segments[1:]
    if allowed_mounts and mount not in set(allowed_mounts):
        raise SecretURIError(
            SecretURIError.TENANT_MOUNT_MISMATCH,
            f"Mount '{mount}' not allowed for tenant {tenant_id}",
        )
    sorted_params = tuple(sorted(params.items(), key=lambda kv: kv[0]))
    return SecretURI(
        provider=provider,
        engine=engine,
        mount=mount,
        path_segments=tuple(tail),
        fragment_key=frag,
        params=sorted_params,
        original=pointer,
    )


