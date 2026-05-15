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

Before reporting success, run `python -m pytest -q` in this repository and the AI front-door integrity gate: `python ../LawFirm-os-semantic-substrate/scripts/validate_ai_front_door.py --substrate-root ../LawFirm-os-semantic-substrate`.

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
<!-- END REPO_SPECIFIC_INSTRUCTIONS -->
