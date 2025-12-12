# test_determinism.py
#
# Determinism and guarantee tests for DBL Main.

import concurrent.futures

import pytest
from dbl_core import BoundaryContext, PolicyDecision
from kl_kernel_logic import PsiDefinition

from dbl_main.core.pipeline import Pipeline
from dbl_main.policies.base import Policy
from dbl_main.policies.rate_limit import RateLimitPolicy
from dbl_main.policies.content_safety import ContentSafetyPolicy


class AllowPolicy(Policy):
    @property
    def name(self) -> str:
        return "allow"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(outcome="allow", reason="allowed")


@pytest.mark.stress
def test_pipeline_deterministic_under_repeated_calls():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(
        psi=psi,
        caller_id="user-1",
        tenant_id="tenant-1",
        metadata={"key": "value", "nested": {"a": 1}},
    )
    
    pipeline = Pipeline(
        name="test",
        policies=[
            RateLimitPolicy(max_requests=100),
            ContentSafetyPolicy(blocked_patterns=["forbidden"]),
        ],
    )
    
    first = pipeline.evaluate(ctx)
    
    for _ in range(100):
        result = pipeline.evaluate(ctx)
        
        assert result.final_outcome == first.final_outcome
        assert len(result.decisions) == len(first.decisions)
        
        # Context unchanged
        assert ctx.metadata["nested"]["a"] == 1


@pytest.mark.stress
def test_pipeline_no_mutation_of_context():
    psi = PsiDefinition(psi_type="test", name="op1")
    original_metadata = {"key": "value", "nested": {"a": 1}}
    ctx = BoundaryContext(psi=psi, metadata=original_metadata)
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy()])
    
    result = pipeline.evaluate(ctx)
    
    # effective_metadata is a deep copy, not an alias
    assert result.effective_metadata is not ctx.metadata
    assert result.effective_metadata == ctx.metadata
    
    # Modifying effective_metadata does not affect context
    result.effective_metadata["new_key"] = "new_value"
    assert "new_key" not in ctx.metadata


@pytest.mark.stress
def test_pipeline_thread_safety():
    psi = PsiDefinition(psi_type="test", name="parallel_op")
    
    pipeline = Pipeline(
        name="shared",
        policies=[RateLimitPolicy(max_requests=1000)],
    )
    
    def worker(idx: int):
        ctx = BoundaryContext(
            psi=psi,
            caller_id=f"user-{idx}",
            metadata={"idx": idx},
        )
        result = pipeline.evaluate(ctx)
        return result.final_outcome, result.effective_metadata.get("idx")
    
    num_tasks = 100
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(worker, i) for i in range(num_tasks)]
        results = [f.result() for f in futures]
    
    seen = set()
    for outcome, idx in results:
        assert outcome == "allow"
        assert idx is not None
        seen.add(idx)
    
    assert len(seen) == num_tasks


def test_pipeline_decisions_order_preserved():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    class NamedPolicy(Policy):
        def __init__(self, policy_name: str):
            self._policy_name = policy_name
        
        @property
        def name(self) -> str:
            return self._policy_name
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            return PolicyDecision(outcome="allow", reason=self._policy_name)
    
    pipeline = Pipeline(
        name="test",
        policies=[
            NamedPolicy("first"),
            NamedPolicy("second"),
            NamedPolicy("third"),
        ],
    )
    
    result = pipeline.evaluate(ctx)
    
    assert len(result.decisions) == 3
    assert result.decisions[0].reason == "first"
    assert result.decisions[1].reason == "second"
    assert result.decisions[2].reason == "third"

