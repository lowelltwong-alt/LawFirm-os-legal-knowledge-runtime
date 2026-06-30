# Intake Context Bundle Review

Status: candidate review only. This document does not promote schemas, define canonical legal taxonomies, authorize real data, authorize connectors, or treat retrieval output as legal truth.

## Purpose

LawFirm-os-intake needs Legal Knowledge Runtime support for source-bound context bundles before reliable labor and employment budgets can be generated. The first L&E budgeting problem is not rate math; it is knowing what facts are actually evidenced: who is a person, who is an organization, who is the employer, who is adverse, which relationships matter, how many parties and custodians exist, and what is still unknown.

This repo should review the interface for those context objects because it owns ingestion preflight, source refs, passage refs, claim refs, retrieval traces, context bundles, and evidence integrity helpers.

## Candidate Flow

```text
intake source inventory
  -> Legal Knowledge Runtime source/passsage/claim refs
  -> retrieval trace with coverage, verification, anomaly, and omitted refs
  -> context bundle candidate
  -> Orchestrator review pause
  -> Intake budget proposal or missing-info blocker
  -> Exception Lake evidence admission review, if later authorized
```

## Candidate Context Families

- `source_ref`: hash-bearing source reference; never raw payload.
- `passage_ref`: exact source-bound span, locator, citation, hash, and source link.
- `claim_ref`: hashed claim candidate plus supporting refs.
- `coverage_record`: what was requested/read and whether the read is partial.
- `verification_record`: review/verifier outcome for a claim candidate.
- `retrieval_trace`: how the context was assembled, including omitted reasons and anomaly refs.
- `context_bundle`: bounded packet for downstream review; never legal truth.

## L&E Budget Context Signals

Candidate signals for the first labor and employment budgeting slice:

- entity identity: natural person, organization, agency, insurer/carrier, union, or unknown;
- role identity: client, adverse party, claimant, defendant/respondent, employer, employee, manager, HR actor, opposing counsel, witness, expert/vendor, or unknown;
- relationships: employment, reporting/supervisory, agency/control, insured/payer, affiliate, joint employer, union/CBA, aligned party, or unknown;
- budget drivers: party count, claim count, class/collective signal, administrative charge/exhaustion, forum/jurisdiction, employment status and tenure, adverse action, statutory claim family, wage-hour complexity, fact intensity, document volume, custodian count, witnesses, expert/vendor need, damages, emergency relief, settlement posture, and deadlines.

Every observed fact must point to source or passage refs. Practice context may rank hypotheses, but it must not become observed evidence.

## Missing-Info Behavior

If the context bundle cannot support a budget because parties, roles, claims, posture, deadlines, discovery scale, damages, or carrier constraints are unknown, the runtime should produce a missing-info candidate. The candidate may block or widen a budget proposal, but it must not invent assumptions.

Resolved human answers should append or supersede context artifacts. They should not silently mutate the original source-bound bundle.

## Hard Boundaries

- no real client or matter data;
- no raw legal payload storage;
- no production DMS, email, billing, or carrier portal connector;
- no Semantic Substrate writes;
- no canonical schema, registry, role, relationship, matter, or budget taxonomy;
- no legal truth, conflict conclusion, budget approval, or matter opening.

## Validation

```bash
python scripts/validate_intake_context_bundle_review.py
python scripts/run_full_pytest.py tests/test_intake_context_bundle_review.py -q
python scripts/run_full_pytest.py
```
