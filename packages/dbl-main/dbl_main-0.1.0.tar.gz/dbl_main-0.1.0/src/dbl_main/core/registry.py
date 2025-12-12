# registry.py
#
# Policy and pipeline registries.

from __future__ import annotations

from typing import Dict, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from ..policies.base import Policy
    from .pipeline import Pipeline


class PolicyRegistry:
    """Registry of available policies by name."""
    
    def __init__(self) -> None:
        self._policies: Dict[str, Type[Policy]] = {}
    
    def register(self, name: str, policy_class: Type[Policy]) -> None:
        """Register a policy class by name."""
        self._policies[name] = policy_class
    
    def get(self, name: str) -> Optional[Type[Policy]]:
        """Get a policy class by name."""
        return self._policies.get(name)
    
    def create(self, name: str, **kwargs) -> Optional[Policy]:
        """Create a policy instance by name."""
        policy_class = self._policies.get(name)
        if policy_class is None:
            return None
        return policy_class(**kwargs)
    
    def list_policies(self) -> list[str]:
        """List all registered policy names."""
        return list(self._policies.keys())


class PipelineRegistry:
    """Registry of pipelines by tenant/use-case."""
    
    def __init__(self) -> None:
        self._pipelines: Dict[str, Pipeline] = {}
    
    def register(self, key: str, pipeline: Pipeline) -> None:
        """Register a pipeline by key (e.g., 'tenant-1:api')."""
        self._pipelines[key] = pipeline
    
    def get(self, key: str) -> Optional[Pipeline]:
        """Get a pipeline by key."""
        return self._pipelines.get(key)
    
    def for_context(
        self,
        tenant_id: Optional[str] = None,
        channel: Optional[str] = None,
    ) -> Optional[Pipeline]:
        """Get pipeline for tenant/channel combination."""
        if tenant_id and channel:
            key = f"{tenant_id}:{channel}"
            if key in self._pipelines:
                return self._pipelines[key]
        
        if tenant_id:
            key = f"{tenant_id}:default"
            if key in self._pipelines:
                return self._pipelines[key]
        
        return self._pipelines.get("default")

