# test_config.py

import json
import tempfile
from pathlib import Path

from dbl_core import BoundaryContext
from kl_kernel_logic import PsiDefinition

from dbl_main.config.loader import Config, load_config, build_pipeline_for, PolicyRegistry


def test_config_from_json():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir)
        
        # Write pipelines.json
        pipelines = {"pipelines": {"default": {"policies": ["rate-limit"]}}}
        with open(config_dir / "pipelines.json", "w") as f:
            json.dump(pipelines, f)
        
        # Write policies.json
        policies = {"policies": {"rate-limit": {"max_requests": 50}}}
        with open(config_dir / "policies.json", "w") as f:
            json.dump(policies, f)
        
        cfg = load_config(str(config_dir))
        
        assert "default" in cfg.pipelines
        assert cfg.pipelines["default"]["policies"] == ["rate-limit"]
        assert cfg.policies["rate-limit"]["max_requests"] == 50


def test_build_pipeline_for_default():
    cfg = Config(
        pipelines={"default": {"policies": ["rate-limit", "content-safety"]}},
        policies={
            "rate-limit": {"max_requests": 100},
            "content-safety": {"blocked_patterns": ["bad"]},
        },
    )
    
    pipeline = build_pipeline_for(cfg)
    
    assert pipeline.name == "default"
    assert len(pipeline.policies) == 2


def test_build_pipeline_for_use_case():
    cfg = Config(
        pipelines={
            "default": {"policies": ["rate-limit"]},
            "llm-generate": {"policies": ["content-safety"]},
        },
        policies={
            "rate-limit": {},
            "content-safety": {},
        },
    )
    
    pipeline = build_pipeline_for(cfg, use_case="llm-generate")
    
    assert pipeline.name == "llm-generate"
    assert len(pipeline.policies) == 1


def test_build_pipeline_with_custom_registry():
    from dbl_main.policies.base import Policy
    from dbl_core import PolicyDecision
    
    class CustomPolicy(Policy):
        @property
        def name(self) -> str:
            return "custom"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            return PolicyDecision(outcome="allow", reason="custom")
    
    registry = PolicyRegistry()
    registry.register("custom", CustomPolicy)
    
    cfg = Config(
        pipelines={"default": {"policies": ["custom"]}},
        policies={"custom": {}},
    )
    
    pipeline = build_pipeline_for(cfg, registry=registry)
    
    assert len(pipeline.policies) == 1
    assert pipeline.policies[0].name == "custom"


def test_policy_registry_create():
    from dbl_main.policies.rate_limit import RateLimitPolicy
    
    registry = PolicyRegistry()
    registry.register("rate-limit", RateLimitPolicy)
    
    policy = registry.create("rate-limit", max_requests=50)
    
    assert policy is not None
    assert policy._max_requests == 50


def test_policy_registry_unknown_returns_none():
    registry = PolicyRegistry()
    
    policy = registry.create("unknown")
    
    assert policy is None

