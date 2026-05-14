from __future__ import annotations

from typing import Any

from .util import new_id, utc_now


def assemble_synthetic_context_bundle(manifest: dict[str, Any], *, bundle_type: str, run_id: str, retrieval_trace_id: str) -> dict[str, Any]:
    docs = manifest.get("documents") or []
    if not docs:
        raise ValueError("manifest contains no documents")
    document_refs = [doc["document_ref"] for doc in docs]
    first = document_refs[0]
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
        "controlling_span_refs": [f"{first}#synthetic-controlling-span"],
        "related_span_refs": [f"{first}#synthetic-related-span"],
        "entities": {"source": "synthetic_fixture"},
        "missing_or_uncertain": ["Synthetic bundle; no production source system has been consulted."],
        "human_review_required": True,
        "created_at": utc_now(),
        "boundary_controls": {
            "bundle_is_canonical_truth": False,
            "may_be_used_without_human_review_for_legal_finality": False,
            "raw_document_payload_embedded": False,
        },
    }


def build_retrieval_trace(manifest: dict[str, Any], *, run_id: str, retrieval_plan_id: str, retrievers_used: list[str]) -> dict[str, Any]:
    docs = manifest.get("documents") or []
    return {
        "schema_type": "legal-retrieval-trace",
        "schema_version": "v1",
        "retrieval_trace_id": new_id("lkrt"),
        "run_id": run_id,
        "retrieval_plan_id": retrieval_plan_id,
        "retrievers_used": retrievers_used,
        "source_manifest_refs": [manifest.get("manifest_id", "unknown")],
        "access_policy_ref": manifest.get("default_access_policy_ref", "policy.synthetic-only.v1"),
        "result_span_refs": [f"{doc['document_ref']}#synthetic-controlling-span" for doc in docs if doc.get("document_ref")],
        "omitted_reasons": [],
        "created_at": utc_now(),
    }
