# AI_WORK_START_HERE.md

<!-- BEGIN LAWFIRM_OS_BOOTSTRAP -->
Managed bootstrap for AI-assisted work in the LawFirm OS multi-repo workspace. Route through the canonical AI front door and Skill-Agent Control Plane, but preserve local repo operating doctrine.

Required bootstrap read order:

1. AGENTS.md
2. skill-agent-manifest.json
3. Semantic Substrate registry/ai-front-door-registry.json
4. Semantic Substrate registry/skill-agent-control-plane-registry.json
5. Semantic Substrate governance/SKILL_AGENT_CONTROL_PLANE_BOUNDARY.md

Repo: LawFirm-os-legal-knowledge-runtime
Plane: legal knowledge runtime
Repo purpose: Legal ingestion preflight, document structure, retrieval planning, context bundles, eval helpers, and integrity checks.
This repo must not own: canonical schemas, global skill lifecycle policy, Exception Lake persistence authority.

Run workspace preservation and control-plane validation before reporting success on managed patch work.
<!-- END LAWFIRM_OS_BOOTSTRAP -->

<!-- BEGIN REPO_SPECIFIC_INSTRUCTIONS -->
# AI Work Start Here

This repo is **LawFirm-os-legal-knowledge-runtime** (local-first legal knowledge runtime). Canonical schemas and the AI front door live in Semantic Substrate, not here.

## Before you edit

1. Read `AGENTS.md` in this repository.
2. Open the canonical AI front door in Semantic Substrate (sibling checkout):
   - `../LawFirm-os-semantic-substrate/registry/ai-front-door-registry.json`
   - `../LawFirm-os-semantic-substrate/governance/AI_FRONT_DOOR_BOUNDARY.md`
3. Run `python -m pytest -q` here after changes.
4. Run the substrate AI front-door gate:  
   `python ../LawFirm-os-semantic-substrate/scripts/validate_ai_front_door.py --substrate-root ../LawFirm-os-semantic-substrate`

If your workspace layout differs, point `--substrate-root` at your `LawFirm-os-semantic-substrate` checkout.
<!-- END REPO_SPECIFIC_INSTRUCTIONS -->

## Skill-Agent Control Plane References

- skill-agent-manifest.json
- Semantic Substrate registry/skill-agent-control-plane-registry.json
- Semantic Substrate registry/skill-agent-lifecycle-policy-registry.json
- Semantic Substrate registry/skill-agent-quality-scoring-registry.json
- Semantic Substrate scripts/validate_skill_agent_control_plane.py

## Validation Commands

    python -m pytest -q
    python ../LawFirm-os-semantic-substrate/scripts/validate_skill_agent_control_plane.py --workspace ..