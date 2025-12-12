# tests/test_dbl_core_stress.py

import concurrent.futures
import pytest

from dbl_core import BoundaryContext, DBLCore
from kl_kernel_logic import PsiDefinition


@pytest.mark.stress
def test_dbl_core_deterministic_under_repeated_calls() -> None:
    psi = PsiDefinition(psi_type="test", name="op1")
    ctx = BoundaryContext(
        psi=psi,
        caller_id="user-1",
        tenant_id="tenant-1",
        channel="api",
        metadata={"key": "value", "nested": {"a": 1}},
    )

    core = DBLCore(config={"limit.default": 100})

    first = core.evaluate(ctx)
    first_desc = first.describe()

    # no alias on the original
    assert first.effective_metadata is not ctx.metadata

    num_iterations = 1000

    for _ in range(num_iterations):
        result = core.evaluate(ctx)
        desc = result.describe()

        assert result.final_outcome == first.final_outcome
        assert result.effective_psi.describe() == first.effective_psi.describe()
        assert desc == first_desc

        # context remains stable
        assert ctx.metadata["nested"]["a"] == 1
        assert ctx.tenant_id == "tenant-1"


@pytest.mark.stress
def test_dbl_core_handles_large_metadata() -> None:
    psi = PsiDefinition(psi_type="test", name="large_meta_op")

    big_metadata = {
        f"key_{i}": {
            "index": i,
            "flags": [True, False, True],
            "text": "x" * 100,
        }
        for i in range(1000)
    }

    ctx = BoundaryContext(
        psi=psi,
        caller_id="user-big",
        metadata=big_metadata,
    )

    core = DBLCore(config={"max_keys": 2000})

    result = core.evaluate(ctx)

    assert result.is_allowed() is True
    assert result.effective_metadata is not big_metadata
    assert len(result.effective_metadata) == len(big_metadata)


@pytest.mark.stress
def test_dbl_core_thread_safety() -> None:
    psi = PsiDefinition(psi_type="test", name="parallel_op")

    core = DBLCore(config={"mode": "parallel-test"})

    def worker(idx: int):
        ctx = BoundaryContext(
            psi=psi,
            caller_id=f"user-{idx}",
            tenant_id="tenant-1",
            channel="api",
            metadata={"idx": idx},
        )
        result = core.evaluate(ctx)
        return result.final_outcome, result.effective_metadata.get("idx")

    num_tasks = 200

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(worker, i) for i in range(num_tasks)]
        results = [f.result() for f in futures]

    seen = set()
    for outcome, idx in results:
        assert outcome == "allow"
        assert idx is not None
        seen.add(idx)

    assert len(seen) == num_tasks


# Optional: hypothesis-based test (runs if hypothesis is installed)
try:
    from hypothesis import given, strategies as st

    @pytest.mark.stress
    @given(
        psi_type=st.text(min_size=1, max_size=20),
        name=st.text(min_size=1, max_size=30),
        caller_id=st.one_of(st.none(), st.text(min_size=1, max_size=30)),
    )
    def test_dbl_core_never_crashes_on_random_input(
        psi_type: str,
        name: str,
        caller_id: str | None,
    ) -> None:
        psi = PsiDefinition(psi_type=psi_type, name=name)
        ctx = BoundaryContext(psi=psi, caller_id=caller_id)

        core = DBLCore()
        result = core.evaluate(ctx)

        assert result.final_outcome in ("allow", "modify", "block")

except ImportError:
    pass
