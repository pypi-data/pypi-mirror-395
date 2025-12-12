# test_pipeline.py

from dbl_core import BoundaryContext, PolicyDecision
from kl_kernel_logic import PsiDefinition

from dbl_main.core.pipeline import Pipeline
from dbl_main.policies.base import Policy


class AllowPolicy(Policy):
    @property
    def name(self) -> str:
        return "allow-all"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(outcome="allow", reason="allowed")


class BlockPolicy(Policy):
    @property
    def name(self) -> str:
        return "block-all"
    
    def evaluate(self, context: BoundaryContext) -> PolicyDecision:
        return PolicyDecision(outcome="block", reason="blocked")


def test_pipeline_all_allow():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, caller_id="user-1")
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy(), AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.final_outcome == "allow"
    assert len(result.decisions) == 2


def test_pipeline_stops_on_block():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, caller_id="user-1")
    
    pipeline = Pipeline(name="test", policies=[AllowPolicy(), BlockPolicy(), AllowPolicy()])
    result = pipeline.evaluate(ctx)
    
    assert result.final_outcome == "block"
    assert len(result.decisions) == 2  # stopped at block


def test_pipeline_empty():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    pipeline = Pipeline(name="empty", policies=[])
    result = pipeline.evaluate(ctx)
    
    assert result.final_outcome == "allow"
    assert len(result.decisions) == 0

