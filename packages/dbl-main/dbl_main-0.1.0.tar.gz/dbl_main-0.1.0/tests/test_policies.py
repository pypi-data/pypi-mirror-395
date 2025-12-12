# test_policies.py

from dbl_core import BoundaryContext
from kl_kernel_logic import PsiDefinition

from dbl_main.policies.rate_limit import RateLimitPolicy
from dbl_main.policies.content_safety import ContentSafetyPolicy


def test_rate_limit_no_checker_allows():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, caller_id="user-1")
    
    policy = RateLimitPolicy(max_requests=10)
    decision = policy.evaluate(ctx)
    
    assert decision.outcome == "allow"


def test_rate_limit_blocks_when_exceeded():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, caller_id="user-1")
    
    def rate_checker(caller_id: str, window: int) -> int:
        return 100  # already at limit
    
    policy = RateLimitPolicy(max_requests=10, rate_checker=rate_checker)
    decision = policy.evaluate(ctx)
    
    assert decision.outcome == "block"


def test_content_safety_no_content_allows():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={})
    
    policy = ContentSafetyPolicy()
    decision = policy.evaluate(ctx)
    
    assert decision.outcome == "allow"


def test_content_safety_blocks_pattern():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={"prompt": "hello BLOCKED_WORD world"})
    
    policy = ContentSafetyPolicy(blocked_patterns=["blocked_word"])
    decision = policy.evaluate(ctx)
    
    assert decision.outcome == "block"


def test_content_safety_allows_clean():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={"prompt": "hello world"})
    
    policy = ContentSafetyPolicy(blocked_patterns=["blocked_word"])
    decision = policy.evaluate(ctx)
    
    assert decision.outcome == "allow"

