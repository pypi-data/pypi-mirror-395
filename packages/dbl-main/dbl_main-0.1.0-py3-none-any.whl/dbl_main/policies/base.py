# base.py
#
# Policy interface.

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping

from dbl_core import BoundaryContext, PolicyDecision


class Policy(ABC):
    """
    Abstract base for all policies.
    
    Each policy evaluates a BoundaryContext and returns a PolicyDecision.
    """
    
    @abstractmethod
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        """Evaluate the context and return a decision."""
        ...
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Policy name for logging and audit."""
        ...
    
    def describe(self) -> Mapping[str, Any]:
        """Return policy metadata for audit."""
        return {"name": self.name}

