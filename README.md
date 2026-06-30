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

Use `python scripts/run_full_pytest.py` for full or focused pytest runs. Direct pytest invocation is blocked by `config/validation-runtime-policy.yaml` so local and agent validation always gets the required 3600 second timeout ceiling.

## Intake Context Bundle Review

This repo carries a candidate-only intake context-bundle review docket at `registry/intake-context-bundle-review-registry.json`, with narrative guidance in `docs/INTAKE_CONTEXT_BUNDLE_REVIEW.md` and deterministic validation in `scripts/validate_intake_context_bundle_review.py`.

The docket reviews how `LawFirm-os-intake` should hand source refs, passage refs, claim refs, retrieval traces, L&E party/entity/relationship signals, budget-driver context, and missing-info blockers to Legal Knowledge Runtime. It does not authorize real data, raw payload storage, production connectors, canonical schema or taxonomy creation, legal truth, budget approval, or matter opening.

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
