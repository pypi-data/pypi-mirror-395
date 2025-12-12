# context_builder.py
#
# Helper for building BoundaryContext from request data.

from __future__ import annotations

from typing import Any, Mapping, Optional

from dbl_core import BoundaryContext
from kl_kernel_logic import PsiDefinition


class ContextBuilder:
    """
    Helper class for building BoundaryContext from request data.
    """
    
    def __init__(self) -> None:
        self._defaults: dict[str, Any] = {}
    
    def set_defaults(self, **kwargs) -> None:
        """Set default values for context fields."""
        self._defaults.update(kwargs)
    
    def build(
        self,
        psi: PsiDefinition,
        caller_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        channel: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> BoundaryContext:
        """Build a BoundaryContext from the given parameters."""
        return BoundaryContext(
            psi=psi,
            caller_id=caller_id or self._defaults.get("caller_id"),
            tenant_id=tenant_id or self._defaults.get("tenant_id"),
            channel=channel or self._defaults.get("channel"),
            metadata=metadata or {},
        )
    
    def from_request(
        self,
        psi_type: str,
        psi_name: str,
        caller_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        channel: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> BoundaryContext:
        """Build a BoundaryContext from raw request data."""
        psi = PsiDefinition(psi_type=psi_type, name=psi_name)
        return self.build(
            psi=psi,
            caller_id=caller_id,
            tenant_id=tenant_id,
            channel=channel,
            metadata=metadata,
        )

