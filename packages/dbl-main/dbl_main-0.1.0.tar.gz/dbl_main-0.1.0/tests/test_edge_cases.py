# test_edge_cases.py
#
# Edge-case pipeline tests.
#
# Focus:
# - Empty pipelines
# - Single policy pipelines
# - Very long pipelines
# - Unusual metadata structures
# - Boundary values

import pytest
from dbl_core import BoundaryContext, PolicyDecision
from kl_kernel_logic import PsiDefinition

from dbl_main.core.pipeline import Pipeline
from dbl_main.policies.base import Policy


# ---------------------------------------------------------------------------
# Helper policies
# ---------------------------------------------------------------------------

class AllowPolicy(Policy):
    def __init__(self, name: str = "allow"):
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(outcome="allow", reason=f"{self._name} passed")


class BlockPolicy(Policy):
    def __init__(self, name: str = "block"):
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(outcome="block", reason=f"{self._name} blocked")


class ModifyPolicy(Policy):
    def __init__(self, key: str, value: str):
        self._key = key
        self._value = value
    
    @property
    def name(self) -> str:
        return f"modify-{self._key}"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(
            outcome="modify",
            reason=f"added {self._key}",
            modified_metadata={self._key: self._value},
        )


# ---------------------------------------------------------------------------
# Empty and minimal pipelines
# ---------------------------------------------------------------------------

def test_empty_pipeline_allows():
    """Empty pipeline with no policies should allow."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(name="empty", policies=[])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert result.final_outcome == "allow"
    assert len(result.decisions) == 0


def test_single_allow_policy():
    """Single allow policy."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(name="single", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert len(result.decisions) == 1


def test_single_block_policy():
    """Single block policy."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(name="single", policies=[BlockPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert not result.is_allowed()
    assert result.final_outcome == "block"
    assert len(result.decisions) == 1


def test_single_modify_policy():
    """Single modify policy."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={"original": True})
    
    pipeline = Pipeline(name="single", policies=[ModifyPolicy("added", "value")])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert result.final_outcome == "modify"
    assert result.effective_metadata["added"] == "value"
    assert result.effective_metadata["original"] is True


# ---------------------------------------------------------------------------
# Long pipelines
# ---------------------------------------------------------------------------

def test_long_pipeline_all_allow():
    """Pipeline with many allow policies."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    num_policies = 100
    policies = [AllowPolicy(f"allow-{i}") for i in range(num_policies)]
    
    pipeline = Pipeline(name="long", policies=policies)
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert len(result.decisions) == num_policies


def test_long_pipeline_block_at_end():
    """Pipeline with block at the very end."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    policies = [AllowPolicy(f"allow-{i}") for i in range(99)]
    policies.append(BlockPolicy("final-block"))
    
    pipeline = Pipeline(name="long", policies=policies)
    result = pipeline.evaluate(ctx)
    
    assert not result.is_allowed()
    assert result.final_outcome == "block"
    assert len(result.decisions) == 100


def test_long_pipeline_block_at_start():
    """Pipeline with block at the very start."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    policies = [BlockPolicy("first-block")]
    policies.extend([AllowPolicy(f"allow-{i}") for i in range(99)])
    
    pipeline = Pipeline(name="long", policies=policies)
    result = pipeline.evaluate(ctx)
    
    assert not result.is_allowed()
    assert len(result.decisions) == 1  # Stopped at first


def test_long_pipeline_many_modifications():
    """Pipeline with many modify policies accumulating metadata."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={"base": True})
    
    num_policies = 50
    policies = [ModifyPolicy(f"key_{i}", f"value_{i}") for i in range(num_policies)]
    
    pipeline = Pipeline(name="long", policies=policies)
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert result.final_outcome == "modify"
    assert len(result.decisions) == num_policies
    
    # All modifications accumulated
    for i in range(num_policies):
        assert result.effective_metadata[f"key_{i}"] == f"value_{i}"
    
    # Original preserved
    assert result.effective_metadata["base"] is True


# ---------------------------------------------------------------------------
# Unusual metadata structures
# ---------------------------------------------------------------------------

def test_empty_metadata():
    """Empty metadata dict."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={})
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert result.effective_metadata == {}


def test_deeply_nested_metadata():
    """Deeply nested metadata structure."""
    psi = PsiDefinition(psi_type="test", name="op1")
    
    nested = {"level": 0}
    current = nested
    for i in range(1, 20):
        current["child"] = {"level": i}
        current = current["child"]
    
    ctx = BoundaryContext(psi=psi, metadata=nested)
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    
    # Verify deep structure preserved
    current = result.effective_metadata
    for i in range(20):
        assert current["level"] == i
        if i < 19:
            current = current["child"]


def test_metadata_with_various_types():
    """Metadata with various Python types."""
    psi = PsiDefinition(psi_type="test", name="op1")
    
    metadata = {
        "string": "hello",
        "int": 42,
        "float": 3.14,
        "bool_true": True,
        "bool_false": False,
        "none": None,
        "list": [1, 2, 3],
        "dict": {"a": 1, "b": 2},
        "nested_list": [[1, 2], [3, 4]],
        "empty_list": [],
        "empty_dict": {},
    }
    
    ctx = BoundaryContext(psi=psi, metadata=metadata)
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert result.effective_metadata["string"] == "hello"
    assert result.effective_metadata["int"] == 42
    assert result.effective_metadata["float"] == 3.14
    assert result.effective_metadata["bool_true"] is True
    assert result.effective_metadata["bool_false"] is False
    assert result.effective_metadata["none"] is None
    assert result.effective_metadata["list"] == [1, 2, 3]
    assert result.effective_metadata["dict"] == {"a": 1, "b": 2}


def test_metadata_with_unicode():
    """Metadata with unicode strings."""
    psi = PsiDefinition(psi_type="test", name="op1")
    
    metadata = {
        "german": "Größe",
        "chinese": "你好",
        "emoji": "🚀",
        "mixed": "Hello 世界 🌍",
    }
    
    ctx = BoundaryContext(psi=psi, metadata=metadata)
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert result.effective_metadata["german"] == "Größe"
    assert result.effective_metadata["chinese"] == "你好"
    assert result.effective_metadata["emoji"] == "🚀"


def test_large_metadata_value():
    """Metadata with very large string value."""
    psi = PsiDefinition(psi_type="test", name="op1")
    
    large_string = "x" * 100_000  # 100KB string
    metadata = {"large": large_string}
    
    ctx = BoundaryContext(psi=psi, metadata=metadata)
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert len(result.effective_metadata["large"]) == 100_000


# ---------------------------------------------------------------------------
# Boundary values for context fields
# ---------------------------------------------------------------------------

def test_empty_string_fields():
    """Context with empty string fields."""
    psi = PsiDefinition(psi_type="", name="")
    ctx = BoundaryContext(
        psi=psi,
        caller_id="",
        tenant_id="",
        channel="",
    )
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert result.context.caller_id == ""
    assert result.context.tenant_id == ""


def test_none_optional_fields():
    """Context with None for optional fields."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(
        psi=psi,
        caller_id=None,
        tenant_id=None,
        channel=None,
    )
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert result.context.caller_id is None
    assert result.context.tenant_id is None


def test_very_long_string_fields():
    """Context with very long string fields."""
    psi = PsiDefinition(psi_type="test", name="op1")
    
    long_id = "x" * 10_000
    ctx = BoundaryContext(
        psi=psi,
        caller_id=long_id,
        tenant_id=long_id,
        channel=long_id,
    )
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert len(result.context.caller_id) == 10_000


# ---------------------------------------------------------------------------
# PsiDefinition edge cases
# ---------------------------------------------------------------------------

def test_psi_with_large_metadata():
    """PsiDefinition with large metadata."""
    psi = PsiDefinition(
        psi_type="test",
        name="op1",
        metadata={f"key_{i}": f"value_{i}" for i in range(1000)},
    )
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert len(result.effective_psi.metadata) == 1000


def test_psi_modification_preserves_original():
    """Modifying psi in result does not affect original."""
    original_psi = PsiDefinition(psi_type="test", name="original")
    ctx = BoundaryContext(psi=original_psi)
    
    class PsiModifyPolicy(Policy):
        @property
        def name(self) -> str:
            return "psi-modify"
        
        def evaluate(self, context: BoundaryContext) -> PolicyDecision:
            new_psi = PsiDefinition(psi_type="modified", name="new-name")
            return PolicyDecision(
                outcome="modify",
                reason="changed psi",
                modified_psi=new_psi,
            )
    
    pipeline = Pipeline(name="test", policies=[PsiModifyPolicy()])
    result = pipeline.evaluate(ctx)
    
    # Result has new psi
    assert result.effective_psi.name == "new-name"
    assert result.effective_psi.psi_type == "modified"
    
    # Original unchanged
    assert original_psi.name == "original"
    assert original_psi.psi_type == "test"
    assert ctx.psi.name == "original"


# ---------------------------------------------------------------------------
# Policy ordering edge cases
# ---------------------------------------------------------------------------

def test_modify_then_block():
    """Modify policy followed by block - modifications discarded."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(
        name="test",
        policies=[
            ModifyPolicy("added", "value"),
            BlockPolicy(),
        ],
    )
    result = pipeline.evaluate(ctx)
    
    assert not result.is_allowed()
    assert result.final_outcome == "block"
    # Modifications still in effective_metadata even though blocked
    assert result.effective_metadata.get("added") == "value"


def test_block_then_modify_never_reached():
    """Block first - modify never evaluated."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(
        name="test",
        policies=[
            BlockPolicy(),
            ModifyPolicy("never", "reached"),
        ],
    )
    result = pipeline.evaluate(ctx)
    
    assert not result.is_allowed()
    assert len(result.decisions) == 1
    assert "never" not in result.effective_metadata


def test_alternating_allow_modify():
    """Alternating allow and modify policies."""
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(
        name="test",
        policies=[
            AllowPolicy("a1"),
            ModifyPolicy("m1", "v1"),
            AllowPolicy("a2"),
            ModifyPolicy("m2", "v2"),
            AllowPolicy("a3"),
        ],
    )
    result = pipeline.evaluate(ctx)
    
    assert result.is_allowed()
    assert result.final_outcome == "modify"  # Last modify wins for outcome
    assert result.effective_metadata["m1"] == "v1"
    assert result.effective_metadata["m2"] == "v2"
    assert len(result.decisions) == 5

