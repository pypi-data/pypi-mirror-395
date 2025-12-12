# test_dbl_core.py

from dbl_core import (
    BoundaryContext,
    PolicyDecision,
    BoundaryResult,
    DBLCore,
)
from kl_kernel_logic import PsiDefinition


def test_boundary_context_creation():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, caller_id="user-1")

    assert ctx.psi == psi
    assert ctx.caller_id == "user-1"
    assert ctx.tenant_id is None


def test_boundary_context_describe():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, caller_id="user-1")

    desc = ctx.describe()
    assert desc["caller_id"] == "user-1"
    assert "psi" in desc


def test_dbl_core_default_allows():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)

    core = DBLCore()
    result = core.evaluate(ctx)

    assert isinstance(result, BoundaryResult)
    assert result.final_outcome == "allow"
    assert result.is_allowed() is True
    assert result.effective_psi == psi


def test_policy_decision_immutable():
    decision = PolicyDecision(outcome="allow", reason="test")

    assert decision.outcome == "allow"
    assert decision.reason == "test"


def test_boundary_result_describe():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi)

    core = DBLCore()
    result = core.evaluate(ctx)

    desc = result.describe()
    assert desc["final_outcome"] == "allow"
    assert "decisions" in desc
    assert len(desc["decisions"]) == 1


def test_dbl_core_describe_config_returns_copy():
    cfg = {"limit.default": 100}
    core = DBLCore(config=cfg)

    desc = core.describe_config()
    assert desc == cfg
    assert desc is not cfg


def test_boundary_result_describe_is_pure():
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(psi=psi, metadata={"a": {"b": 1}})
    core = DBLCore()
    result = core.evaluate(ctx)

    d1 = result.describe()
    d2 = result.describe()
    assert d1 == d2

