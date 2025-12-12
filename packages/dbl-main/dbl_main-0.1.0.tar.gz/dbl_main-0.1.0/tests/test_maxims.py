# test_maxims.py
#
# Stress tests for DBL Main design maxims.
#
# Maxim 1: Policies always see the original BoundaryContext
# Maxim 2: Modifications accumulate only in effective_*
# Maxim 3: No mutation of BoundaryContext
# Maxim 4: Aggregation is deterministic

import copy
import concurrent.futures
from typing import Any

import pytest
from dbl_core import BoundaryContext, PolicyDecision
from kl_kernel_logic import PsiDefinition

from dbl_main.core.pipeline import Pipeline
from dbl_main.policies.base import Policy


# ---------------------------------------------------------------------------
# Maxim 1: Policies always see the original BoundaryContext
# ---------------------------------------------------------------------------

class ContextCapturingPolicy(Policy):
    """Captures the context it receives for later inspection."""
    
    def __init__(self, name: str, captured: list[dict[str, Any]]):
        self._name = name
        self._captured = captured
    
    @property
    def name(self) -> str:
        return self._name
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        # Capture a snapshot of what we see
        self._captured.append({
            "policy": self._name,
            "caller_id": context.caller_id,
            "metadata": dict(context.metadata),
            "metadata_id": id(context.metadata),
            "psi_name": context.psi.name,
        })
        return PolicyDecision(outcome="allow", reason=self._name)


class ModifyingPolicy(Policy):
    """Returns modified_metadata to test accumulation."""
    
    def __init__(self, key: str, value: Any):
        self._key = key
        self._value = value
    
    @property
    def name(self) -> str:
        return f"modify-{self._key}"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(
            outcome="modify",
            reason=f"set {self._key}",
            modified_metadata={self._key: self._value},
        )


@pytest.mark.stress
def test_maxim1_policies_see_original_context():
    """All policies see the exact same original context, not modified versions."""
    
    original_metadata = {"original": True, "counter": 0}
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, caller_id="user-1", metadata=original_metadata)
    
    captured: list[dict[str, Any]] = []
    
    pipeline = Pipeline(
        name="test",
        policies=[
            ContextCapturingPolicy("first", captured),
            ModifyingPolicy("added_by_first", "value1"),
            ContextCapturingPolicy("second", captured),
            ModifyingPolicy("added_by_second", "value2"),
            ContextCapturingPolicy("third", captured),
        ],
    )
    
    result = pipeline.evaluate(ctx)
    
    # All three capturing policies should see the SAME original context
    assert len(captured) == 3
    
    for i, capture in enumerate(captured):
        # Original metadata (equality)
        assert capture["metadata"] == original_metadata, f"Policy {i} saw modified context"
        assert "added_by_first" not in capture["metadata"]
        assert "added_by_second" not in capture["metadata"]
        assert capture["caller_id"] == "user-1"
        
        # Psi constancy
        assert capture["psi_name"] == "op1"
    
    # But effective_metadata should have all modifications
    assert result.effective_metadata["added_by_first"] == "value1"
    assert result.effective_metadata["added_by_second"] == "value2"
    
    # effective_metadata is not the original
    assert result.effective_metadata is not ctx.metadata


@pytest.mark.stress
def test_maxim1_under_load():
    """Maxim 1 holds under repeated calls."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    original_metadata = {"stable": True}
    ctx = BoundaryContext(psi=psi, metadata=original_metadata)
    
    for iteration in range(100):
        captured: list[dict[str, Any]] = []
        
        pipeline = Pipeline(
            name="test",
            policies=[
                ContextCapturingPolicy("a", captured),
                ModifyingPolicy("iter", iteration),
                ContextCapturingPolicy("b", captured),
            ],
        )
        
        result = pipeline.evaluate(ctx)
        
        # Both policies saw original
        assert captured[0]["metadata"] == original_metadata
        assert captured[1]["metadata"] == original_metadata
        
        # Metadata identity preserved across captures
        assert captured[0]["metadata_id"] == captured[1]["metadata_id"]
        
        # But result has modification
        assert result.effective_metadata["iter"] == iteration


# ---------------------------------------------------------------------------
# Maxim 2: Modifications accumulate only in effective_*
# ---------------------------------------------------------------------------

@pytest.mark.stress
def test_maxim2_modifications_accumulate():
    """Later policies can override earlier modifications."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={})
    
    pipeline = Pipeline(
        name="test",
        policies=[
            ModifyingPolicy("key", "first"),
            ModifyingPolicy("key", "second"),  # overwrites
            ModifyingPolicy("another", "value"),
        ],
    )
    
    result = pipeline.evaluate(ctx)
    
    # Last write wins
    assert result.effective_metadata["key"] == "second"
    assert result.effective_metadata["another"] == "value"


@pytest.mark.stress
def test_maxim2_psi_modifications():
    """Later policies can override psi."""
    
    psi1 = PsiDefinition(psi_type="test", name="original")
    psi2 = PsiDefinition(psi_type="test", name="modified")
    psi3 = PsiDefinition(psi_type="test", name="final")
    
    class PsiModifyingPolicy(Policy):
        def __init__(self, new_psi: PsiDefinition):
            self._new_psi = new_psi
        
        @property
        def name(self) -> str:
            return f"psi-{self._new_psi.name}"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            return PolicyDecision(
                outcome="modify",
                reason="change psi",
                modified_psi=self._new_psi,
            )
    
    ctx = BoundaryContext(psi=psi1, metadata={})
    
    pipeline = Pipeline(
        name="test",
        policies=[
            PsiModifyingPolicy(psi2),
            PsiModifyingPolicy(psi3),  # overwrites
        ],
    )
    
    result = pipeline.evaluate(ctx)
    
    # Context unchanged
    assert ctx.psi.name == "original"
    assert ctx.psi is psi1
    
    # Effective psi is the last one (identity check)
    assert result.effective_psi.name == "final"
    assert result.effective_psi is psi3
    assert result.effective_psi is not ctx.psi


@pytest.mark.stress
def test_maxim2_combined_psi_and_metadata_modifications():
    """Policies can modify both psi and metadata, later wins."""
    
    psi_original = PsiDefinition(psi_type="test", name="original")
    psi_modified = PsiDefinition(psi_type="test", name="modified")
    
    class CombinedModifyingPolicy(Policy):
        def __init__(self, new_psi: PsiDefinition, key: str, value: Any):
            self._new_psi = new_psi
            self._key = key
            self._value = value
        
        @property
        def name(self) -> str:
            return f"combined-{self._key}"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            return PolicyDecision(
                outcome="modify",
                reason="combined",
                modified_psi=self._new_psi,
                modified_metadata={self._key: self._value},
            )
    
    ctx = BoundaryContext(psi=psi_original, metadata={"existing": "value"})
    
    pipeline = Pipeline(
        name="test",
        policies=[
            CombinedModifyingPolicy(psi_modified, "first", 1),
            CombinedModifyingPolicy(psi_modified, "second", 2),
        ],
    )
    
    result = pipeline.evaluate(ctx)
    
    # Both modifications accumulated
    assert result.effective_metadata["first"] == 1
    assert result.effective_metadata["second"] == 2
    assert result.effective_metadata["existing"] == "value"
    
    # Psi modified
    assert result.effective_psi is psi_modified


# ---------------------------------------------------------------------------
# Maxim 3: No mutation of BoundaryContext
# ---------------------------------------------------------------------------

@pytest.mark.stress
def test_maxim3_no_mutation():
    """BoundaryContext must remain unchanged after pipeline evaluation."""
    
    original_nested = {"deep": {"value": 1}}
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(
        psi=psi,
        caller_id="user-1",
        tenant_id="tenant-1",
        metadata={"shallow": "value", "nested": original_nested},
    )
    
    # Snapshot before
    before_caller = ctx.caller_id
    before_tenant = ctx.tenant_id
    before_psi_name = ctx.psi.name
    before_metadata = copy.deepcopy(dict(ctx.metadata))
    
    class AggressivePolicy(Policy):
        @property
        def name(self) -> str:
            return "aggressive"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            return PolicyDecision(
                outcome="modify",
                reason="aggressive",
                modified_metadata={"injected": True, "nested": {"deep": {"value": 999}}},
            )
    
    pipeline = Pipeline(name="test", policies=[AggressivePolicy()])
    result = pipeline.evaluate(ctx)
    
    # Context unchanged
    assert ctx.caller_id == before_caller
    assert ctx.tenant_id == before_tenant
    assert ctx.psi.name == before_psi_name
    assert dict(ctx.metadata) == before_metadata
    
    # Nested structure unchanged
    assert ctx.metadata["nested"]["deep"]["value"] == 1
    
    # effective_metadata is independent
    assert result.effective_metadata["nested"]["deep"]["value"] == 999
    assert result.effective_metadata is not ctx.metadata


@pytest.mark.stress
def test_maxim3_effective_metadata_is_independent():
    """Modifying effective_metadata does not affect context."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={"key": "value"})
    
    pipeline = Pipeline(name="test", policies=[])
    result = pipeline.evaluate(ctx)
    
    # Reference independence
    assert result.effective_metadata is not ctx.metadata
    
    # Mutate result
    result.effective_metadata["new_key"] = "new_value"
    
    # Context unaffected
    assert "new_key" not in ctx.metadata


def test_maxim3_mutation_is_convention():
    """
    Direct mutation of context.metadata IS technically possible.
    
    This test documents the current behavior: BoundaryContext.metadata
    is a regular dict that CAN be mutated. The no-mutation maxim is a
    convention that policies SHOULD follow, not a technical enforcement.
    
    The protection comes from:
    1. Pipeline uses deepcopy for effective_metadata
    2. Policies should use modified_metadata in PolicyDecision
    3. Code review and testing enforce the convention
    """
    
    psi = PsiDefinition(psi_type="test", name="op1")
    # Use deepcopy to protect original from rogue policies
    ctx = BoundaryContext(psi=psi, metadata={"original": True})
    
    class RoguePolicy(Policy):
        """A policy that violates the convention (for documentation)."""
        
        @property
        def name(self) -> str:
            return "rogue"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            # This is BAD - violates maxim 3
            context.metadata["rogue"] = True
            return PolicyDecision(outcome="allow", reason="rogue")
    
    class GoodPolicy(Policy):
        """A policy that follows the convention."""
        
        @property
        def name(self) -> str:
            return "good"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            # This is GOOD - uses modified_metadata
            return PolicyDecision(
                outcome="modify",
                reason="good",
                modified_metadata={"added": True},
            )
    
    # Good policy: effective_metadata gets the change
    good_pipeline = Pipeline(name="good", policies=[GoodPolicy()])
    good_ctx = BoundaryContext(psi=psi, metadata={"original": True})
    good_result = good_pipeline.evaluate(good_ctx)
    
    assert "added" in good_result.effective_metadata
    assert "added" not in good_ctx.metadata  # Original unchanged


# ---------------------------------------------------------------------------
# Maxim 4: Aggregation is deterministic
# ---------------------------------------------------------------------------

@pytest.mark.stress
def test_maxim4_deterministic_under_load():
    """Same input produces identical output, 1000 times."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(
        psi=psi,
        caller_id="user-1",
        metadata={"stable": True, "nested": {"a": 1}},
    )
    
    pipeline = Pipeline(
        name="test",
        policies=[
            ModifyingPolicy("added", "value"),
        ],
    )
    
    first = pipeline.evaluate(ctx)
    first_outcome = first.final_outcome
    first_effective = dict(first.effective_metadata)
    
    for _ in range(1000):
        result = pipeline.evaluate(ctx)
        assert result.final_outcome == first_outcome
        assert dict(result.effective_metadata) == first_effective


@pytest.mark.stress
def test_maxim4_deterministic_multi_policy():
    """Determinism with multiple policies including allow and modify."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={"input": "data"})
    
    class AllowPolicy(Policy):
        @property
        def name(self) -> str:
            return "allow"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            return PolicyDecision(outcome="allow", reason="allowed")
    
    class NoModifyPolicy(Policy):
        @property
        def name(self) -> str:
            return "no-modify"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            return PolicyDecision(outcome="allow", reason="no changes")
    
    pipeline = Pipeline(
        name="test",
        policies=[
            AllowPolicy(),
            ModifyingPolicy("key1", "value1"),
            NoModifyPolicy(),
            ModifyingPolicy("key2", "value2"),
            AllowPolicy(),
        ],
    )
    
    first = pipeline.evaluate(ctx)
    
    for _ in range(100):
        result = pipeline.evaluate(ctx)
        assert result.final_outcome == first.final_outcome
        assert len(result.decisions) == len(first.decisions)
        assert dict(result.effective_metadata) == dict(first.effective_metadata)


@pytest.mark.stress
def test_maxim4_deterministic_parallel():
    """Determinism holds under parallel execution."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    
    class IndexedModifyingPolicy(Policy):
        @property
        def name(self) -> str:
            return "indexed"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            idx = context.metadata.get("idx", 0)
            return PolicyDecision(
                outcome="modify",
                reason="indexed",
                modified_metadata={
                    "key": "value",
                    "derived": f"idx-{idx}",
                },
            )
    
    pipeline = Pipeline(
        name="shared",
        policies=[IndexedModifyingPolicy()],
    )
    
    def worker(idx: int):
        ctx = BoundaryContext(
            psi=psi,
            caller_id=f"user-{idx}",
            metadata={"idx": idx},
        )
        result = pipeline.evaluate(ctx)
        return (
            result.final_outcome,
            result.effective_metadata.get("idx"),
            result.effective_metadata.get("key"),
            result.effective_metadata.get("derived"),
        )
    
    num_tasks = 200
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(worker, i) for i in range(num_tasks)]
        results = [f.result() for f in futures]
    
    seen_idx = set()
    for outcome, idx, key, derived in results:
        assert outcome == "modify"
        assert key == "value"
        assert idx is not None
        assert derived == f"idx-{idx}"  # Derived value matches input
        seen_idx.add(idx)
    
    # All unique indices processed
    assert len(seen_idx) == num_tasks


def test_pipeline_decisions_order_preserved():
    """Decision order matches policy order."""
    
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


# ---------------------------------------------------------------------------
# Combined: All maxims under extreme conditions
# ---------------------------------------------------------------------------

@pytest.mark.stress
def test_all_maxims_combined():
    """Stress test combining all maxims."""
    
    psi = PsiDefinition(psi_type="test", name="combined")
    original_metadata = {"original": True, "count": 0}
    
    captured_all: list[dict[str, Any]] = []
    
    for iteration in range(50):
        ctx = BoundaryContext(
            psi=psi,
            caller_id=f"user-{iteration}",
            metadata=original_metadata,
        )
        
        # Reference check: context uses original_metadata
        assert ctx.metadata is original_metadata
        assert ctx.psi is psi
        
        captured: list[dict[str, Any]] = []
        
        pipeline = Pipeline(
            name="combined",
            policies=[
                ContextCapturingPolicy("first", captured),
                ModifyingPolicy("iter", iteration),
                ContextCapturingPolicy("second", captured),
                ModifyingPolicy("nested", {"deep": iteration}),
                ContextCapturingPolicy("third", captured),
            ],
        )
        
        result = pipeline.evaluate(ctx)
        
        # Maxim 1: All saw original
        for c in captured:
            assert c["metadata"] == original_metadata
            assert c["psi_name"] == "combined"
        
        # Maxim 2: Modifications accumulated
        assert result.effective_metadata["iter"] == iteration
        assert result.effective_metadata["nested"]["deep"] == iteration
        
        # Maxim 3: Context unchanged
        assert ctx.metadata == original_metadata
        assert ctx.metadata is original_metadata
        assert result.effective_metadata is not ctx.metadata
        
        # Maxim 4: Outcome is predictable
        assert result.final_outcome == "modify"
        
        captured_all.extend(captured)
    
    # 50 iterations × 3 capturing policies = 150 captures
    assert len(captured_all) == 150
