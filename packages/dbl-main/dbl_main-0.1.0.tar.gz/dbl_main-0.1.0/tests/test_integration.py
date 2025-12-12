# test_integration.py
#
# Integration tests for DBL Main.
#
# Focus:
# - Full flow from context to result
# - Configuration loading and pipeline building
# - Registry usage
# - Audit logging integration
# - Real policy combinations

import pytest

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration
import tempfile
import os
import json
from pathlib import Path

from dbl_core import BoundaryContext, PolicyDecision
from kl_kernel_logic import PsiDefinition

from dbl_main.core.pipeline import Pipeline
from dbl_main.core.registry import PolicyRegistry, PipelineRegistry
from dbl_main.core.context_builder import ContextBuilder
from dbl_main.policies.base import Policy
from dbl_main.policies.rate_limit import RateLimitPolicy
from dbl_main.policies.content_safety import ContentSafetyPolicy
from dbl_main.audit.logger import AuditLogger
from dbl_main.config.loader import load_config, build_pipeline_for, Config


# ---------------------------------------------------------------------------
# Full flow integration
# ---------------------------------------------------------------------------

def test_full_flow_allow():
    """Complete flow: context -> pipeline -> result -> allowed."""
    # 1. Build context
    psi = PsiDefinition(psi_type="llm", name="generate")
    ctx = BoundaryContext(
        psi=psi,
        caller_id="user-123",
        tenant_id="tenant-abc",
        channel="api",
        metadata={"prompt": "Hello world", "model": "gpt-4"},
    )
    
    # 2. Build pipeline with real policies
    pipeline = Pipeline(
        name="default",
        policies=[
            RateLimitPolicy(max_requests=100),
            ContentSafetyPolicy(blocked_patterns=["forbidden"]),
        ],
    )
    
    # 3. Evaluate
    result = pipeline.evaluate(ctx)
    
    # 4. Assert
    assert result.is_allowed()
    assert result.context is ctx
    assert result.effective_psi is ctx.psi
    assert "prompt" in result.effective_metadata


def test_full_flow_block_by_content():
    """Complete flow: blocked by content safety."""
    psi = PsiDefinition(psi_type="llm", name="generate")
    ctx = BoundaryContext(
        psi=psi,
        caller_id="user-123",
        metadata={"prompt": "This contains forbidden content"},
    )
    
    pipeline = Pipeline(
        name="default",
        policies=[
            RateLimitPolicy(max_requests=100),
            ContentSafetyPolicy(blocked_patterns=["forbidden"]),
        ],
    )
    
    result = pipeline.evaluate(ctx)
    
    assert not result.is_allowed()
    assert result.final_outcome == "block"
    assert any("content" in d.reason.lower() for d in result.decisions)


def test_full_flow_block_by_rate_limit():
    """Complete flow: blocked by rate limit."""
    psi = PsiDefinition(psi_type="llm", name="generate")
    ctx = BoundaryContext(
        psi=psi,
        caller_id="user-123",
        metadata={"prompt": "Hello"},
    )
    
    # Rate limit checker that always says exceeded (takes caller_id, window_seconds)
    def always_exceeded(caller_id: str, window_seconds: int) -> int:
        return 1000  # Return count that exceeds max
    
    pipeline = Pipeline(
        name="default",
        policies=[
            RateLimitPolicy(max_requests=100, rate_checker=always_exceeded),
            ContentSafetyPolicy(blocked_patterns=["forbidden"]),
        ],
    )
    
    result = pipeline.evaluate(ctx)
    
    assert not result.is_allowed()
    assert result.final_outcome == "block"
    assert len(result.decisions) == 1  # Stopped at rate limit


# ---------------------------------------------------------------------------
# Registry integration
# ---------------------------------------------------------------------------

def test_policy_registry_with_pipeline():
    """PolicyRegistry used to build pipeline."""
    registry = PolicyRegistry()
    registry.register("rate-limit", RateLimitPolicy)
    registry.register("content-safety", ContentSafetyPolicy)
    
    # Build policies from registry
    policies = [
        registry.create("rate-limit", max_requests=50),
        registry.create("content-safety", blocked_patterns=["bad"]),
    ]
    
    pipeline = Pipeline(name="from-registry", policies=policies)
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={"text": "good content"})
    
    result = pipeline.evaluate(ctx)
    assert result.is_allowed()


def test_pipeline_registry_lookup():
    """PipelineRegistry for tenant/channel lookup."""
    policy_registry = PolicyRegistry()
    policy_registry.register("rate-limit", RateLimitPolicy)
    
    pipeline_registry = PipelineRegistry()
    
    # Register pipelines for different contexts
    default_pipeline = Pipeline(
        name="default",
        policies=[policy_registry.create("rate-limit", max_requests=100)],
    )
    premium_pipeline = Pipeline(
        name="premium",
        policies=[policy_registry.create("rate-limit", max_requests=1000)],
    )
    
    pipeline_registry.register("default", default_pipeline)
    pipeline_registry.register("premium:api", premium_pipeline)
    
    # Lookup by key
    assert pipeline_registry.get("default") is default_pipeline
    assert pipeline_registry.get("premium:api") is premium_pipeline
    
    # For context using tenant/channel kwargs
    found = pipeline_registry.for_context(tenant_id="premium", channel="api")
    assert found is premium_pipeline
    
    # Fallback to default
    found_default = pipeline_registry.for_context(tenant_id="unknown", channel="cli")
    assert found_default is default_pipeline


# ---------------------------------------------------------------------------
# Audit integration
# ---------------------------------------------------------------------------

def test_audit_logger_captures_result():
    """AuditLogger captures pipeline result."""
    logger = AuditLogger()
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, caller_id="user-1")
    
    pipeline = Pipeline(name="test", policies=[RateLimitPolicy(max_requests=100)])
    result = pipeline.evaluate(ctx)
    
    # Log result
    logger.log(result)
    
    records = logger.get_records()
    assert len(records) == 1
    
    record = records[0]
    assert "timestamp" in record
    assert "result" in record
    assert record["result"]["final_outcome"] == "allow"
    assert record["result"]["context"]["caller_id"] == "user-1"


def test_audit_logger_multiple_results():
    """AuditLogger accumulates multiple results."""
    logger = AuditLogger()
    
    pipeline = Pipeline(name="test", policies=[])
    
    for i in range(10):
        psi = PsiDefinition(psi_type="test", name=f"op-{i}")
        ctx = BoundaryContext(psi=psi, caller_id=f"user-{i}")
        result = pipeline.evaluate(ctx)
        logger.log(result)
    
    records = logger.get_records()
    assert len(records) == 10
    
    # Each entry has unique caller
    callers = {r["result"]["context"]["caller_id"] for r in records}
    assert len(callers) == 10


# ---------------------------------------------------------------------------
# Configuration integration (JSON only - no pyyaml dependency)
# ---------------------------------------------------------------------------

def test_config_to_pipeline_flow_json():
    """Load config from JSON and build pipeline."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write pipelines.json
        pipelines_path = Path(tmpdir) / "pipelines.json"
        pipelines_path.write_text(json.dumps({
            "pipelines": {
                "default": {
                    "policies": ["rate-limit", "content-safety"]
                },
                "premium": {
                    "policies": ["content-safety"]
                }
            }
        }))
        
        # Write policies.json
        policies_path = Path(tmpdir) / "policies.json"
        policies_path.write_text(json.dumps({
            "policies": {
                "rate-limit": {"max_requests": 100},
                "content-safety": {"blocked_patterns": ["forbidden", "banned"]}
            }
        }))
        
        # Load and build
        cfg = load_config(tmpdir)
        pipeline = build_pipeline_for(cfg, use_case="default")
        
        assert pipeline.name == "default"
        assert len(pipeline.policies) == 2
        
        # Test it works
        psi = PsiDefinition(psi_type="test", name="op1")
        ctx = BoundaryContext(psi=psi, metadata={"text": "clean"})
        result = pipeline.evaluate(ctx)
        
        assert result.is_allowed()


def test_config_tenant_specific_pipeline_json():
    """Tenant-specific pipeline from JSON config."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write config
        pipelines_path = Path(tmpdir) / "pipelines.json"
        pipelines_path.write_text(json.dumps({
            "pipelines": {
                "default": {"policies": ["rate-limit"]},
                "enterprise:llm": {"policies": ["content-safety"]}
            }
        }))
        
        policies_path = Path(tmpdir) / "policies.json"
        policies_path.write_text(json.dumps({
            "policies": {
                "rate-limit": {"max_requests": 100},
                "content-safety": {"blocked_patterns": []}
            }
        }))
        
        cfg = load_config(tmpdir)
        
        # Default pipeline
        default = build_pipeline_for(cfg)
        assert default.name == "default"
        
        # Tenant-specific
        enterprise = build_pipeline_for(cfg, tenant_id="enterprise", use_case="llm")
        assert enterprise.name == "enterprise:llm"


# ---------------------------------------------------------------------------
# Context builder integration
# ---------------------------------------------------------------------------

def test_context_builder_to_pipeline():
    """ContextBuilder creates context for pipeline."""
    builder = ContextBuilder()
    builder.set_defaults(
        channel="api",
        tenant_id="default-tenant",
    )
    
    psi = PsiDefinition(psi_type="llm", name="generate")
    
    ctx = builder.build(
        psi=psi,
        caller_id="user-1",
        metadata={"prompt": "Hello"},
    )
    
    assert ctx.channel == "api"
    assert ctx.tenant_id == "default-tenant"
    assert ctx.caller_id == "user-1"
    
    pipeline = Pipeline(name="test", policies=[])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert result.context.channel == "api"


def test_context_builder_from_request():
    """ContextBuilder.from_request creates context from raw data."""
    builder = ContextBuilder()
    builder.set_defaults(channel="default-channel")
    
    ctx = builder.from_request(
        psi_type="tool",
        psi_name="calculator",
        caller_id="user-abc",
        metadata={"operation": "add"},
    )
    
    assert ctx.psi.psi_type == "tool"
    assert ctx.psi.name == "calculator"
    assert ctx.caller_id == "user-abc"
    assert ctx.channel == "default-channel"


# ---------------------------------------------------------------------------
# Custom policy integration
# ---------------------------------------------------------------------------

def test_custom_policy_in_pipeline():
    """Custom policy integrates with standard pipeline."""
    
    class TenantCheckPolicy(Policy):
        def __init__(self, allowed_tenants: list[str]):
            self._allowed = set(allowed_tenants)
        
        @property
        def name(self) -> str:
            return "tenant-check"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            if context.tenant_id in self._allowed:
                return PolicyDecision(outcome="allow", reason="tenant allowed")
            return PolicyDecision(
                outcome="block",
                reason=f"tenant {context.tenant_id} not in allowed list",
            )
    
    pipeline = Pipeline(
        name="with-custom",
        policies=[
            TenantCheckPolicy(allowed_tenants=["premium", "enterprise"]),
            RateLimitPolicy(max_requests=100),
        ],
    )
    
    psi = PsiDefinition(psi_type="test", name="op1")
    
    # Allowed tenant
    ctx_premium = BoundaryContext(psi=psi, tenant_id="premium")
    result = pipeline.evaluate(ctx_premium)
    assert result.is_allowed()
    
    # Blocked tenant
    ctx_free = BoundaryContext(psi=psi, tenant_id="free")
    result = pipeline.evaluate(ctx_free)
    assert not result.is_allowed()
    assert "not in allowed" in result.decisions[0].reason


# ---------------------------------------------------------------------------
# End-to-end scenario
# ---------------------------------------------------------------------------

def test_e2e_llm_request_flow():
    """End-to-end: LLM request through full stack."""
    # Setup
    policy_registry = PolicyRegistry()
    policy_registry.register("rate-limit", RateLimitPolicy)
    policy_registry.register("content-safety", ContentSafetyPolicy)
    
    pipeline_registry = PipelineRegistry()
    
    # Build pipeline
    pipeline = Pipeline(
        name="llm-default",
        policies=[
            policy_registry.create("rate-limit", max_requests=1000),
            policy_registry.create("content-safety", blocked_patterns=["hack", "exploit"]),
        ],
    )
    pipeline_registry.register("default", pipeline)
    
    # Context builder
    builder = ContextBuilder()
    builder.set_defaults(channel="api")
    
    # Audit
    audit = AuditLogger()
    
    # Simulate request
    psi = PsiDefinition(psi_type="llm", name="chat-completion")
    ctx = builder.build(
        psi=psi,
        caller_id="user-abc",
        tenant_id="tenant-xyz",
        metadata={
            "prompt": "Write a poem about nature",
            "model": "gpt-4",
            "temperature": 0.7,
        },
    )
    
    # Get pipeline and evaluate
    active_pipeline = pipeline_registry.for_context(
        tenant_id=ctx.tenant_id,
        channel=ctx.channel,
    ) or pipeline_registry.get("default")
    result = active_pipeline.evaluate(ctx)
    
    # Log
    audit.log(result)
    
    # Assertions
    assert result.is_allowed()
    assert result.effective_metadata["prompt"] == "Write a poem about nature"
    
    records = audit.get_records()
    assert len(records) == 1
    assert records[0]["result"]["final_outcome"] == "allow"


def test_e2e_blocked_request_flow():
    """End-to-end: Blocked request through full stack."""
    policy_registry = PolicyRegistry()
    policy_registry.register("content-safety", ContentSafetyPolicy)
    
    pipeline = Pipeline(
        name="strict",
        policies=[
            policy_registry.create("content-safety", blocked_patterns=["malicious"]),
        ],
    )
    
    audit = AuditLogger()
    
    psi = PsiDefinition(psi_type="llm", name="generate")
    ctx = BoundaryContext(
        psi=psi,
        caller_id="attacker",
        metadata={"prompt": "Do something malicious"},
    )
    
    result = pipeline.evaluate(ctx)
    audit.log(result)
    
    assert not result.is_allowed()
    assert result.final_outcome == "block"
    
    records = audit.get_records()
    assert records[0]["result"]["final_outcome"] == "block"
