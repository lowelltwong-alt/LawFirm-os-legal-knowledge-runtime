# AGENTS.md

<!-- BEGIN LAWFIRM_OS_BOOTSTRAP -->
Managed bootstrap for the LawFirm OS Skill-Agent Control Plane. This block adds cross-repo routing context; it must not replace the repo-specific instructions preserved below.

Before making changes in this repository, read:

1. AI_WORK_START_HERE.md
2. skill-agent-manifest.json
3. ../LawFirm-os-semantic-substrate/registry/ai-front-door-registry.json
4. ../LawFirm-os-semantic-substrate/registry/skill-agent-control-plane-registry.json
5. ../LawFirm-os-semantic-substrate/governance/SKILL_AGENT_CONTROL_PLANE_BOUNDARY.md

Repo: LawFirm-os-legal-knowledge-runtime
Plane: legal knowledge runtime
Repo purpose: Legal ingestion preflight, document structure, retrieval planning, context bundles, eval helpers, and integrity checks.
This repo must not own: canonical schemas, global skill lifecycle policy, Exception Lake persistence authority.

Preservation rule: keep the REPO_SPECIFIC_INSTRUCTIONS section intact unless a human explicitly approves removal. New bootstrap text should be merged around repo-specific doctrine, not overwrite it.
<!-- END LAWFIRM_OS_BOOTSTRAP -->

<!-- BEGIN REPO_SPECIFIC_INSTRUCTIONS -->
# Agent Instructions

This repo is the Legal Knowledge Runtime, not the source of semantic authority.

## Required AI entry behavior

Before making changes in this repository, read:

1. `AI_WORK_START_HERE.md`
2. `../LawFirm-os-semantic-substrate/registry/ai-front-door-registry.json`
3. `../LawFirm-os-semantic-substrate/governance/AI_FRONT_DOOR_BOUNDARY.md`

This repository is one component of the LawFirm OS multi-repo kernel. Do not treat it as standalone.

## Boundary rule

This repository owns legal document ingestion preflight, document structure, retrieval planning, context bundle assembly, integrity checks, and local eval helpers. Canonical schemas, registries, governance doctrine, route authority, legal document type authority, endpoint authority, and the AI front door remain in `LawFirm-os-semantic-substrate`.

## Required validation

Before reporting success, run `python scripts/run_full_pytest.py` in this repository and the AI front-door integrity gate: `python ../LawFirm-os-semantic-substrate/scripts/validate_ai_front_door.py --substrate-root ../LawFirm-os-semantic-substrate`. The pytest wrapper is required by `config/validation-runtime-policy.yaml`; direct pytest invocation is blocked so validation always gets the long ceiling.

## Invariants

- Read contracts from Semantic Substrate; never mutate them.
- Treat all model/tool outputs as proposals.
- Do not ingest real client or matter data in MVP.
- Do not write full document payloads to Exception Lake.
- Prefer claim-check references, hashes, and span refs over payload fanout.
- Fail closed on missing access policy, privilege label, retention class, parser profile, or unsupported index primitive.

## Allowed MVP work

- synthetic ingestion preflight;
- local metadata/lexical/document-tree scaffolding;
- legal retrieval plan objects;
- legal context bundle objects;
- retrieval traces and runtime ledger records.

## Forbidden MVP work

- live connectors;
- autonomous writes;
- broad recursive file crawling;
- external API calls;
- silent schema or registry changes;
- production document ingestion.

## Context Quality Doctrine Dependency

- Legal Knowledge Runtime assembles Legal Context Bundles under Semantic Substrate contracts, including `../LawFirm-os-semantic-substrate/governance/CONTEXT_QUALITY_DOCTRINE.md`.
- It may calculate context-quality and uncertainty metrics only when definitions exist in Semantic Substrate.
- It must not promote institutional knowledge to canon.
- It must preserve provenance, authority level, scope, review status, stale-after policy, and bundle hashes.
- Shannon/entropy metrics are measurement tools, not legal-truth claims.
<!-- END REPO_SPECIFIC_INSTRUCTIONS -->

<!-- BEGIN DIGITAL_ASSET_DIRECTORY_GOVERNANCE -->
## Digital Asset Directory learning and mail pointer

Central hub: `C:\Users\lowel\OneDrive\Desktop\Git Projects\04_Digital_Assett_Directory`
Wave: `1`
Rollout policy: `managed_pointer_plus_mailbox`
Authority tier: `knowledge_runtime`
Recommended profiles: `python-modular-design, legal-knowledge-runtime, retrieval-boundaries`

Before material AI-assisted work:
1. Read this repository's own front door and authority surfaces first.
2. Run: `asset-dir agent preflight --repo . --agent <agent> --task "<task>" --hub "C:\Users\lowel\OneDrive\Desktop\Git Projects\04_Digital_Assett_Directory"`
3. State scope, allowed and forbidden paths, validation plan, and stop conditions.
4. Preserve this repo's local canon. DAD is advisory evidence and learning transport, not semantic authority.

Before reporting completion or pushing material changes:
1. Run this repo's required validation.
2. Run: `asset-dir agent postflight --session <SESSION_ID> --repo . --summary "<summary>" --hub "C:\Users\lowel\OneDrive\Desktop\Git Projects\04_Digital_Assett_Directory"`
3. Capture lessons, discoveries, failures, reusable patterns, missing capabilities, risks, and unknowns.

DAD mail lives at `.digital-asset/mail/` and is candidate-only inbox/outbox transport. Mail can suggest lessons, workflows, assets, taxonomy, capabilities, or governance notices; local review decides whether anything is adopted. Agent review is triage only, and human review/public-release gates remain separate.

Hooks are not enabled by this Wave 1 install. Do not set `core.hooksPath` or add hook enforcement without separate human approval.
<!-- END DIGITAL_ASSET_DIRECTORY_GOVERNANCE -->
