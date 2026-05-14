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
