# AI Table Of Contents

Canonical machine name: `LawFirm-os-legal-knowledge-runtime`. Plane: legal knowledge runtime.

This repo assembles legal ingestion preflight records, retrieval plans, and Legal Context Bundles under Semantic Substrate contracts. It does not define canonical schemas, registries, governance doctrine, route IDs, endpoint authority, AI front-door routing, or legal truth.

## Start Here

- `AI_WORK_START_HERE.md` - repo-specific AI work router.
- `AGENTS.md` - agent-facing safety and authority rules.
- `README.md` - current MVP scope and non-claims.
- `.ai/control/governance-dependency-map-mirror.json` - local mirror of the upstream governance dependency map; it cannot override `LawFirm-os-semantic-substrate`.
- `scripts/validate_governance_dependency_map_mirror.py` - fail-closed check for mirror shape and watched governance paths.
- `config/validation-runtime-policy.yaml` - minimum runtime ceiling policy for full and focused pytest validation.
- `scripts/run_full_pytest.py` - required pytest wrapper that applies the validation runtime policy marker and long timeout.
- `registry/intake-context-bundle-review-registry.json` - candidate-only review docket for intake context-bundle, L&E budget-context, and missing-info handoff surfaces.
- `docs/INTAKE_CONTEXT_BUNDLE_REVIEW.md` - human-readable review guidance for the candidate intake context-bundle docket.
- `scripts/validate_intake_context_bundle_review.py` - deterministic validator for the candidate docket.

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

## Candidate Intake Context Bundle Review

- `LawFirm-os-intake` may propose source-bound context needs, but this repo only reviews candidate Legal Knowledge Runtime interfaces.
- L&E entity, role, relationship, budget-driver, and missing-info signals are local review labels, not canonical legal taxonomies.
- Every observed fact must remain source-bound through source refs, passage refs, claim refs, retrieval traces, and bundle hashes.
- The candidate docket does not authorize real data, raw legal payload storage, production connectors, Semantic Substrate writes, legal truth, budget approval, or matter opening.
