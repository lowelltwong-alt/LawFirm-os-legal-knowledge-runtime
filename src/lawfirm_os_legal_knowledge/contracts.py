from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .util import read_json, sha256_file


MANIFEST_REL = Path("manifests") / "contract_manifest.v1.json"
CONTRACT_EXPORT_REL = Path("registry") / "legal-knowledge-runtime-contract-export.json"


@dataclass(frozen=True)
class SubstrateLegalKnowledgeSnapshot:
    root: Path
    manifest_id: str
    manifest_hash: str
    legal_contract_export_present: bool
    legal_contract_export_hash: str | None
    allowed_schema_keys: list[str]
    registry_refs: list[str]


def load_substrate_snapshot(substrate_root: str | Path | None) -> SubstrateLegalKnowledgeSnapshot:
    if substrate_root is None:
        return SubstrateLegalKnowledgeSnapshot(
            root=Path("."),
            manifest_id="none",
            manifest_hash="sha256:" + "0" * 64,
            legal_contract_export_present=False,
            legal_contract_export_hash=None,
            allowed_schema_keys=[],
            registry_refs=[],
        )
    root = Path(substrate_root).resolve()
    manifest_path = root / MANIFEST_REL
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing substrate manifest: {manifest_path}")
    manifest = read_json(manifest_path)
    export_path = root / CONTRACT_EXPORT_REL
    return SubstrateLegalKnowledgeSnapshot(
        root=root,
        manifest_id=str(manifest.get("manifest_id", "unknown")),
        manifest_hash=sha256_file(manifest_path),
        legal_contract_export_present=export_path.exists(),
        legal_contract_export_hash=sha256_file(export_path) if export_path.exists() else None,
        allowed_schema_keys=[str(x) for x in manifest.get("canonical_schema_keys", [])],
        registry_refs=[str(x) for x in manifest.get("registry_refs", [])],
    )
