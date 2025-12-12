# test_audit.py

from dbl_core import BoundaryContext, BoundaryResult, PolicyDecision
from kl_kernel_logic import PsiDefinition

from dbl_main.audit.logger import AuditLogger


def test_audit_logger_logs_result():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, caller_id="user-1")
    
    result = BoundaryResult(
        context=ctx,
        decisions=[PolicyDecision(outcome="allow", reason="test")],
        final_outcome="allow",
        effective_psi=psi,
        effective_metadata={},
    )
    
    logger = AuditLogger()
    logger.log(result)
    
    records = logger.get_records()
    assert len(records) == 1
    assert "timestamp" in records[0]
    assert records[0]["result"]["final_outcome"] == "allow"


def test_audit_logger_logs_with_extra():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    result = BoundaryResult(
        context=ctx,
        decisions=[],
        final_outcome="allow",
        effective_psi=psi,
        effective_metadata={},
    )
    
    logger = AuditLogger()
    logger.log(result, extra={"request_id": "abc123"})
    
    records = logger.get_records()
    assert records[0]["extra"]["request_id"] == "abc123"


def test_audit_logger_clear():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    result = BoundaryResult(
        context=ctx,
        decisions=[],
        final_outcome="allow",
        effective_psi=psi,
        effective_metadata={},
    )
    
    logger = AuditLogger()
    logger.log(result)
    logger.log(result)
    
    assert len(logger.get_records()) == 2
    
    logger.clear()
    
    assert len(logger.get_records()) == 0


def test_audit_logger_custom_writer():
    captured = []
    
    def custom_writer(record):
        captured.append(record)
    
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)
    
    result = BoundaryResult(
        context=ctx,
        decisions=[],
        final_outcome="block",
        effective_psi=psi,
        effective_metadata={},
    )
    
    logger = AuditLogger(writer=custom_writer)
    logger.log(result)
    
    assert len(captured) == 1
    assert captured[0]["result"]["final_outcome"] == "block"

