# rate_limit.py
#
# Rate limit policy.

from __future__ import annotations

from typing import Any, Mapping, Optional

from dbl_core import BoundaryContext, PolicyDecision

from .base import Policy


class RateLimitPolicy(Policy):
    """
    Rate limit policy.
    
    Checks if caller has exceeded request limits.
    """
    
    def __init__(
        self,
        max_requests: int = 100,
        window_seconds: int = 60,
        rate_checker: Optional[callable] = None,
    ) -> None:
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._rate_checker = rate_checker
    
    @property
    def name(self) -> str:
        return "rate-limit"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        """Check rate limit for caller."""
        
        # If no rate checker provided, allow
        if self._rate_checker is None:
            return PolicyDecision(
                outcome="allow",
                reason="rate-limit: no checker configured",
                details={"policy": self.name, "max_requests": self._max_requests},
            )
        
        caller_id = context.caller_id or "anonymous"
        current_count = self._rate_checker(caller_id, self._window_seconds)
        
        if current_count >= self._max_requests:
            return PolicyDecision(
                outcome="block",
                reason=f"rate-limit: exceeded {self._max_requests} requests in {self._window_seconds}s",
                details={
                    "policy": self.name,
                    "caller_id": caller_id,
                    "current_count": current_count,
                    "max_requests": self._max_requests,
                },
            )
        
        return PolicyDecision(
            outcome="allow",
            reason="rate-limit: within limits",
            details={
                "policy": self.name,
                "caller_id": caller_id,
                "current_count": current_count,
                "max_requests": self._max_requests,
            },
        )

