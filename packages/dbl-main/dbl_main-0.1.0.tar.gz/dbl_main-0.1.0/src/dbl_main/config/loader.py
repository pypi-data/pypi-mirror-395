# loader.py
#
# Configuration loading for DBL Main.

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from ..core.pipeline import Pipeline


@dataclass
class PipelineConfig:
    """Configuration for a single pipeline."""
    
    name: str
    policies: Sequence[str] = field(default_factory=list)
    enabled: bool = True


@dataclass
class TenantConfig:
    """Configuration for a tenant."""
    
    tenant_id: str
    pipelines: Mapping[str, PipelineConfig] = field(default_factory=dict)
    defaults: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class Config:
    """Loaded configuration."""
    
    pipelines: Mapping[str, Any] = field(default_factory=dict)
    policies: Mapping[str, Any] = field(default_factory=dict)
    tenants: Mapping[str, Any] = field(default_factory=dict)


def load_config(path: str) -> Config:
    """
    Load configuration from a directory.
    
    Expects:
    - path/pipelines.yaml or path/pipelines.json
    - path/policies.yaml or path/policies.json
    - path/tenants/*.yaml or path/tenants/*.json
    """
    config_path = Path(path)
    
    pipelines = _load_file(config_path / "pipelines")
    policies = _load_file(config_path / "policies")
    
    tenants = {}
    tenants_path = config_path / "tenants"
    if tenants_path.exists():
        for f in tenants_path.iterdir():
            if f.suffix in (".json", ".yaml", ".yml"):
                tenant_id = f.stem
                tenants[tenant_id] = _load_file(f.with_suffix(""))
    
    return Config(
        pipelines=pipelines.get("pipelines", {}),
        policies=policies.get("policies", {}),
        tenants=tenants,
    )


def _load_file(path: Path) -> Mapping[str, Any]:
    """Load a JSON or YAML file."""
    json_path = path.with_suffix(".json")
    yaml_path = path.with_suffix(".yaml")
    yml_path = path.with_suffix(".yml")
    
    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)
    
    # YAML support requires pyyaml
    for yp in (yaml_path, yml_path):
        if yp.exists():
            try:
                import yaml
                with open(yp, "r") as f:
                    return yaml.safe_load(f) or {}
            except ImportError:
                raise ImportError("pyyaml required for YAML config files")
    
    return {}


def get_default_policy_registry() -> PolicyRegistry:
    """Get the default policy registry with built-in policies."""
    from ..core.registry import PolicyRegistry
    from ..policies.rate_limit import RateLimitPolicy
    from ..policies.content_safety import ContentSafetyPolicy
    
    registry = PolicyRegistry()
    registry.register("rate-limit", RateLimitPolicy)
    registry.register("content-safety", ContentSafetyPolicy)
    return registry


class PolicyRegistry:
    """Registry of policy classes by name."""
    
    def __init__(self) -> None:
        self._policies: dict[str, type] = {}
    
    def register(self, name: str, policy_class: type) -> None:
        self._policies[name] = policy_class
    
    def create(self, name: str, **kwargs) -> Any:
        policy_class = self._policies.get(name)
        if policy_class is None:
            return None
        return policy_class(**kwargs)
    
    def list_policies(self) -> list[str]:
        return list(self._policies.keys())


def build_pipeline_for(
    cfg: Config,
    tenant_id: Optional[str] = None,
    use_case: Optional[str] = None,
    registry: Optional[PolicyRegistry] = None,
) -> Pipeline:
    """
    Build a pipeline from configuration.
    
    Looks up pipeline by tenant/use_case, falls back to 'default'.
    Uses the provided registry or creates a default one.
    """
    from ..core.pipeline import Pipeline
    from ..policies.rate_limit import RateLimitPolicy
    from ..policies.content_safety import ContentSafetyPolicy
    
    # Use provided registry or create default
    if registry is None:
        registry = PolicyRegistry()
        registry.register("rate-limit", RateLimitPolicy)
        registry.register("content-safety", ContentSafetyPolicy)
    
    # Find pipeline config
    pipeline_name = "default"
    if tenant_id and use_case:
        pipeline_name = f"{tenant_id}:{use_case}"
    elif use_case:
        pipeline_name = use_case
    
    pipeline_cfg = cfg.pipelines.get(pipeline_name) or cfg.pipelines.get("default") or {}
    policy_names = pipeline_cfg.get("policies", [])
    
    # Build policies from registry
    policies = []
    for name in policy_names:
        policy_cfg = cfg.policies.get(name, {})
        policy = registry.create(name, **policy_cfg)
        if policy:
            policies.append(policy)
    
    return Pipeline(name=pipeline_name, policies=policies)

