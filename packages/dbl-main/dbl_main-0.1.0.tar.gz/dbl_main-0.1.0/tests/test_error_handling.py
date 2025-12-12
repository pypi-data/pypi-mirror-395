# test_error_handling.py
#
# Tests for error handling and robustness against misbehaving policies.
#
# Focus:
# - Policies that raise exceptions
# - Policies that return invalid PolicyDecisions
# - Pipeline behavior under error conditions

import pytest
from dbl_core import BoundaryContext, PolicyDecision
from kl_kernel_logic import PsiDefinition

from dbl_main.core.pipeline import Pipeline
from dbl_main.policies.base import Policy


# ---------------------------------------------------------------------------
# Policies that raise exceptions
# ---------------------------------------------------------------------------

class ExceptionPolicy(Policy):
    """Policy that raises an exception during evaluation."""
    
    def __init__(self, exception: Exception):
        self._exception = exception
    
    @property
    def name(self) -> str:
        return "exception"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        raise self._exception


class ConditionalExceptionPolicy(Policy):
    """Policy that raises exception based on metadata."""
    
    @property
    def name(self) -> str:
        return "conditional-exception"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        if context.metadata.get("should_fail"):
            raise RuntimeError("Conditional failure")
        return PolicyDecision(outcome="allow", reason="passed")


def test_exception_in_policy_propagates():
    """Exception in policy propagates up (no silent swallowing)."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(
        name="test",
        policies=[ExceptionPolicy(ValueError("boom"))],
    )
    
    with pytest.raises(ValueError, match="boom"):
        pipeline.evaluate(ctx)


def test_exception_after_successful_policies():
    """Exception after some successful policies still propagates."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    class AllowPolicy(Policy):
        @property
        def name(self) -> str:
            return "allow"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            return PolicyDecision(outcome="allow", reason="ok")
    
    pipeline = Pipeline(
        name="test",
        policies=[
            AllowPolicy(),
            AllowPolicy(),
            ExceptionPolicy(RuntimeError("late failure")),
        ],
    )
    
    with pytest.raises(RuntimeError, match="late failure"):
        pipeline.evaluate(ctx)


def test_context_unchanged_after_exception():
    """Context remains unchanged even when exception occurs."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    original_metadata = {"key": "value", "nested": {"a": 1}}
    ctx = BoundaryContext(psi=psi, caller_id="user-1", metadata=original_metadata)
    
    # Snapshot before
    before_metadata = dict(ctx.metadata)
    before_caller = ctx.caller_id
    
    pipeline = Pipeline(
        name="test",
        policies=[ExceptionPolicy(ValueError("boom"))],
    )
    
    with pytest.raises(ValueError):
        pipeline.evaluate(ctx)
    
    # Context unchanged
    assert ctx.caller_id == before_caller
    assert dict(ctx.metadata) == before_metadata
    assert ctx.metadata["nested"]["a"] == 1


def test_conditional_exception_based_on_metadata():
    """Exception can be triggered by metadata content."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    
    pipeline = Pipeline(
        name="test",
        policies=[ConditionalExceptionPolicy()],
    )
    
    # Normal case
    ctx_ok = BoundaryContext(psi=psi, metadata={"should_fail": False})
    result = pipeline.evaluate(ctx_ok)
    assert result.is_allowed()
    
    # Failure case
    ctx_fail = BoundaryContext(psi=psi, metadata={"should_fail": True})
    with pytest.raises(RuntimeError, match="Conditional failure"):
        pipeline.evaluate(ctx_fail)


# ---------------------------------------------------------------------------
# Policies with edge-case returns
# ---------------------------------------------------------------------------

class NoneOutcomePolicy(Policy):
    """Policy that returns None as outcome (invalid)."""
    
    @property
    def name(self) -> str:
        return "none-outcome"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        # This is technically invalid but tests robustness
        return PolicyDecision(outcome=None, reason="bad")  # type: ignore


class EmptyReasonPolicy(Policy):
    """Policy that returns empty reason."""
    
    @property
    def name(self) -> str:
        return "empty-reason"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(outcome="allow", reason="")


class NoneModifiedMetadataPolicy(Policy):
    """Policy that explicitly sets modified_metadata to None."""
    
    @property
    def name(self) -> str:
        return "none-modified"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(
            outcome="modify",
            reason="explicit none",
            modified_metadata=None,
        )


def test_empty_reason_is_valid():
    """Empty reason string is acceptable."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(name="test", policies=[EmptyReasonPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert result.decisions[0].reason == ""


def test_none_modified_metadata_is_ignored():
    """modified_metadata=None should not affect effective_metadata."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={"original": True})
    
    pipeline = Pipeline(name="test", policies=[NoneModifiedMetadataPolicy()])
    result = pipeline.evaluate(ctx)
    
    # Original preserved, no crash
    assert result.effective_metadata["original"] is True
    assert result.final_outcome == "modify"


# ---------------------------------------------------------------------------
# Multiple exception types
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("exception", [
    ValueError("value error"),
    TypeError("type error"),
    RuntimeError("runtime error"),
    KeyError("key error"),
    AttributeError("attribute error"),
])
def test_various_exception_types_propagate(exception: Exception):
    """Various exception types all propagate correctly."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(
        name="test",
        policies=[ExceptionPolicy(exception)],
    )
    
    with pytest.raises(type(exception)):
        pipeline.evaluate(ctx)


# ---------------------------------------------------------------------------
# Slow / hanging policies (documentation)
# ---------------------------------------------------------------------------

def test_slow_policy_completes():
    """Slow policy should complete normally (no timeout by default)."""
    
    import time
    
    class SlowPolicy(Policy):
        @property
        def name(self) -> str:
            return "slow"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            time.sleep(0.01)  # 10ms
            return PolicyDecision(outcome="allow", reason="slow but ok")
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(name="test", policies=[SlowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()


# ---------------------------------------------------------------------------
# Policy returning wrong types (type safety)
# ---------------------------------------------------------------------------

class WrongReturnTypePolicy(Policy):
    """Policy that returns wrong type instead of PolicyDecision."""
    
    @property
    def name(self) -> str:
        return "wrong-type"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return {"outcome": "allow", "reason": "dict not PolicyDecision"}  # type: ignore


def test_wrong_return_type_causes_error():
    """Policy returning wrong type causes AttributeError."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(name="test", policies=[WrongReturnTypePolicy()])
    
    # Pipeline tries to access .outcome on a dict, which will fail
    with pytest.raises(AttributeError):
        pipeline.evaluate(ctx)


# ---------------------------------------------------------------------------
# Block after exception (order matters)
# ---------------------------------------------------------------------------

def test_block_before_exception_stops_pipeline():
    """Block policy stops pipeline before exception policy runs."""
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    class BlockPolicy(Policy):
        @property
        def name(self) -> str:
            return "block"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            return PolicyDecision(outcome="block", reason="blocked")
    
    pipeline = Pipeline(
        name="test",
        policies=[
            BlockPolicy(),
            ExceptionPolicy(ValueError("should not run")),
        ],
    )
    
    # No exception because block stops pipeline
    result = pipeline.evaluate(ctx)
    assert result.final_outcome == "block"
    assert len(result.decisions) == 1

