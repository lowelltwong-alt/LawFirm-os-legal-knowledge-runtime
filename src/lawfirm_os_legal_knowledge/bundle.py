from __future__ import annotations

from typing import Any, Sequence

from .util import new_id, utc_now


def assemble_synthetic_context_bundle(
    manifest: dict[str, Any],
    *,
    bundle_type: str,
    run_id: str,
    retrieval_trace_id: str,
    source_refs: Sequence[dict[str, Any]] = (),
    claim_refs: Sequence[dict[str, Any]] = (),
    passage_refs: Sequence[dict[str, Any]] = (),
) -> dict[str, Any]:
    docs = manifest.get("documents") or []
    if not docs:
        raise ValueError("manifest contains no documents")
    document_refs = [doc["document_ref"] for doc in docs]
    first = document_refs[0]
    passage_ids = [str(ref["passage_ref_id"]) for ref in passage_refs]
    if passage_ids:
        controlling_span_refs = [passage_ids[0]]
        related_span_refs = passage_ids[1:]
    else:
        controlling_span_refs = [f"{first}#synthetic-controlling-span"]
        related_span_refs = [f"{first}#synthetic-related-span"]
    return {
        "schema_type": "legal-context-bundle",
        "schema_version": "v1",
        "bundle_id": new_id("lkb"),
        "bundle_type": bundle_type,
        "run_id": run_id,
        "retrieval_trace_id": retrieval_trace_id,
        "access_decision_ref": manifest.get("default_access_policy_ref", "policy.synthetic-only.v1"),
        "matter_ref": None,
        "client_ref": None,
        "allowed_use": "synthetic_test_only",
        "document_refs": document_refs,
        "source_refs": [dict(ref) for ref in source_refs],
        "claim_refs": [dict(ref) for ref in claim_refs],
        "passage_refs": [dict(ref) for ref in passage_refs],
        "controlling_span_refs": controlling_span_refs,
        "related_span_refs": related_span_refs,
        "entities": {"source": "synthetic_fixture"},
        "missing_or_uncertain": ["Synthetic bundle; no production source system has been consulted."],
        "human_review_required": True,
        "created_at": utc_now(),
        "boundary_controls": {
            "bundle_is_canonical_truth": False,
            "external_source_not_canon": True,
            "may_be_used_without_human_review_for_legal_finality": False,
            "raw_document_payload_embedded": False,
            "retrieved_content_treated_as_instruction": False,
        },
    }


def build_retrieval_trace(
    manifest: dict[str, Any],
    *,
    run_id: str,
    retrieval_plan_id: str,
    retrievers_used: list[str],
    source_refs: Sequence[dict[str, Any]] = (),
    claim_refs: Sequence[dict[str, Any]] = (),
    coverage_records: Sequence[dict[str, Any]] = (),
    verification_records: Sequence[dict[str, Any]] = (),
    anomaly_records: Sequence[dict[str, Any]] = (),
    passage_refs: Sequence[dict[str, Any]] = (),
) -> dict[str, Any]:
    docs = manifest.get("documents") or []
    passage_ids = [str(p["passage_ref_id"]) for p in passage_refs]
    default_spans = [f"{doc['document_ref']}#synthetic-controlling-span" for doc in docs if doc.get("document_ref")]
    return {
        "schema_type": "legal-retrieval-trace",
        "schema_version": "v1",
        "retrieval_trace_id": new_id("lkrt"),
        "run_id": run_id,
        "retrieval_plan_id": retrieval_plan_id,
        "retrievers_used": retrievers_used,
        "source_manifest_refs": [manifest.get("manifest_id", "unknown")],
        "access_policy_ref": manifest.get("default_access_policy_ref", "policy.synthetic-only.v1"),
        "result_span_refs": passage_ids if passage_ids else default_spans,
        "source_refs": [{"source_ref_id": ref["source_ref_id"]} for ref in source_refs],
        "claim_refs": [{"claim_ref_id": ref["claim_ref_id"]} for ref in claim_refs],
        "passage_refs": [{"passage_ref_id": ref["passage_ref_id"]} for ref in passage_refs],
        "coverage_records": [{"coverage_record_id": ref["coverage_record_id"]} for ref in coverage_records],
        "verification_records": [{"verification_record_id": ref["verification_record_id"]} for ref in verification_records],
        "untrusted_content_anomaly_records": [
            {"anomaly_record_id": ref["anomaly_record_id"]} for ref in anomaly_records
        ],
        "omitted_reasons": [],
        "created_at": utc_now(),
        "boundary_controls": {
            "external_source_not_canon": True,
            "raw_document_payload_embedded": False,
            "retrieved_content_treated_as_instruction": False,
        },
    }
