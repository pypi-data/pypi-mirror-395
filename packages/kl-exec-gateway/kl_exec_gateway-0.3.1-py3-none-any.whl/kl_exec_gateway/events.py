# src/kl_exec_gateway/events.py

from __future__ import annotations

import logging
from collections import deque
from threading import Lock
from typing import Deque, Iterable

from .models import GatewayTrace


class EventStore:
    """
    Minimal in-memory event store for GatewayTrace objects.

    This is used to feed the insight panel UI on the right side.
    """

    def __init__(self, maxlen: int = 500) -> None:
        self._events: Deque[GatewayTrace] = deque(maxlen=maxlen)
        self._lock = Lock()
        self.logger = logging.getLogger(__name__)

    def add(self, trace: GatewayTrace) -> None:
        with self._lock:
            self._events.appendleft(trace)

        # Log event for monitoring
        self.logger.info(
            "Event added to store",
            extra={
                "trace_id": trace.trace_id,
                "policy_allowed": trace.policy_decision.allowed,
                "policy_code": trace.policy_decision.code,
            },
        )

    def list_recent(self, limit: int = 50) -> Iterable[GatewayTrace]:
        with self._lock:
            return list(list(self._events)[:limit])
