from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.validate_intake_context_bundle_review import (
    IntakeContextBundleReviewError,
    validate_intake_context_bundle_review,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "intake-context-bundle-review-registry.json"
VALIDATOR = ROOT / "scripts" / "validate_intake_context_bundle_review.py"


def _registry_payload() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_intake_context_bundle_review_registry_validates() -> None:
    data = validate_intake_context_bundle_review()

    assert data["status"] == "candidate_review_only"
    assert data["non_authoritative"] is True
    assert data["raw_legal_payload_storage_authorized"] is False
    assert data["canonical_schema_or_registry_authority_assigned"] is False


def test_intake_context_bundle_review_validator_cli_passes() -> None:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "validation passed" in completed.stdout


def test_interface_requires_source_bound_reference_families() -> None:
    data = _registry_payload()
    item = next(
        review
        for review in data["review_items"]
        if review["source_proposal_id"] == "lkr.intake-context-bundle-interface.v0_1"
    )

    assert "source_ref" in item["required_context_ref_families"]
    assert "passage_ref" in item["required_context_ref_families"]
    assert "claim_ref" in item["required_context_ref_families"]
    assert "retrieval_trace" in item["required_context_ref_families"]
    assert "context_bundle" in item["required_context_ref_families"]
    assert "source_hash" in item["required_source_bound_fields"]
    assert "text_sha256" in item["required_source_bound_fields"]
    assert item["required_boundary_controls"]["raw_payload_storage_allowed"] is False
    assert item["required_boundary_controls"]["context_bundle_is_legal_truth"] is False


def test_labor_employment_context_keeps_unknowns_and_budget_drivers() -> None:
    data = _registry_payload()
    item = next(
        review
        for review in data["review_items"]
        if review["source_proposal_id"] == "lkr.labor-employment-budget-context.v0_1"
    )

    assert "unknown_entity_candidate" in item["candidate_entity_types"]
    assert "unknown_role_candidate" in item["candidate_role_types"]
    assert "unknown_relationship_candidate" in item["candidate_relationship_types"]
    assert "employment_relationship_candidate" in item["candidate_relationship_types"]
    assert (
        "joint_employer_or_integrated_enterprise_candidate"
        in item["candidate_relationship_types"]
    )
    assert (
        "class_or_collective_action_signal" in item["candidate_budget_driver_signals"]
    )
    assert (
        "document_volume_and_ediscovery_scale"
        in item["candidate_budget_driver_signals"]
    )
    assert item["required_evidence_controls"]["source_ref_required"] is True
    assert (
        item["required_evidence_controls"][
            "context_priors_separate_from_observed_facts"
        ]
        is True
    )


def test_missing_info_context_blocks_or_widens_without_invented_assumptions() -> None:
    data = _registry_payload()
    item = next(
        review
        for review in data["review_items"]
        if review["source_proposal_id"] == "lkr.intake-missing-info-context.v0_1"
    )

    assert "party_role_ambiguous" in item["candidate_missing_info_categories"]
    assert "document_volume_unknown" in item["candidate_missing_info_categories"]
    assert (
        "carrier_guideline_or_rate_constraint_unknown"
        in item["candidate_missing_info_categories"]
    )
    assert "budget_effect" in item["required_handoff_fields"]
    assert item["required_boundary_controls"]["budget_may_be_blocked"] is True
    assert (
        item["required_boundary_controls"][
            "default_assumption_without_evidence_allowed"
        ]
        is False
    )


def test_validator_rejects_missing_unknown_role(tmp_path: Path) -> None:
    data = _registry_payload()
    item = next(
        review
        for review in data["review_items"]
        if review["source_proposal_id"] == "lkr.labor-employment-budget-context.v0_1"
    )
    item["candidate_role_types"].remove("unknown_role_candidate")
    bad_registry = tmp_path / "bad_registry.json"
    bad_registry.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(IntakeContextBundleReviewError, match="unknown_role_candidate"):
        validate_intake_context_bundle_review(bad_registry)
