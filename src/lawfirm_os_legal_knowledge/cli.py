from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .bundle import assemble_synthetic_context_bundle, build_retrieval_trace
from .contracts import load_substrate_snapshot
from .evidence import write_evidence_dir, write_runtime_record
from .ingestion import validate_ingestion_manifest
from .util import new_id, new_trace_id, read_json, sha256_file, utc_now, write_json

EXIT_INPUT = 2
EXIT_CONTRACT = 3
EXIT_ARTIFACT = 5


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lawfirm-os-legal-knowledge")
    sub = parser.add_subparsers(dest="command", required=True)

    preflight = sub.add_parser("ingest-preflight")
    preflight.add_argument("--manifest", required=True)
    preflight.add_argument("--substrate")
    preflight.add_argument("--out-dir", default=".lawfirm-os-legal-knowledge/runs")
    preflight.add_argument("--stdout", choices=["json", "text"], default="json")

    bundle = sub.add_parser("assemble-bundle")
    bundle.add_argument("--manifest", required=True)
    bundle.add_argument("--bundle-type", required=True)
    bundle.add_argument("--out-dir", default=".lawfirm-os-legal-knowledge/runs")
    bundle.add_argument("--stdout", choices=["json", "text"], default="json")
    return parser


def run_ingest_preflight(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    run_id = new_id("lkrun")
    trace_id = new_trace_id()
    out_root = Path(args.out_dir) / run_id
    ledger_path = Path(args.out_dir) / "legal_knowledge_runtime.jsonl"
    try:
        manifest = read_json(args.manifest)
    except Exception as exc:
        return EXIT_INPUT, {"status": "input_failed", "error": str(exc)}
    try:
        snapshot = load_substrate_snapshot(args.substrate)
    except Exception as exc:
        return EXIT_CONTRACT, {"status": "substrate_failed", "error": str(exc)}

    result = validate_ingestion_manifest(manifest)
    packet_dir = out_root / "evidence"
    files = {
        "input_manifest.json": manifest,
        "substrate_snapshot.json": snapshot.__dict__ | {"root": str(snapshot.root)},
        "preflight_result.json": result.to_dict(),
    }
    evidence_manifest = write_evidence_dir(packet_dir, files)
    record = write_runtime_record(
        ledger_path,
        record_id=new_id("lkrec"),
        run_id=run_id,
        trace_id=trace_id,
        operation="ingest_preflight",
        status="success" if result.accepted else "blocked",
        synthetic=manifest.get("data_origin") == "synthetic",
        artifact_refs=[str(packet_dir)],
    )
    summary = {
        "run_id": run_id,
        "trace_id": trace_id,
        "status": result.status,
        "accepted": result.accepted,
        "manifest_id": result.manifest_id,
        "document_count": result.document_count,
        "permitted_indexes": result.permitted_indexes,
        "warnings": result.warnings,
        "failures": result.failures,
        "ledger_path": str(ledger_path),
        "evidence_packet_path": str(packet_dir),
        "evidence_packet_hash": evidence_manifest["packet_hash"],
        "runtime_record_id": record["record_id"],
        "created_at": utc_now(),
    }
    write_json(packet_dir / "stdout_summary.json", summary)
    return (0 if result.accepted else EXIT_INPUT), summary


def run_assemble_bundle(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    run_id = new_id("lkrun")
    trace_id = new_trace_id()
    out_root = Path(args.out_dir) / run_id
    ledger_path = Path(args.out_dir) / "legal_knowledge_runtime.jsonl"
    try:
        manifest = read_json(args.manifest)
    except Exception as exc:
        return EXIT_INPUT, {"status": "input_failed", "error": str(exc)}

    preflight = validate_ingestion_manifest(manifest)
    if not preflight.accepted:
        return EXIT_INPUT, {"status": "blocked", "failures": preflight.failures}
    retrieval_plan_id = new_id("lkrp")
    retrievers = sorted(set(preflight.permitted_indexes) & {"metadata", "lexical", "document_tree"}) or ["metadata"]
    trace = build_retrieval_trace(manifest, run_id=run_id, retrieval_plan_id=retrieval_plan_id, retrievers_used=retrievers)
    bundle = assemble_synthetic_context_bundle(manifest, bundle_type=args.bundle_type, run_id=run_id, retrieval_trace_id=trace["retrieval_trace_id"])
    packet_dir = out_root / "evidence"
    evidence_manifest = write_evidence_dir(packet_dir, {
        "input_manifest.json": manifest,
        "preflight_result.json": preflight.to_dict(),
        "retrieval_trace.json": trace,
        "legal_context_bundle.json": bundle,
    })
    record = write_runtime_record(
        ledger_path,
        record_id=new_id("lkrec"),
        run_id=run_id,
        trace_id=trace_id,
        operation="assemble_bundle",
        status="success",
        synthetic=True,
        artifact_refs=[str(packet_dir)],
    )
    summary = {
        "run_id": run_id,
        "trace_id": trace_id,
        "status": "ok",
        "bundle_id": bundle["bundle_id"],
        "bundle_type": bundle["bundle_type"],
        "retrieval_trace_id": trace["retrieval_trace_id"],
        "ledger_path": str(ledger_path),
        "evidence_packet_path": str(packet_dir),
        "evidence_packet_hash": evidence_manifest["packet_hash"],
        "runtime_record_id": record["record_id"],
    }
    write_json(packet_dir / "stdout_summary.json", summary)
    return 0, summary


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "ingest-preflight":
        code, summary = run_ingest_preflight(args)
    elif args.command == "assemble-bundle":
        code, summary = run_assemble_bundle(args)
    else:
        parser.error("unknown command")
        return 2
    if args.stdout == "json":
        print(json.dumps(summary, indent=2, sort_keys=False))
    else:
        print(summary.get("status", "unknown"))
    return code
