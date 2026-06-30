#!/usr/bin/env python3
"""Validate the candidate intake context-bundle review docket."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry" / "intake-context-bundle-review-registry.json"
EXPECTED_SOURCE_PROPOSAL_IDS = {
    "lkr.intake-context-bundle-interface.v0_1",
    "lkr.labor-employment-budget-context.v0_1",
    "lkr.intake-missing-info-context.v0_1",
}
REQUIRED_PROHIBITED_ACTIONS = {
    "semantic_substrate_write",
    "raw_legal_payload_storage",
    "real_data_ingestion",
    "production_connector_write",
}
REQUIRED_BOUNDARY_FALSE = {
    "raw_payload_storage_allowed",
    "real_data_authorized_now",
    "external_write_authorized_now",
}
REQUIRED_CONTEXT_REF_FAMILIES = {
    "source_ref",
    "passage_ref",
    "claim_ref",
    "coverage_record",
    "verification_record",
    "retrieval_trace",
    "context_bundle",
}
REQUIRED_SOURCE_BOUND_FIELDS = {
    "source_ref_id",
    "source_id",
    "source_hash",
    "content_hash",
    "passage_ref_id",
    "text_sha256",
    "claim_ref_id",
    "claim_text_hash",
    "retrieval_trace_id",
    "context_bundle_id",
    "contract_surface_sha256",
}
REQUIRED_ENTITY_TYPES = {
    "natural_person_candidate",
    "organization_candidate",
    "government_agency_candidate",
    "insurer_or_carrier_candidate",
    "union_or_labor_organization_candidate",
    "unknown_entity_candidate",
}
REQUIRED_ROLE_TYPES = {
    "represented_client_candidate",
    "adverse_party_candidate",
    "employer_candidate",
    "employee_candidate",
    "manager_or_supervisor_candidate",
    "opposing_counsel_candidate",
    "court_or_agency_candidate",
    "unknown_role_candidate",
}
REQUIRED_RELATIONSHIPS = {
    "employment_relationship_candidate",
    "reporting_or_supervisory_relationship_candidate",
    "joint_employer_or_integrated_enterprise_candidate",
    "union_or_collective_bargaining_relationship_candidate",
    "unknown_relationship_candidate",
}
REQUIRED_BUDGET_DRIVERS = {
    "party_count",
    "claim_count",
    "class_or_collective_action_signal",
    "administrative_charge_or_exhaustion_signal",
    "forum_or_jurisdiction",
    "document_volume_and_ediscovery_scale",
    "custodian_count_candidate",
    "witness_count_candidate",
    "damages_or_backpay_frontpay_signal",
    "deadline_or_scheduling_pressure",
}
REQUIRED_MISSING_INFO = {
    "principal_party_identity_missing",
    "entity_type_or_capacity_missing",
    "party_role_ambiguous",
    "employment_relationship_unclear",
    "claim_family_or_count_unclear",
    "case_posture_unclear",
    "deadline_or_hearing_date_unclear",
    "document_volume_unknown",
    "custodian_or_witness_count_unknown",
    "damages_or_exposure_unknown",
    "carrier_guideline_or_rate_constraint_unknown",
}


class IntakeContextBundleReviewError(ValueError):
    """Raised when the candidate intake context review docket violates boundaries."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntakeContextBundleReviewError(f"{_rel(path)} unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise IntakeContextBundleReviewError(f"{_rel(path)} must be a JSON object")
    return data


def _require_bool(data: dict[str, Any], key: str, expected: bool, label: str) -> None:
    if data.get(key) is not expected:
        raise IntakeContextBundleReviewError(f"{label}.{key} must be {expected}")


def _require_string_list(data: dict[str, Any], key: str, label: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise IntakeContextBundleReviewError(f"{label}.{key} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise IntakeContextBundleReviewError(
            f"{label}.{key} must contain only non-empty strings"
        )
    return value


def _require_contains(
    data: dict[str, Any], key: str, required: set[str], label: str
) -> set[str]:
    observed = set(_require_string_list(data, key, label))
    missing = sorted(required - observed)
    if missing:
        raise IntakeContextBundleReviewError(f"{label}.{key} missing {missing}")
    return observed


def _validate_top_level(data: dict[str, Any], label: str) -> None:
    expected = {
        "schema_version": "intake_context_bundle_review_registry.v0_1",
        "object_type": "intake_context_bundle_review_registry",
        "status": "candidate_review_only",
        "owner_repo": "LawFirm-os-legal-knowledge-runtime",
        "source_repo": "LawFirm-os-intake",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise IntakeContextBundleReviewError(f"{label}.{key} must be {value!r}")

    for key in (
        "contains_real_firm_data",
        "direct_promotion_performed",
        "external_writes_performed",
        "canonical_schema_or_registry_authority_assigned",
        "canonical_legal_taxonomy_assigned",
        "runtime_connector_authorized",
        "raw_legal_payload_storage_authorized",
        "real_data_pilot_authorized",
    ):
        _require_bool(data, key, False, label)
    _require_bool(data, "non_authoritative", True, label)

    generated = set(_require_string_list(data, "generated_from_proposal_ids", label))
    if generated != EXPECTED_SOURCE_PROPOSAL_IDS:
        raise IntakeContextBundleReviewError(
            f"{label}.generated_from_proposal_ids must be {sorted(EXPECTED_SOURCE_PROPOSAL_IDS)}"
        )


def _validate_boundary_controls(item: dict[str, Any], label: str) -> None:
    controls = item.get("required_boundary_controls")
    if not isinstance(controls, dict):
        raise IntakeContextBundleReviewError(
            f"{label}.required_boundary_controls must be an object"
        )
    for key in REQUIRED_BOUNDARY_FALSE:
        if controls.get(key) is not False:
            raise IntakeContextBundleReviewError(
                f"{label}.required_boundary_controls.{key} must be false"
            )


def _validate_common_item(item: dict[str, Any], label: str) -> None:
    if item.get("target_repo") != "LawFirm-os-legal-knowledge-runtime":
        raise IntakeContextBundleReviewError(
            f"{label}.target_repo must be Legal Knowledge Runtime"
        )
    if item.get("authority_plane") != "legal_knowledge_runtime":
        raise IntakeContextBundleReviewError(
            f"{label}.authority_plane must be legal_knowledge_runtime"
        )
    if item.get("adoption_status") != "owner_review_required":
        raise IntakeContextBundleReviewError(
            f"{label}.adoption_status must be owner_review_required"
        )
    local_label = item.get("local_review_label")
    if not isinstance(local_label, str) or not local_label.startswith(
        "legal_knowledge_runtime.local."
    ):
        raise IntakeContextBundleReviewError(
            f"{label}.local_review_label must be local-only"
        )
    prohibited = set(_require_string_list(item, "prohibited_actions", label))
    missing = sorted(REQUIRED_PROHIBITED_ACTIONS - prohibited)
    if missing:
        raise IntakeContextBundleReviewError(
            f"{label}.prohibited_actions missing {missing}"
        )
    _require_bool(item, "non_authoritative", True, label)
    _require_bool(item, "direct_promotion_performed", False, label)
    _require_bool(item, "external_writes_performed", False, label)


def _validate_interface_item(item: dict[str, Any], label: str) -> None:
    _require_contains(
        item, "required_context_ref_families", REQUIRED_CONTEXT_REF_FAMILIES, label
    )
    _require_contains(
        item, "required_source_bound_fields", REQUIRED_SOURCE_BOUND_FIELDS, label
    )
    _validate_boundary_controls(item, label)
    controls = item["required_boundary_controls"]
    if controls.get("human_review_required") is not True:
        raise IntakeContextBundleReviewError(
            f"{label}.required_boundary_controls.human_review_required must be true"
        )
    if controls.get("context_bundle_is_legal_truth") is not False:
        raise IntakeContextBundleReviewError(
            f"{label}.required_boundary_controls.context_bundle_is_legal_truth must be false"
        )
    if controls.get("canonical_schema_or_registry_authority") is not False:
        raise IntakeContextBundleReviewError(
            f"{label}.required_boundary_controls.canonical_schema_or_registry_authority must be false"
        )


def _validate_labor_employment_item(item: dict[str, Any], label: str) -> None:
    _require_contains(item, "candidate_entity_types", REQUIRED_ENTITY_TYPES, label)
    _require_contains(item, "candidate_role_types", REQUIRED_ROLE_TYPES, label)
    _require_contains(
        item, "candidate_relationship_types", REQUIRED_RELATIONSHIPS, label
    )
    _require_contains(
        item, "candidate_budget_driver_signals", REQUIRED_BUDGET_DRIVERS, label
    )
    controls = item.get("required_evidence_controls")
    if not isinstance(controls, dict):
        raise IntakeContextBundleReviewError(
            f"{label}.required_evidence_controls must be an object"
        )
    for key in (
        "source_ref_required",
        "passage_ref_required_for_observed_fact",
        "claim_ref_required_for_derived_signal",
        "unknown_option_required",
        "role_ambiguity_preserved",
        "context_priors_separate_from_observed_facts",
    ):
        if controls.get(key) is not True:
            raise IntakeContextBundleReviewError(
                f"{label}.required_evidence_controls.{key} must be true"
            )
    if controls.get("confidence_is_not_probability") is not True:
        raise IntakeContextBundleReviewError(
            f"{label}.required_evidence_controls.confidence_is_not_probability must be true"
        )


def _validate_missing_info_item(item: dict[str, Any], label: str) -> None:
    _require_contains(
        item,
        "candidate_missing_info_categories",
        REQUIRED_MISSING_INFO,
        label,
    )
    handoff = set(_require_string_list(item, "required_handoff_fields", label))
    for required in (
        "missing_info_item_id",
        "blocking_level",
        "budget_effect",
        "source_ref_ids",
        "passage_ref_ids",
        "claim_ref_ids",
        "review_question",
        "human_review_outcome_ref",
    ):
        if required not in handoff:
            raise IntakeContextBundleReviewError(
                f"{label}.required_handoff_fields missing {required}"
            )
    _validate_boundary_controls(item, label)
    controls = item["required_boundary_controls"]
    if controls.get("default_assumption_without_evidence_allowed") is not False:
        raise IntakeContextBundleReviewError(
            f"{label}.required_boundary_controls.default_assumption_without_evidence_allowed must be false"
        )


def validate_intake_context_bundle_review(path: Path = REGISTRY) -> dict[str, Any]:
    data = _read_json(path)
    label = _rel(path)
    _validate_top_level(data, label)

    items = data.get("review_items")
    if not isinstance(items, list) or len(items) != len(EXPECTED_SOURCE_PROPOSAL_IDS):
        raise IntakeContextBundleReviewError(
            f"{label}.review_items must contain exactly {len(EXPECTED_SOURCE_PROPOSAL_IDS)} items"
        )

    seen = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise IntakeContextBundleReviewError(
                f"{label}.review_items[{index}] must be an object"
            )
        item_label = f"{label}.review_items[{index}]"
        proposal_id = item.get("source_proposal_id")
        if proposal_id not in EXPECTED_SOURCE_PROPOSAL_IDS:
            raise IntakeContextBundleReviewError(
                f"{item_label}.source_proposal_id is not expected: {proposal_id!r}"
            )
        seen.add(proposal_id)
        _validate_common_item(item, item_label)
        if proposal_id == "lkr.intake-context-bundle-interface.v0_1":
            _validate_interface_item(item, item_label)
        elif proposal_id == "lkr.labor-employment-budget-context.v0_1":
            _validate_labor_employment_item(item, item_label)
        elif proposal_id == "lkr.intake-missing-info-context.v0_1":
            _validate_missing_info_item(item, item_label)

    if seen != EXPECTED_SOURCE_PROPOSAL_IDS:
        raise IntakeContextBundleReviewError(
            f"{label}.review_items missing {sorted(EXPECTED_SOURCE_PROPOSAL_IDS - seen)}"
        )
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    args = parser.parse_args(argv)

    try:
        validate_intake_context_bundle_review(args.registry)
    except IntakeContextBundleReviewError as exc:
        print(f"Intake context bundle review validation failed: {exc}", file=sys.stderr)
        return 1
    print("Intake context bundle review validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
