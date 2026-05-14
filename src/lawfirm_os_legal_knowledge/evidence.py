from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import append_jsonl, sha256_file, sha256_json, utc_now, write_json


def write_runtime_record(ledger_path: Path, *, record_id: str, run_id: str, trace_id: str, operation: str, status: str, synthetic: bool, artifact_refs: list[str]) -> dict[str, Any]:
    record = {
        "schema_type": "legal-knowledge-runtime-record",
        "schema_version": "v1",
        "record_id": record_id,
        "run_id": run_id,
        "trace_id": trace_id,
        "operation": operation,
        "status": status,
        "synthetic": synthetic,
        "artifact_refs": artifact_refs,
        "created_at": utc_now(),
    }
    append_jsonl(ledger_path, record)
    return record


def write_evidence_dir(packet_dir: Path, files: dict[str, Any]) -> dict[str, Any]:
    packet_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in files.items():
        write_json(packet_dir / name, payload)
    manifest = {
        "schema_version": "1.0",
        "packet_hash": sha256_json(files),
        "files": {},
        "created_at": utc_now(),
    }
    for child in sorted(packet_dir.iterdir()):
        if child.is_file() and child.name != "manifest.json":
            manifest["files"][child.name] = sha256_file(child)
    write_json(packet_dir / "manifest.json", manifest)
    return manifest
