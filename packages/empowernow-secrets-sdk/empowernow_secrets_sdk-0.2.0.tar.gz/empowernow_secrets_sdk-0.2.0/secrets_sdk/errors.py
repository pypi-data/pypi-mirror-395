from __future__ import annotations

from typing import Literal


class SecretURIError(Exception):
    """Raised for canonical Secret URI validation/normalization failures."""

    INVALID_WILDCARD: Literal["INVALID_WILDCARD"] = "INVALID_WILDCARD"
    ILLEGAL_SEGMENT: Literal["ILLEGAL_SEGMENT"] = "ILLEGAL_SEGMENT"
    TENANT_MOUNT_MISMATCH: Literal["TENANT_MOUNT_MISMATCH"] = "TENANT_MOUNT_MISMATCH"
    UNSUPPORTED_ENGINE: Literal["UNSUPPORTED_ENGINE"] = "UNSUPPORTED_ENGINE"
    AMBIGUOUS_MOUNT: Literal["AMBIGUOUS_MOUNT"] = "AMBIGUOUS_MOUNT"
    AMBIGUOUS_QUERY: Literal["AMBIGUOUS_QUERY"] = "AMBIGUOUS_QUERY"
    DOUBLE_MOUNT_SOURCE: Literal["DOUBLE_MOUNT_SOURCE"] = "DOUBLE_MOUNT_SOURCE"
    PROVIDER_TRAILING_SLASH_MISMATCH: Literal["PROVIDER_TRAILING_SLASH_MISMATCH"] = (
        "PROVIDER_TRAILING_SLASH_MISMATCH"
    )

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code: str = code


class AuthzDeniedError(Exception):
    pass


class PDPUnavailableError(Exception):
    pass


class BindingDriftError(Exception):
    pass


class ProviderError(Exception):
    pass


