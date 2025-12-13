from __future__ import annotations

import asyncio
import random
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Dict, Optional, Tuple


GrantKey = Tuple[str, str, str, str, Optional[str]]


@dataclass
class Grant:
    grant_id: str
    ttl_s: int
    max_uses: int
    uses: int
    decision_id: str
    policy_version: str
    classification: Optional[str]
    must_revalidate_on: Optional[str]  # "node" or None
    cnf_binding: Optional[str] = None
    wrap_ttl: Optional[str] = None


class GrantCache:
    def __init__(
        self,
        negative_ttl_s: int = 5,
        anti_replay_ttl_s: int = 300,
        jitter_ms: int = 500,
        monotonic_fn=time.monotonic,
    ) -> None:
        self._grants: Dict[GrantKey, Tuple[Grant, float]] = {}
        self._negatives: Dict[GrantKey, float] = {}
        self._replay: Dict[str, float] = {}
        self._locks: Dict[GrantKey, asyncio.Lock] = {}
        self._negative_ttl_s = negative_ttl_s
        self._anti_replay_ttl_s = anti_replay_ttl_s
        self._jitter_ms = jitter_ms
        self._now = monotonic_fn

    def _expired(self, expires_at: float) -> bool:
        return self._now() >= expires_at

    def _deadline(self, ttl_s: int, with_jitter: bool = False) -> float:
        base = self._now() + float(ttl_s)
        if with_jitter and self._jitter_ms > 0:
            base += random.randint(0, self._jitter_ms) / 1000.0
        return base

    def get(self, key: GrantKey) -> Optional[Grant]:
        entry = self._grants.get(key)
        if not entry:
            return None
        grant, exp = entry
        if self._expired(exp):
            self._grants.pop(key, None)
            return None
        return grant

    def put(self, key: GrantKey, grant: Grant) -> None:
        exp = self._deadline(grant.ttl_s)
        self._grants[key] = (grant, exp)
        self._negatives.pop(key, None)

    def increment_uses_atomically(self, key: GrantKey) -> bool:
        entry = self._grants.get(key)
        if not entry:
            return False
        grant, exp = entry
        if self._expired(exp):
            self._grants.pop(key, None)
            return False
        new_uses = grant.uses + 1
        if new_uses > max(1, grant.max_uses):
            return False
        grant.uses = new_uses
        self._grants[key] = (grant, exp)
        return True

    def set_negative(self, key: GrantKey, ttl_s: Optional[int] = None) -> None:
        ttl = ttl_s if ttl_s is not None else self._negative_ttl_s
        self._negatives[key] = self._deadline(ttl, with_jitter=True)

    def is_negative(self, key: GrantKey) -> bool:
        exp = self._negatives.get(key)
        if exp is None:
            return False
        if self._expired(exp):
            self._negatives.pop(key, None)
            return False
        return True

    def mark_jti(self, jti: str) -> bool:
        exp = self._replay.get(jti)
        if exp and not self._expired(exp):
            return False
        self._replay[jti] = self._deadline(self._anti_replay_ttl_s)
        return True

    @asynccontextmanager
    async def lock(self, key: GrantKey):
        lock = self._locks.get(key)
        if lock is None:
            lock = asyncio.Lock()
            self._locks[key] = lock
        async with lock:
            yield


