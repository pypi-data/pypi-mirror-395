from __future__ import annotations

import os
from typing import Any, Dict, Optional


class AuditPublisher:
    def __init__(self) -> None:
        self.enabled = os.getenv("ENABLE_KAFKA_PRODUCER", "false").lower() in ("true", "1", "yes")
        self.sample_n = max(1, int(os.getenv("AUDIT_SAMPLE_CACHE_HIT_N", "1")))
        self._counter = 0

    async def publish_secret_event(self, event_type: str, data: Dict[str, Any]) -> None:  # pragma: no cover - no-op by default
        if not self.enabled:
            return
        # Placeholder for platform producer integration. Intentionally a no-op here.
        return

    def should_emit_cache_hit(self) -> bool:
        if self.sample_n <= 1:
            return True
        self._counter += 1
        if self._counter >= self.sample_n:
            self._counter = 0
            return True
        return False


