from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from .safety import scan_retrieved_text_for_injection
from .util import new_id, utc_now


PASSAGE_SPAN_TYPES = frozenset(
    {
        "holding",
        "rule",
        "facts",
        "reasoning",
        "statute_section",
        "regulation_paragraph",
        "clause",
        "docket_event",
        "argument_section",
        "unknown",
    }
)


class SourceGroundingError(ValueError):
    """Raised when a source-grounded artifact cannot be emitted safely."""


@dataclass(frozen=True)
class SourceEmission:
    source_ref: dict[str, Any]
    anomaly_records: tuple[dict[str, Any], ...]


def emit_source_ref(
    document: dict[str, Any],
    *,
    run_id: str,
    retrieved_at: str | None = None,
    content: str | None = None,
) -> SourceEmission:
    if not run_id:
        raise SourceGroundingError("run_id is required")
    source_id = str(document.get("document_ref") or "")
    if not source_id:
        raise SourceGroundingError("document_ref is required for SourceRef emission")
    content_hash = _content_hash(document, content)
    detected = bool(content and scan_retrieved_text_for_injection(content))
    source_ref_id = new_id("sr")
    anomaly_records = tuple(
        emit_untrusted_content_anomaly_records(
            source_ref_id=source_ref_id,
            run_id=run_id,
            content=content or "",
            detected_at=retrieved_at,
        )
    )
    source_ref: dict[str, Any] = {
        "schema_version": "source_ref.v1",
        "source_ref_id": source_ref_id,
        "source_id": source_id,
        "content_hash": content_hash,
        "retrieved_at": retrieved_at or utc_now(),
        "source_kind": _source_kind(document),
        "provenance_tag": _provenance_tag(document),
        "freshness_status": str(document.get("freshness_status") or "unknown"),
        "instruction_like_content_detected": detected,
        "run_id": run_id,
    }
    if anomaly_records:
        source_ref["untrusted_content_anomaly_record_id"] = anomaly_records[0]["anomaly_record_id"]
    return SourceEmission(source_ref=source_ref, anomaly_records=anomaly_records)


def emit_passage_ref(
    *,
    source_ref_id: str,
    document: dict[str, Any],
    span_text: str,
    run_id: str,
    span_type: str,
    passage_ref_id: str | None = None,
    citation_label: str | None = None,
    citation_anchor: str | None = None,
    start_offset: int | None = None,
    end_offset: int | None = None,
    heading_path: Sequence[str] | None = None,
    parent_passage_ref_id: str | None = None,
    related_passage_ref_ids: Sequence[str] | None = None,
    cites_passage_ref_ids: Sequence[str] | None = None,
    provider_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Emit a graph-ready PassageRef anchored to a SourceRef (structural / locator grounding, not token chunking)."""
    if not source_ref_id:
        raise SourceGroundingError("source_ref_id is required")
    if not run_id:
        raise SourceGroundingError("run_id is required")
    if not span_text:
        raise SourceGroundingError("span_text is required for passage hashing")
    if span_type not in PASSAGE_SPAN_TYPES:
        raise SourceGroundingError("span_type must be a substrate-registered passage span type")
    locator: dict[str, Any] = {}
    if start_offset is not None:
        locator["start_offset"] = start_offset
    if end_offset is not None:
        locator["end_offset"] = end_offset
    if heading_path:
        locator["heading_path"] = list(heading_path)
    meta = dict(provider_metadata) if provider_metadata else {}
    passage: dict[str, Any] = {
        "schema_version": "passage_ref.v1",
        "passage_ref_id": passage_ref_id or new_id("pr"),
        "source_ref_id": source_ref_id,
        "source_kind": _source_kind(document),
        "text_sha256": _bare_hash(span_text),
        "span_type": span_type,
        "canonical_status": "external_source_not_canon",
        "run_id": run_id,
    }
    jurisdiction = str(document.get("jurisdiction") or "").strip()
    if jurisdiction:
        passage["jurisdiction"] = jurisdiction
    if locator:
        passage["locator"] = locator
    if citation_label:
        passage["citation_label"] = citation_label
    if citation_anchor:
        passage["citation_anchor"] = citation_anchor
    if parent_passage_ref_id:
        passage["parent_passage_ref_id"] = parent_passage_ref_id
    if related_passage_ref_ids:
        passage["related_passage_ref_ids"] = list(related_passage_ref_ids)
    if cites_passage_ref_ids:
        passage["cites_passage_ref_ids"] = list(cites_passage_ref_ids)
    if meta:
        passage["provider_metadata"] = meta
    return passage


def emit_source_refs_for_manifest(
    manifest: dict[str, Any],
    *,
    run_id: str,
    retrieved_at: str | None = None,
    content_by_document_ref: dict[str, str] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sources: list[dict[str, Any]] = []
    anomalies: list[dict[str, Any]] = []
    docs = manifest.get("documents") or []
    if not isinstance(docs, list) or not docs:
        raise SourceGroundingError("manifest documents must be a non-empty list")
    for doc in docs:
        if not isinstance(doc, dict):
            raise SourceGroundingError("manifest documents must be objects")
        content = None
        if content_by_document_ref:
            content = content_by_document_ref.get(str(doc.get("document_ref") or ""))
        emitted = emit_source_ref(doc, run_id=run_id, retrieved_at=retrieved_at, content=content)
        sources.append(emitted.source_ref)
        anomalies.extend(emitted.anomaly_records)
    return sources, anomalies


def emit_coverage_record(
    *,
    source_ref_id: str,
    run_id: str,
    units_requested: int,
    units_read: int,
    coverage_record_id: str | None = None,
    passage_ref_id: str | None = None,
) -> dict[str, Any]:
    if not source_ref_id:
        raise SourceGroundingError("source_ref_id is required")
    if not run_id:
        raise SourceGroundingError("run_id is required")
    if units_requested < 0 or units_read < 0:
        raise SourceGroundingError("coverage units cannot be negative")
    partial = units_read < units_requested
    rec: dict[str, Any] = {
        "schema_version": "coverage_record.v1",
        "coverage_record_id": coverage_record_id or new_id("cov"),
        "source_ref_id": source_ref_id,
        "units_requested": units_requested,
        "units_read": units_read,
        "partial_read": partial,
        "reviewer_note_required": partial,
        "coverage_quality": _coverage_quality(units_requested, units_read),
        "run_id": run_id,
    }
    if passage_ref_id:
        rec["passage_ref_id"] = passage_ref_id
    return rec


def emit_claim_ref(
    *,
    claim_text: str,
    source_ref_ids: Sequence[str],
    run_id: str,
    support_status: str = "supported",
    verified_status: str = "pending",
    defect_record_id: str | None = None,
    claim_ref_id: str | None = None,
    passage_ref_ids: Sequence[str] | None = None,
) -> dict[str, Any]:
    if not claim_text:
        raise SourceGroundingError("claim_text is required")
    if not run_id:
        raise SourceGroundingError("run_id is required")
    if not source_ref_ids:
        raise SourceGroundingError("at least one source_ref_id is required")
    if support_status == "unsupported" and not defect_record_id:
        raise SourceGroundingError("unsupported claim requires defect_record_id or validation failure")
    if verified_status == "refuted" and not defect_record_id:
        raise SourceGroundingError("refuted claim requires defect_record_id or validation failure")
    claim: dict[str, Any] = {
        "schema_version": "claim_ref.v1",
        "claim_ref_id": claim_ref_id or new_id("cl"),
        "claim_text_hash": _bare_hash(claim_text),
        "support_status": support_status,
        "verified_status": verified_status,
        "source_refs": [{"source_ref_id": ref} for ref in source_ref_ids],
        "run_id": run_id,
    }
    if passage_ref_ids:
        claim["passage_refs"] = [{"passage_ref_id": ref} for ref in passage_ref_ids]
    if defect_record_id:
        claim["defect_record_id"] = defect_record_id
    return claim


def emit_unsupported_claim_validation_failure(
    *,
    claim_text: str,
    source_ref_ids: Sequence[str],
    run_id: str,
) -> dict[str, Any]:
    if not claim_text:
        raise SourceGroundingError("claim_text is required")
    return {
        "schema_version": "legal_claim_validation_failure.pr07",
        "validation_failure_id": new_id("lkvf"),
        "failure_kind": "unsupported_claim",
        "claim_text_hash": _bare_hash(claim_text),
        "source_refs": [{"source_ref_id": ref} for ref in source_ref_ids],
        "run_id": run_id,
        "raw_claim_text_included": False,
        "created_at": utc_now(),
    }


def emit_verification_record(
    *,
    claim_ref_id: str,
    run_id: str,
    verified_by_kind: str,
    verified_by_id: str,
    verdict: str,
    confidence: float | None = None,
    freshness_window_days: int | None = None,
    defect_record_id: str | None = None,
    verified_at: str | None = None,
    verification_record_id: str | None = None,
    passage_ref_ids: Sequence[str] | None = None,
) -> dict[str, Any]:
    if verdict == "refuted" and not defect_record_id:
        raise SourceGroundingError("refuted verification requires defect_record_id or validation failure")
    rec: dict[str, Any] = {
        "schema_version": "verification_record.v1",
        "verification_record_id": verification_record_id or new_id("vr"),
        "claim_ref_id": claim_ref_id,
        "verified_by_kind": verified_by_kind,
        "verified_by_id": verified_by_id,
        "verdict": verdict,
        "verified_at": verified_at or utc_now(),
        "run_id": run_id,
    }
    if confidence is not None:
        rec["confidence"] = confidence
    if freshness_window_days is not None:
        rec["freshness_window_days"] = freshness_window_days
    if defect_record_id:
        rec["defect_record_id"] = defect_record_id
    if passage_ref_ids:
        rec["passage_refs"] = [{"passage_ref_id": ref} for ref in passage_ref_ids]
    return rec


def emit_untrusted_content_anomaly_records(
    *,
    source_ref_id: str,
    run_id: str,
    content: str,
    detected_at: str | None = None,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for signal in scan_retrieved_text_for_injection(content):
        records.append(
            {
                "schema_version": "untrusted_content_anomaly_record.v1",
                "anomaly_record_id": new_id("uca"),
                "source_ref_id": source_ref_id,
                "run_id": run_id,
                "detected_at": detected_at or utc_now(),
                "risk_flag": signal.risk_flag,
                "decision": signal.decision,
                "detail_hash": _bare_hash(signal.detail),
                "raw_content_included": False,
                "retrieved_content_treated_as_instruction": False,
            }
        )
    return records


def source_refs_for_context_bundle(source_refs: Iterable[dict[str, Any]]) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for ref in source_refs:
        refs.append(
            {
                "source_ref_id": str(ref["source_ref_id"]),
                "source_id": str(ref["source_id"]),
                "content_hash": str(ref["content_hash"]),
            }
        )
    return refs


def passage_refs_for_context_bundle(passage_refs: Iterable[dict[str, Any]]) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for ref in passage_refs:
        refs.append(
            {
                "passage_ref_id": str(ref["passage_ref_id"]),
                "source_ref_id": str(ref["source_ref_id"]),
                "text_sha256": str(ref["text_sha256"]),
            }
        )
    return refs


def refs_for_evidence_packet(records: Iterable[dict[str, Any]], id_field: str) -> list[dict[str, str]]:
    return [{id_field: str(record[id_field])} for record in records]


def validate_source_refs(source_refs: Iterable[dict[str, Any]]) -> list[str]:
    failures: list[str] = []
    for idx, ref in enumerate(source_refs):
        label = f"source_refs[{idx}]"
        if not ref.get("provenance_tag"):
            failures.append(f"{label}.provenance_tag is required")
        content_hash = str(ref.get("content_hash") or "")
        if not _is_hex64(content_hash):
            failures.append(f"{label}.content_hash must be 64-hex")
    return failures


def _content_hash(document: dict[str, Any], content: str | None) -> str:
    if content is not None:
        return _bare_hash(content)
    source_hash = str(document.get("source_hash") or "")
    if not source_hash:
        raise SourceGroundingError("source_hash is required for SourceRef emission")
    bare = source_hash.removeprefix("sha256:")
    if not _is_hex64(bare):
        raise SourceGroundingError("source_hash must be sha256-prefixed or bare 64-hex")
    return bare


def _source_kind(document: dict[str, Any]) -> str:
    if str(document.get("source_uri") or "").startswith("synthetic://"):
        return "synthetic_fixture"
    document_type = str(document.get("document_type") or "").lower()
    mapping = {
        "statute": "statute",
        "regulation": "regulation",
        "case": "case_law",
        "case_law": "case_law",
        "secondary": "secondary",
        "memo": "internal_memo",
        "internal_memo": "internal_memo",
    }
    return mapping.get(document_type, "secondary")


def _provenance_tag(document: dict[str, Any]) -> str:
    if str(document.get("source_uri") or "").startswith("synthetic://"):
        return "external_source_not_canon.synthetic_fixture"
    return str(document.get("provenance_tag") or "external_source_not_canon.unverified")


def _coverage_quality(units_requested: int, units_read: int) -> str:
    if units_requested == 0:
        return "metadata_only"
    if units_read == 0:
        return "metadata_only"
    if units_read >= units_requested:
        return "complete"
    return "partial"


def _bare_hash(value: Any) -> str:
    if isinstance(value, str):
        encoded = value.encode("utf-8")
    else:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _is_hex64(value: str) -> bool:
    return len(value) == 64 and all(c in "0123456789abcdef" for c in value)
