# LawFirm OS Legal Knowledge Runtime

Local-first, synthetic-first runtime for legal document ingestion preflight, retrieval planning, and Legal Context Bundle assembly.

## Position in the kernel

```text
Semantic Substrate        -> legal knowledge contracts and boundary doctrine
Legal Knowledge Runtime   -> document ingestion, indexes, retrieval plans, context bundles
Orchestrator              -> calls this runtime as a bounded tool
Exception Lake Runtime    -> stores retrieval trace/evidence events, not full document payloads
Skills Registry           -> reusable legal-knowledge expertise as skills
```

## MVP commands

```bash
python -m lawfirm_os_legal_knowledge ingest-preflight \
  --manifest examples/synthetic_legal_document_ingestion_manifest.json \
  --substrate ../LawFirm-os-semantic-substrate \
  --out-dir .lawfirm-os-legal-knowledge/runs \
  --stdout json

python -m lawfirm_os_legal_knowledge assemble-bundle \
  --manifest examples/synthetic_legal_document_ingestion_manifest.json \
  --bundle-type contract_review_context.v1 \
  --out-dir .lawfirm-os-legal-knowledge/runs \
  --stdout json
```

## Non-claims

- No real client data path.
- No real matter data path.
- No production DMS connector.
- No provider-specific vector or graph database.
- No Semantic Substrate writes.
- No legal finality without human review.

## Governance Dependency-Map Mirror

This repo carries `.ai/control/governance-dependency-map-mirror.json` as a local mirror of the upstream governance dependency map in `LawFirm-os-semantic-substrate/registry/governance-dependency-map.json`.

If governance-facing legal-knowledge-runtime files change, check the upstream governance dependency map and update the local mirror, AI work router, AI table of contents, README, validator, and tests when affected. The mirror is downstream enforcement only; it cannot override Semantic Substrate governance, define canonical schemas or registries, treat retrieval/model output as legal truth, store raw legal payloads, or authorize production automation.

## Context Quality Doctrine Dependency

- Legal Knowledge Runtime assembles Legal Context Bundles under Semantic Substrate contracts, including `../LawFirm-os-semantic-substrate/governance/CONTEXT_QUALITY_DOCTRINE.md`.
- It may calculate context-quality and uncertainty metrics only when definitions exist in Semantic Substrate.
- It must not promote institutional knowledge to canon.
- It must preserve provenance, authority level, scope, review status, stale-after policy, and bundle hashes.
- Shannon/entropy metrics are measurement tools, not legal-truth claims.
