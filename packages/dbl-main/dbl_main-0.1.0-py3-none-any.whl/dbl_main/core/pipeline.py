# pipeline.py
#
# Pipeline engine for policy orchestration.

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence, TYPE_CHECKING

from dbl_core import BoundaryContext, BoundaryResult, PolicyDecision

if TYPE_CHECKING:
    from ..policies.base import Policy


@dataclass
class Pipeline:
    """
    Ordered sequence of policies to evaluate.
    
    Evaluates each policy in order, aggregates decisions,
    and returns a final BoundaryResult.
    """
    
    name: str
    policies: Sequence[Policy] = field(default_factory=list)
    config: Mapping[str, Any] = field(default_factory=dict)
    
    def evaluate(self, context: BoundaryContext) -> BoundaryResult:
        """
        Run all policies and aggregate to a BoundaryResult.
        
        Stops on first "block" decision.
        """
        decisions: list[PolicyDecision] = []
        final_outcome = "allow"
        effective_psi = context.psi
        effective_metadata = copy.deepcopy(context.metadata) if context.metadata else {}
        
        for policy in self.policies:
            decision = policy.evaluate(context)
            decisions.append(decision)
            
            # Apply modifications
            if decision.modified_psi is not None:
                effective_psi = decision.modified_psi
            if decision.modified_metadata is not None:
                effective_metadata.update(decision.modified_metadata)
            
            # Block stops pipeline
            if decision.outcome == "block":
                final_outcome = "block"
                break
            
            # Modify is cumulative
            if decision.outcome == "modify":
                final_outcome = "modify"
        
        return BoundaryResult(
            context=context,
            decisions=decisions,
            final_outcome=final_outcome,
            effective_psi=effective_psi,
            effective_metadata=effective_metadata,
        )
    
    def add_policy(self, policy: Policy) -> None:
        """Add a policy to the pipeline."""
        self.policies = list(self.policies) + [policy]

