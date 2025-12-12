# dbl_core.py

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Sequence, Literal

from kl_kernel_logic import PsiDefinition

# Type aliases for domain vocabulary
Metadata = Mapping[str, Any]
Config = Mapping[str, Any]
DecisionOutcome = Literal["allow", "modify", "block"]

ENGINE_NAME = "dbl-core"
ENGINE_VERSION = "0.2.0"


@dataclass(frozen=True)
class BoundaryContext:
    """
    Input context for DBL evaluation.
    
    Immutable. DBL Core never mutates the instance or its metadata.
    """

    psi: PsiDefinition
    caller_id: Optional[str] = None
    tenant_id: Optional[str] = None
    channel: Optional[str] = None

    metadata: Metadata = field(default_factory=dict)

    def describe(self) -> Dict[str, Any]:
        return {
            "psi": self.psi.describe(),
            "caller_id": self.caller_id,
            "tenant_id": self.tenant_id,
            "channel": self.channel,
            "metadata": dict(self.metadata),
        }

    def __repr__(self) -> str:
        return (
            f"BoundaryContext(psi={self.psi.name}, "
            f"caller_id={self.caller_id}, tenant_id={self.tenant_id})"
        )


@dataclass(frozen=True)
class PolicyDecision:
    """
    Result of a single policy evaluation step.
    
    The modified_psi and modified_metadata fields allow a policy to override
    the original values. When set, DBL Core aggregates them into the final
    effective_psi and effective_metadata in BoundaryResult.
    """

    outcome: DecisionOutcome
    reason: str
    details: Metadata = field(default_factory=dict)

    modified_psi: Optional[PsiDefinition] = None
    modified_metadata: Optional[Metadata] = None


@dataclass(frozen=True)
class BoundaryResult:
    """
    Aggregated DBL evaluation result.
    
    The effective_* fields represent the state after all policies have been applied.
    effective_metadata is a deep copy, never an alias to context.metadata.
    """

    context: BoundaryContext
    decisions: Sequence[PolicyDecision]

    final_outcome: DecisionOutcome
    effective_psi: PsiDefinition
    effective_metadata: Metadata = field(default_factory=dict)

    def is_allowed(self) -> bool:
        return self.final_outcome in ("allow", "modify")

    def describe(self) -> Dict[str, Any]:
        return {
            "engine": ENGINE_NAME,
            "engine_version": ENGINE_VERSION,
            "context": self.context.describe(),
            "decisions": [
                {
                    "outcome": d.outcome,
                    "reason": d.reason,
                    "details": dict(d.details),
                    "modified_psi": (
                        d.modified_psi.describe() if d.modified_psi else None
                    ),
                    "modified_metadata": (
                        dict(d.modified_metadata)
                        if d.modified_metadata is not None
                        else None
                    ),
                }
                for d in self.decisions
            ],
            "final_outcome": self.final_outcome,
            "effective_psi": self.effective_psi.describe(),
            "effective_metadata": dict(self.effective_metadata),
        }


class DBLCore:
    """
    Deterministic Boundary Layer Core.
    
    Pure, stateless per call. No hidden state, no side effects outside BoundaryResult.
    All policy decisions are observable via PolicyDecision and BoundaryResult.
    """

    def __init__(self, *, config: Optional[Config] = None) -> None:
        self._config: Config = dict(config) if config is not None else {}

    def describe_config(self) -> Config:
        """Return a copy of the current config for debug/audit."""
        return dict(self._config)

    def evaluate(self, context: BoundaryContext) -> BoundaryResult:
        """
        Evaluate governance and boundaries for a single operation.
        Default: allow everything.
        """

        decision = PolicyDecision(
            outcome="allow",
            reason="DBLCore default allow",
            details={
                "config_present": bool(self._config),
                "policy_chain": ["default-allow"],
            },
        )

        return BoundaryResult(
            context=context,
            decisions=[decision],
            final_outcome=decision.outcome,
            effective_psi=context.psi,
            effective_metadata=copy.deepcopy(context.metadata) if context.metadata else {},
        )
