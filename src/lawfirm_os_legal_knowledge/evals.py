"""Synthetic/private eval helpers for Legal Knowledge Runtime.

These helpers intentionally do not call models, browsers, networks, or live connectors.
They validate local eval fixture shape and produce simple outcome records that can be
attached to evidence packets or Exception Lake events by higher layers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RetrievalEvalOutcome:
    eval_case_id: str
    passed: bool
    missing_expected_refs: tuple[str, ...]
    forbidden_refs_present: tuple[str, ...]


def grade_retrieval_refs(eval_case: dict[str, Any], actual_refs: list[str]) -> RetrievalEvalOutcome:
    """Grade final retrieved refs against a synthetic eval case.

    This intentionally grades the final bundle/ref set, not an agent transcript.
    """
    if eval_case.get("schema_id") != "legal_retrieval_eval_case.v1":
        raise ValueError("unsupported eval case schema_id")
    if eval_case.get("synthetic") is not True:
        raise ValueError("legal retrieval eval cases must be synthetic in MVP")

    actual = set(actual_refs)
    expected = set(eval_case.get("expected_source_refs", []))
    forbidden = set(eval_case.get("must_not_include_source_refs", []))
    missing = tuple(sorted(expected - actual))
    forbidden_present = tuple(sorted(forbidden & actual))
    return RetrievalEvalOutcome(
        eval_case_id=eval_case["eval_case_id"],
        passed=not missing and not forbidden_present,
        missing_expected_refs=missing,
        forbidden_refs_present=forbidden_present,
    )
