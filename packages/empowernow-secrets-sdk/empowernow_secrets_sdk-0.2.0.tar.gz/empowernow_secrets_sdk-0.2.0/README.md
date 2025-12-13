## Secrets SDK (Python)

### Overview
Secrets SDK provides two client interfaces for resolving Canonical Secret URIs:

**SecretsClient** - Direct vault access for service configuration:
- File-based bootstrap (solves chicken-egg problem)
- Provider routing: `file://`, `openbao+kv2://`, `hashicorp+kv2://`
- Memory caching with TTL
- Lazy authentication (auth on first vault access)

**VaultClient** - PDP-enforced access for multi-tenant operations:
- Canonical URI parsing and tenant-mount guard
- PEP grants with sender-binding, anti-replay, and negative caching
- Provider strategies for OpenBao/HashiCorp KVv2 (version-pinned reads, deleted/destroyed typing)
- Optional non-leaky audits using short `resource_ref`

### Design goals
- Strong typing and small public API surface
- Minimal required configuration; sensible defaults
- No plaintext secret leakage (logs/metrics/OTEL)

Non-goals
- Managing secret values at rest (creation/rotation workflows live in services that own policy)
- Exposing HTTP routes (that's CRUDService's role)

---

## Architecture

```
secrets_sdk/
  __init__.py                # Exports: SecretsClient, SecretURI, BootstrapConfig
  client.py                  # SecretsClient - direct vault access
  bootstrap.py               # BootstrapConfig, load_bootstrap()
  context.py                 # ExecutionContext helpers
  errors.py                  # Typed exceptions
  secret_uri.py              # Canonical URI parser/normalizer
  audit.py                   # Pluggable audit publisher (Kafka/no-op)
  vault_client.py            # VaultClient - PDP-enforced access
  grants/
    grant_cache.py           # In-memory grants, negative cache, anti-replay
  services/
    secret_policy_service.py # PDP facade
  vault_strategies/
    base_vault_strategy.py
    openbao_vault_strategy.py
    hashicorp_vault_strategy.py
```

### Public API

```python
# SecretsClient - service config (no PDP)
class SecretsClient:
    @classmethod
    def create(cls, bootstrap_path: str | None = None, ...) -> "SecretsClient": ...
    async def resolve(self, uri: str, *, refresh: bool = False) -> Any: ...
    async def close(self) -> None: ...

# VaultClient - request handling (PDP-enforced)
class VaultClient:
    def __init__(self, *, enable_kafka: bool | None = None) -> None: ...
    async def get_credentials(self, canonical_uri: str, ctx: ExecutionContext | None = None) -> dict | str: ...
    def get_credentials_sync(self, canonical_uri: str, ctx: ExecutionContext | None = None) -> dict | str: ...

class ExecutionContext:
    subject: str | None
    aud: list[str] | None
    token_jti: str | None
    cnf_jkt: str | None
    mtls_thumbprint: str | None
    @staticmethod
    def from_fastapi_request(request) -> "ExecutionContext": ...
    @staticmethod
    def from_headers(headers: dict[str, str]) -> "ExecutionContext": ...
```

### VaultClient Behavior (PEP flow)
1. Parse → Canonicalize → Tenant mount guard
2. Build grant key `(subject, tenant_id, canonical_uri, "execute", cnf_binding)`
3. Check negative cache; fetch/issue grant via `SecretPolicyService` on miss
4. Enforce audience (`SECRETS_AUDIENCE`), JTI anti-replay, sender binding drift
5. Increment grant uses atomically; on exceed → deny
6. Provider read (KVv2 with optional `version=`); map deleted/destroyed to typed errors
7. Publish non-leaky audit (if enabled)

---

## Configuration

### SecretsClient
Required:
- `OPENBAO_URL` or `VAULT_URL`
- `SECRETS_ALLOWED_MOUNTS` (comma list)

Optional:
- `OPENBAO_TOKEN` / `VAULT_TOKEN` (dev)
- `FILE_MOUNT_PATH` (default `/run/secrets`)
- `SECRETS_BOOTSTRAP_PATH`

### VaultClient
Required:
- `VAULT_URL`, `VAULT_TOKEN`, `TENANT_ID`, `TENANT_ALLOWED_MOUNTS`
- `SECRET_TENANT_SALT` (HMAC key for `resource_ref`)

Optional:
- `VAULT_TIMEOUT` (default 30), `VAULT_VERIFY_SSL` (default true)
- `GRANT_TTL_DEFAULT` (default 300), `GRANT_MAX_USES_DEFAULT` (default 1)
- `NEGATIVE_CACHE_TTL_S` (default 5), `ANTI_REPLAY_TTL_S` (default 300)
- `SECRETS_AUDIENCE` (default `crud.secrets`)
- Audits: `ENABLE_KAFKA_PRODUCER`, `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC_PREFIX`

### Dependencies
```toml
dependencies = ["tenacity", "cachetools", "httpx", "opentelemetry-api"]
```

---

## Usage

### SecretsClient
```python
from secrets_sdk import SecretsClient

client = SecretsClient.create()

# Sync resolution (config loading, file:// only)
db_url = client.resolve_file_sync("file://primary/db-conn-string")

# Async resolution (runtime, all providers)
ldap = await client.resolve("file://dc-credentials/ldap.json")
token = await client.resolve("openbao+kv2://secret/app/api#token")

await client.close()
```

### VaultClient (FastAPI)
```python
from secrets_sdk.vault_client import VaultClient
from secrets_sdk.context import ExecutionContext

client = VaultClient()

async def handler(request):
    ctx = ExecutionContext.from_fastapi_request(request)
    payload = await client.get_credentials("openbao+kv2://secret/myapp/api#token?version=3", ctx)
    return payload["token"]
```

### VaultClient (Sync)
```python
token = VaultClient().get_credentials_sync("openbao+kv2://secret/app/api#token", ctx=None)
```

---

## Errors
```python
from secrets_sdk import SecretURIError
from secrets_sdk.errors import AuthzDeniedError, PDPUnavailableError, BindingDriftError
from secrets_sdk.vault_strategies.errors import (
    VaultSecretNotFoundError,
    VaultSecretVersionDeletedError,
    VaultSecretVersionDestroyedError,
)
```

---

## Testing
Mock `_read_secret_kvv2` for vault strategy tests:
```python
with patch.object(strategy, "_read_secret_kvv2", new_callable=AsyncMock) as mock:
    mock.return_value = {"data": {"data": {"token": "test"}, "metadata": {"version": 1}}}
    result = await strategy.get_credentials("openbao+kv2://secret/app#token")
```

CI: set `VAULT_SKIP_AUTH_CHECK=true` to bypass auth check (tests only).

---

## Build & Test
```bash
pip install -e .[dev]
pytest -q
```

See `docs/` for detailed guides.
