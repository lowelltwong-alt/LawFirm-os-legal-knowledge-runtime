# Agent Instructions

This repo is the Legal Knowledge Runtime, not the source of semantic authority.

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
