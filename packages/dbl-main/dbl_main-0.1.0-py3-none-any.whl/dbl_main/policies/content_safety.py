# content_safety.py
#
# Content safety policy.

from __future__ import annotations

from typing import Any, Callable, Mapping, Optional, Sequence

from dbl_core import BoundaryContext, PolicyDecision

from .base import Policy


class ContentSafetyPolicy(Policy):
    """
    Content safety policy.
    
    Checks if content in metadata passes safety rules.
    """
    
    def __init__(
        self,
        blocked_patterns: Optional[Sequence[str]] = None,
        content_key: str = "prompt",
        safety_checker: Optional[Callable[[str], bool]] = None,
    ) -> None:
        self._blocked_patterns = blocked_patterns or []
        self._content_key = content_key
        self._safety_checker = safety_checker
    
    @property
    def name(self) -> str:
        return "content-safety"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        """Check content safety."""
        
        content = context.metadata.get(self._content_key, "")
        
        if not content:
            return PolicyDecision(
                outcome="allow",
                reason="content-safety: no content to check",
                details={"policy": self.name},
            )
        
        # Check blocked patterns
        for pattern in self._blocked_patterns:
            if pattern.lower() in str(content).lower():
                return PolicyDecision(
                    outcome="block",
                    reason=f"content-safety: blocked pattern detected",
                    details={
                        "policy": self.name,
                        "pattern": pattern,
                    },
                )
        
        # Check with safety checker if provided
        if self._safety_checker is not None:
            is_safe = self._safety_checker(str(content))
            if not is_safe:
                return PolicyDecision(
                    outcome="block",
                    reason="content-safety: failed safety check",
                    details={"policy": self.name},
                )
        
        return PolicyDecision(
            outcome="allow",
            reason="content-safety: passed",
            details={"policy": self.name},
        )

