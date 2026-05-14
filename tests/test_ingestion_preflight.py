from __future__ import annotations

import json
from pathlib import Path

from lawfirm_os_legal_knowledge.cli import main
from lawfirm_os_legal_knowledge.ingestion import validate_ingestion_manifest
from lawfirm_os_legal_knowledge.util import read_json

ROOT = Path(__file__).resolve().parents[1]


def test_synthetic_manifest_passes_preflight() -> None:
    manifest = read_json(ROOT / "examples" / "synthetic_legal_document_ingestion_manifest.json")
    result = validate_ingestion_manifest(manifest)
    assert result.accepted is True
    assert "metadata" in result.permitted_indexes
    assert result.failures == []


def test_real_data_flags_fail_preflight() -> None:
    manifest = read_json(ROOT / "examples" / "synthetic_legal_document_ingestion_manifest.json")
    manifest["contains_real_client_data"] = True
    result = validate_ingestion_manifest(manifest)
    assert result.accepted is False
    assert any("contains_real_client_data" in failure for failure in result.failures)


def test_cli_ingest_preflight_without_substrate(tmp_path: Path, capsys) -> None:
    code = main([
        "ingest-preflight",
        "--manifest", str(ROOT / "examples" / "synthetic_legal_document_ingestion_manifest.json"),
        "--out-dir", str(tmp_path),
        "--stdout", "json",
    ])
    assert code == 0
    output = json.loads(capsys.readouterr().out)
    assert output["accepted"] is True
    assert Path(output["evidence_packet_path"]).exists()


def test_cli_assemble_bundle(tmp_path: Path, capsys) -> None:
    code = main([
        "assemble-bundle",
        "--manifest", str(ROOT / "examples" / "synthetic_legal_document_ingestion_manifest.json"),
        "--bundle-type", "contract_review_context.v1",
        "--out-dir", str(tmp_path),
        "--stdout", "json",
    ])
    assert code == 0
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "ok"
    bundle = read_json(Path(output["evidence_packet_path"]) / "legal_context_bundle.json")
    assert bundle["boundary_controls"]["bundle_is_canonical_truth"] is False
