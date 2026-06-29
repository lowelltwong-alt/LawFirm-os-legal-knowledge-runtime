# AI Table Of Contents

Canonical machine name: `LawFirm-os-legal-knowledge-runtime`. Plane: legal knowledge runtime.

This repo assembles legal ingestion preflight records, retrieval plans, and Legal Context Bundles under Semantic Substrate contracts. It does not define canonical schemas, registries, governance doctrine, route IDs, endpoint authority, AI front-door routing, or legal truth.

## Start Here

- `AI_WORK_START_HERE.md` - repo-specific AI work router.
- `AGENTS.md` - agent-facing safety and authority rules.
- `README.md` - current MVP scope and non-claims.
- `.ai/control/governance-dependency-map-mirror.json` - local mirror of the upstream governance dependency map; it cannot override `LawFirm-os-semantic-substrate`.
- `scripts/validate_governance_dependency_map_mirror.py` - fail-closed check for mirror shape and watched governance paths.

## Contract Authority

- `contracts.lock.json` - local substrate contract pin.
- Substrate `registry/governance-dependency-map.json` - canonical governance-facing dependency map and child mirror update gate.
- Substrate `registry/ai-front-door-registry.json` - canonical AI front-door registry.
- Substrate `governance/LEGAL_KNOWLEDGE_RUNTIME_BOUNDARY.md` - legal knowledge runtime boundary.
- Substrate `governance/LEGAL_DOCUMENT_INGESTION_BOUNDARY.md` - ingestion and raw-payload boundary.
- Substrate `governance/CONTEXT_QUALITY_DOCTRINE.md` - Legal Context Bundle and context-quality doctrine.

## Hard Boundaries

- no real client data
- no real matter data
- no raw legal payload storage
- no Semantic Substrate writes
- no production DMS connector
- no model or retrieval output as legal truth
- no privilege, permission, freshness, or provenance bypass
