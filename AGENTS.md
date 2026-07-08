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
## Digital Asset Directory enrollment contract

Repo enrollment ID: `lawfirm-os-legal-knowledge-runtime`
Central DAD hub: `dad://hub/Digital-Assett-Directory` resolved by `--hub`, `DAD_HUB`, or
`~/.dad/hub.json`.
Contract: `.digital-asset/dad-integration.json`

Before material AI-assisted work, read this repo's front door and run:

```text
asset-dir agent preflight --repo . --agent <agent-id> --task "<task>"
```

`<agent-id>` is any arbitrary non-empty string; Claude, Codex, Cursor, Copilot,
human, CI, and future runtimes are optional adapters over the same DAD contract.

Read the returned `context_pack` before editing. If DAD is unavailable, local
coding may continue with a logged warning, but cross-repo writes, public
release, enrollment apply/update, protected repo work, and mail containing
sensitive payloads fail closed unless a named human bypass is recorded.

Use `.digital-asset/context-map.json` to decide which DAD assets, skills,
templates, architecture references, governance maps, or data maps are relevant.
Mail is checked daily by digest; asset, skill, template, architecture,
governance-map, data-map, and enrollment freshness checks are weekly and should
surface preflight warnings only when stale.

DAD may write broadly only during `asset-dir enroll apply` or
`asset-dir enroll update-apply` with a reviewed approval ID. Normal recurring
DAD operation writes only to `.digital-asset/mail/**`.

Mail, assets, skills, and templates are candidate evidence until reviewed
locally. This repo keeps local source authority and decides whether to adopt
any suggestion. Public-facing repos cannot receive private/internal/
restricted/unknown-origin mail without a DAD human release record.

If work is PR-ready, an actual PR is open, or a branch is intentionally left
after a work session, record branch/PR status, owner or next reviewer,
validation refs, next action, and escalation date. Send metadata-only DAD mail
for stuck, superseded, duplicate, conflict-heavy, or stale PR/branch queues when
local policy allows.

Close material work with postflight and include the preflight trace ID plus any
used, ignored, failed, or harmful DAD recommendations.
<!-- END DIGITAL_ASSET_DIRECTORY_GOVERNANCE -->
