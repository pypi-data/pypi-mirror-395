# test_fuzz.py
#
# Hypothesis-based fuzz tests for DBL Main.
#
# Focus:
# - Random inputs never crash
# - Invariants hold under all inputs
# - Property-based testing

import pytest

try:
    from hypothesis import given, strategies as st, settings, assume, HealthCheck
    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False
    # Dummy decorators when hypothesis not available
    def given(*args, **kwargs):
        def decorator(f):
            return f
        return decorator
    
    def settings(*args, **kwargs):
        def decorator(f):
            return f
        return decorator
    
    def assume(x):
        pass
    
    class st:
        @staticmethod
        def text(*args, **kwargs):
            return None
        @staticmethod
        def integers(*args, **kwargs):
            return None
        @staticmethod
        def floats(*args, **kwargs):
            return None
        @staticmethod
        def booleans(*args, **kwargs):
            return None
        @staticmethod
        def none(*args, **kwargs):
            return None
        @staticmethod
        def one_of(*args, **kwargs):
            return None
        @staticmethod
        def dictionaries(*args, **kwargs):
            return None
        @staticmethod
        def builds(*args, **kwargs):
            return None
        @staticmethod
        def characters(*args, **kwargs):
            return None

from dbl_core import BoundaryContext, PolicyDecision
from kl_kernel_logic import PsiDefinition

from dbl_main.core.pipeline import Pipeline
from dbl_main.policies.base import Policy
from dbl_main.policies.rate_limit import RateLimitPolicy
from dbl_main.policies.content_safety import ContentSafetyPolicy


# Mark all tests as fuzz tests and skip if hypothesis not installed
pytestmark = [
    pytest.mark.fuzz,
    pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed"),
]


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

if HYPOTHESIS_AVAILABLE:
    # Safe text that won't break anything
    safe_text = st.text(
        alphabet=st.characters(
            whitelist_categories=("L", "N", "P", "S", "Z"),
            blacklist_characters="\x00",
        ),
        min_size=0,
        max_size=100,
    )
    
    # Non-empty text for required fields
    non_empty_text = st.text(
        alphabet=st.characters(
            whitelist_categories=("L", "N"),
        ),
        min_size=1,
        max_size=50,
    )
    
    # Simple metadata values
    simple_value = st.one_of(
        st.text(max_size=50),
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.booleans(),
        st.none(),
    )
    
    # Metadata dict
    metadata_strategy = st.dictionaries(
        keys=st.text(min_size=1, max_size=20, alphabet="abcdefghijklmnopqrstuvwxyz_"),
        values=simple_value,
        max_size=20,
    )
    
    # PsiDefinition strategy
    psi_strategy = st.builds(
        PsiDefinition,
        psi_type=non_empty_text,
        name=non_empty_text,
        metadata=metadata_strategy,
    )
    
    # BoundaryContext strategy
    context_strategy = st.builds(
        BoundaryContext,
        psi=psi_strategy,
        caller_id=st.one_of(st.none(), safe_text),
        tenant_id=st.one_of(st.none(), safe_text),
        channel=st.one_of(st.none(), safe_text),
        metadata=metadata_strategy,
    )
else:
    # Dummy strategies when hypothesis not available
    context_strategy = None
    safe_text = None
    non_empty_text = None
    simple_value = None
    metadata_strategy = None
    psi_strategy = None


# ---------------------------------------------------------------------------
# Helper policies for fuzz tests
# ---------------------------------------------------------------------------

class AllowPolicy(Policy):
    @property
    def name(self) -> str:
        return "allow"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(outcome="allow", reason="allowed")


class BlockPolicy(Policy):
    @property
    def name(self) -> str:
        return "block"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(outcome="block", reason="blocked")


class ModifyPolicy(Policy):
    @property
    def name(self) -> str:
        return "modify"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(
            outcome="modify",
            reason="modified",
            modified_metadata={"fuzz_added": True},
        )


# ---------------------------------------------------------------------------
# Fuzz tests
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=200, suppress_health_check=[HealthCheck.too_slow], deadline=None)
def test_empty_pipeline_never_crashes(ctx: BoundaryContext):
    """Empty pipeline handles any context without crashing."""
    pipeline = Pipeline(name="empty", policies=[])
    result = pipeline.evaluate(ctx)
    
    assert result is not None
    assert result.final_outcome == "allow"
    assert result.context is ctx


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=200)
def test_allow_policy_never_crashes(ctx: BoundaryContext):
    """Allow policy handles any context without crashing."""
    pipeline = Pipeline(name="allow", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result is not None
    assert result.is_allowed()
    assert result.final_outcome == "allow"


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=200)
def test_block_policy_never_crashes(ctx: BoundaryContext):
    """Block policy handles any context without crashing."""
    pipeline = Pipeline(name="block", policies=[BlockPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result is not None
    assert not result.is_allowed()
    assert result.final_outcome == "block"


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=200)
def test_modify_policy_never_crashes(ctx: BoundaryContext):
    """Modify policy handles any context without crashing."""
    pipeline = Pipeline(name="modify", policies=[ModifyPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result is not None
    assert result.is_allowed()
    assert result.effective_metadata.get("fuzz_added") is True


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=200)
def test_rate_limit_policy_never_crashes(ctx: BoundaryContext):
    """RateLimitPolicy handles any context without crashing."""
    policy = RateLimitPolicy(max_requests=100)
    pipeline = Pipeline(name="rate", policies=[policy])
    result = pipeline.evaluate(ctx)
    
    assert result is not None
    assert result.final_outcome in ("allow", "modify", "block")


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=200)
def test_content_safety_policy_never_crashes(ctx: BoundaryContext):
    """ContentSafetyPolicy handles any context without crashing."""
    policy = ContentSafetyPolicy(blocked_patterns=["forbidden", "blocked"])
    pipeline = Pipeline(name="content", policies=[policy])
    result = pipeline.evaluate(ctx)
    
    assert result is not None
    assert result.final_outcome in ("allow", "modify", "block")


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=200)
def test_multi_policy_pipeline_never_crashes(ctx: BoundaryContext):
    """Multi-policy pipeline handles any context without crashing."""
    pipeline = Pipeline(
        name="multi",
        policies=[
            AllowPolicy(),
            ModifyPolicy(),
            RateLimitPolicy(max_requests=100),
            ContentSafetyPolicy(blocked_patterns=[]),
        ],
    )
    result = pipeline.evaluate(ctx)
    
    assert result is not None
    assert result.final_outcome in ("allow", "modify", "block")


# ---------------------------------------------------------------------------
# Invariant tests
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=200)
def test_invariant_context_unchanged(ctx: BoundaryContext):
    """Context is never mutated by pipeline."""
    # Snapshot
    original_caller = ctx.caller_id
    original_tenant = ctx.tenant_id
    original_channel = ctx.channel
    original_psi_name = ctx.psi.name
    original_metadata = dict(ctx.metadata)
    
    pipeline = Pipeline(
        name="test",
        policies=[AllowPolicy(), ModifyPolicy()],
    )
    pipeline.evaluate(ctx)
    
    # Verify unchanged
    assert ctx.caller_id == original_caller
    assert ctx.tenant_id == original_tenant
    assert ctx.channel == original_channel
    assert ctx.psi.name == original_psi_name
    assert dict(ctx.metadata) == original_metadata


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=200)
def test_invariant_effective_metadata_independent(ctx: BoundaryContext):
    """effective_metadata is independent copy."""
    pipeline = Pipeline(name="test", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    # effective_metadata is not the same object
    assert result.effective_metadata is not ctx.metadata


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=200)
def test_invariant_decisions_count_matches_policies(ctx: BoundaryContext):
    """Number of decisions <= number of policies (stops on block)."""
    policies = [AllowPolicy(), AllowPolicy(), AllowPolicy()]
    pipeline = Pipeline(name="test", policies=policies)
    result = pipeline.evaluate(ctx)
    
    assert len(result.decisions) <= len(policies)


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=200)
def test_invariant_block_stops_pipeline(ctx: BoundaryContext):
    """Block policy stops further evaluation."""
    policies = [BlockPolicy(), AllowPolicy(), AllowPolicy()]
    pipeline = Pipeline(name="test", policies=policies)
    result = pipeline.evaluate(ctx)
    
    # Only one decision (the block)
    assert len(result.decisions) == 1
    assert result.final_outcome == "block"


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(ctx=context_strategy)
@settings(max_examples=100)
def test_invariant_deterministic(ctx: BoundaryContext):
    """Same input produces same output."""
    pipeline = Pipeline(
        name="test",
        policies=[AllowPolicy(), ModifyPolicy()],
    )
    
    result1 = pipeline.evaluate(ctx)
    result2 = pipeline.evaluate(ctx)
    
    assert result1.final_outcome == result2.final_outcome
    assert result1.effective_psi.describe() == result2.effective_psi.describe()
    assert dict(result1.effective_metadata) == dict(result2.effective_metadata)


# ---------------------------------------------------------------------------
# Edge case strategies
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(
    psi_type=st.text(min_size=0, max_size=100),
    name=st.text(min_size=0, max_size=100),
)
@settings(max_examples=100)
def test_psi_with_any_strings(psi_type: str, name: str):
    """PsiDefinition with arbitrary strings doesn't crash pipeline."""
    # Skip truly empty strings that would fail PsiDefinition
    assume(len(psi_type) > 0 or len(name) > 0)
    
    try:
        psi = PsiDefinition(psi_type=psi_type or "default", name=name or "default")
        ctx = BoundaryContext(psi=psi)
        
        pipeline = Pipeline(name="test", policies=[AllowPolicy()])
        result = pipeline.evaluate(ctx)
        
        assert result is not None
    except (ValueError, TypeError):
        # Some string combinations may be invalid
        pass


@pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")
@given(
    num_policies=st.integers(min_value=0, max_value=50),
)
@settings(max_examples=50)
def test_arbitrary_pipeline_length(num_policies: int):
    """Pipeline with arbitrary number of policies works."""
    policies = [AllowPolicy() for _ in range(num_policies)]
    pipeline = Pipeline(name="test", policies=policies)
    
    psi = PsiDefinition(psi_type="test", name="op")
    ctx = BoundaryContext(psi=psi)
    
    result = pipeline.evaluate(ctx)
    
    assert result is not None
    assert len(result.decisions) == num_policies
    assert result.final_outcome == "allow"

