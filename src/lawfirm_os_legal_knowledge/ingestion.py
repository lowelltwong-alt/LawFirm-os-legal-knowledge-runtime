from __future__ import annotations

from dataclasses import dataclass
from typing import Any

ALLOWED_INDEXES = {"metadata", "lexical", "document_tree", "vector", "graph", "compiled_bundle"}
MVP_ALLOWED_DATA_ORIGINS = {"synthetic"}


@dataclass(frozen=True)
class PreflightResult:
    status: str
    accepted: bool
    manifest_id: str
    corpus_id: str
    document_count: int
    permitted_indexes: list[str]
    warnings: list[str]
    failures: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "accepted": self.accepted,
            "manifest_id": self.manifest_id,
            "corpus_id": self.corpus_id,
            "document_count": self.document_count,
            "permitted_indexes": self.permitted_indexes,
            "warnings": self.warnings,
            "failures": self.failures,
        }


def validate_ingestion_manifest(manifest: dict[str, Any]) -> PreflightResult:
    failures: list[str] = []
    warnings: list[str] = []

    if manifest.get("schema_type") != "legal-document-ingestion-manifest":
        failures.append("schema_type must be legal-document-ingestion-manifest")
    if manifest.get("schema_version") != "v1":
        failures.append("schema_version must be v1")
    if manifest.get("data_origin") not in MVP_ALLOWED_DATA_ORIGINS:
        failures.append("MVP permits only synthetic data_origin")
    if manifest.get("contains_real_client_data") is not False:
        failures.append("contains_real_client_data must be false in MVP")
    if manifest.get("contains_real_matter_data") is not False:
        failures.append("contains_real_matter_data must be false in MVP")
    boundary = manifest.get("boundary_controls") or {}
    if boundary.get("raw_payload_embedded") is not False:
        failures.append("raw_payload_embedded must be false")
    if boundary.get("runtime_may_write_substrate") is not False:
        failures.append("runtime_may_write_substrate must be false")
    if boundary.get("full_document_payload_allowed_to_lake") is not False:
        failures.append("full_document_payload_allowed_to_lake must be false")

    docs = manifest.get("documents")
    if not isinstance(docs, list) or not docs:
        failures.append("documents must be a non-empty list")
        docs = []

    permitted: set[str] = set()
    for idx, doc in enumerate(docs):
        label = f"documents[{idx}]"
        if doc.get("confidentiality_label") != "synthetic":
            failures.append(f"{label}.confidentiality_label must be synthetic in MVP")
        if doc.get("privilege_label") != "none":
            failures.append(f"{label}.privilege_label must be none in MVP")
        if not str(doc.get("source_uri", "")).startswith("synthetic://"):
            failures.append(f"{label}.source_uri must use synthetic:// in MVP")
        for required in ("document_ref", "document_type", "source_hash", "retention_class", "parser_profile", "access_policy_ref"):
            if not doc.get(required):
                failures.append(f"{label}.{required} is required")
        indexes = doc.get("permitted_indexes") or []
        if not isinstance(indexes, list) or not indexes:
            failures.append(f"{label}.permitted_indexes must be non-empty")
        for index in indexes:
            if index not in ALLOWED_INDEXES:
                failures.append(f"{label}.permitted_indexes contains unsupported primitive {index!r}")
            else:
                permitted.add(index)
        if {"vector", "graph"} & set(indexes):
            warnings.append(f"{label}: vector/graph requested but MVP ships adapter seams only")

    accepted = not failures
    return PreflightResult(
        status="accepted" if accepted else "blocked",
        accepted=accepted,
        manifest_id=str(manifest.get("manifest_id", "unknown")),
        corpus_id=str(manifest.get("corpus_id", "unknown")),
        document_count=len(docs),
        permitted_indexes=sorted(permitted),
        warnings=warnings,
        failures=failures,
    )
