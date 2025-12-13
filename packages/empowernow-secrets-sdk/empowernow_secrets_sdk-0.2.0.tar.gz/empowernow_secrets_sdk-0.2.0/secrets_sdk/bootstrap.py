"""Bootstrap loader for CSI-mounted or env-configured credentials."""
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BootstrapConfig:
    """Configuration for vault connection."""

    vault_addr: str
    auth_method: str  # "kubernetes" | "approle" | "token"

    # Kubernetes auth
    kubernetes_role: Optional[str] = None
    kubernetes_mount: str = "kubernetes"
    service_account_token_path: str = "/var/run/secrets/kubernetes.io/serviceaccount/token"

    # AppRole auth
    approle_role_id: Optional[str] = None
    approle_secret_id: Optional[str] = None
    approle_mount: str = "approle"

    # Token auth (dev/Docker)
    token: Optional[str] = None
    token_file: Optional[str] = None

    # TLS
    ca_cert_path: Optional[str] = None
    skip_verify: bool = False  # DEV/TEST ONLY - disables TLS verification


def _validate_bootstrap_config(data: dict, source: str) -> None:
    """
    Validate bootstrap config has required fields for auth method.

    Args:
        data: Bootstrap configuration dictionary
        source: Source path/location for error messages

    Raises:
        ValueError: If required fields are missing for the auth method
    """
    auth_method = data.get("auth_method", "token")

    if auth_method == "kubernetes":
        if not data.get("kubernetes_role"):
            raise ValueError(
                f"Invalid bootstrap config at {source}: "
                f"auth_method='kubernetes' requires 'kubernetes_role' field"
            )

    elif auth_method == "approle":
        if not data.get("approle_role_id") or not data.get("approle_secret_id"):
            raise ValueError(
                f"Invalid bootstrap config at {source}: "
                f"auth_method='approle' requires 'approle_role_id' and 'approle_secret_id'"
            )

    elif auth_method == "token":
        if not data.get("token") and not data.get("token_file"):
            raise ValueError(
                f"Invalid bootstrap config at {source}: "
                f"auth_method='token' requires either 'token' or 'token_file'"
            )


def load_bootstrap(path: Optional[str] = None) -> BootstrapConfig:
    """
    Load bootstrap config with fallback chain.

    Precedence (first found wins):
    1. Explicit path parameter
    2. SECRETS_BOOTSTRAP_PATH environment variable
    3. /vault/secrets/bootstrap.json (Kubernetes CSI mount)
    4. Environment variables (OPENBAO_* or VAULT_*)

    Environment Variable Naming:
    - OPENBAO_* variables are checked first (preferred)
    - VAULT_* variables are fallback for backward compatibility

    Validation Rules:
    - auth_method="kubernetes" requires: kubernetes_role
    - auth_method="approle" requires: approle_role_id AND approle_secret_id
    - auth_method="token" requires: token OR token_file

    Args:
        path: Explicit path to bootstrap.json (optional)

    Returns:
        BootstrapConfig with vault connection parameters

    Raises:
        FileNotFoundError: If no config found via any source
        ValueError: If config invalid (malformed JSON, missing required fields)
    """
    # Try file-based config first
    if path is None:
        path = os.getenv("SECRETS_BOOTSTRAP_PATH")

    if path is None:
        default_path = Path("/vault/secrets/bootstrap.json")
        if default_path.exists():
            path = str(default_path)

    if path and Path(path).exists():
        logger.info("Loading bootstrap config from file: %s", path)
        try:
            data = json.loads(Path(path).read_text())
        except json.JSONDecodeError as e:
            logger.error("Failed to parse bootstrap JSON at %s: %s", path, e)
            raise ValueError(f"Invalid bootstrap config at {path}: JSON parse error: {e}") from e

        try:
            _validate_bootstrap_config(data, path)
            vault_addr = data["vault_addr"]
        except KeyError as e:
            raise ValueError(f"Invalid bootstrap config at {path}: missing required field {e}") from e

        logger.info("Loaded bootstrap: auth_method=%s, vault_addr=%s",
                    data.get("auth_method", "token"), vault_addr)

        return BootstrapConfig(
            vault_addr=vault_addr,
            auth_method=data.get("auth_method", "token"),
            kubernetes_role=data.get("kubernetes_role"),
            approle_role_id=data.get("approle_role_id"),
            approle_secret_id=data.get("approle_secret_id"),
            token=data.get("token"),
            token_file=data.get("token_file"),
            ca_cert_path=data.get("ca_cert_path"),
            skip_verify=data.get("skip_verify", False),
        )

    # Fallback to environment variables (Docker Compose pattern)
    logger.info("No bootstrap file found, falling back to environment variables")
    vault_addr = os.getenv("OPENBAO_URL") or os.getenv("VAULT_URL")
    if not vault_addr:
        logger.error("No bootstrap config found via file or environment variables")
        raise FileNotFoundError(
            "No bootstrap config found. Set SECRETS_BOOTSTRAP_PATH, "
            "mount /vault/secrets/bootstrap.json, or set OPENBAO_URL env var."
        )

    token_file = os.getenv("OPENBAO_TOKEN_FILE") or os.getenv("VAULT_TOKEN_FILE")
    token = os.getenv("OPENBAO_TOKEN") or os.getenv("VAULT_TOKEN")

    logger.info("Loaded bootstrap from env: vault_addr=%s, auth_method=token", vault_addr)

    return BootstrapConfig(
        vault_addr=vault_addr,
        auth_method="token",
        token=token,
        token_file=token_file,
    )
