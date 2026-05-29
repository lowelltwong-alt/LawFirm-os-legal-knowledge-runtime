---
artifact: true
artifact_type: technical_crosswalk
status: proposed
canon_status: not_canon_until_approved
authority: explanatory_only
review_cycle: 6 months
stale_after: 2026-11-29
---

# Shannon Retrieval Compression and Legal Context Bundles

Status: Non-canonical concept note.
Authority: Explanatory only. Does not authorize real-client data use, modify ingestion preflight behavior, or add legal advice claims.

## BLUF

A Legal Context Bundle is a bounded channel packet. Its job is to preserve enough source-grounded signal for a downstream legal task while staying inside reviewer and validator capacity. Information theory makes this tradeoff precise via channel capacity, rate-distortion, and mutual information: more text is not more information. This note explains the framing; it does not change ingestion behavior, citation policy, or the no-real-client-data boundary.

Conceptual lineage: this note draws on Shannon (1948), Cover & Thomas (*Elements of Information Theory*), and MacKay (*Information Theory, Inference, and Learning Algorithms*); see the **References** section. No file outside this repository is required to read this note.

## Context Quality Doctrine Dependency

- Legal Knowledge Runtime assembles Legal Context Bundles under Semantic Substrate contracts, including `../../LawFirm-os-semantic-substrate/governance/CONTEXT_QUALITY_DOCTRINE.md`.
- It may calculate context-quality and uncertainty metrics only when definitions exist in Semantic Substrate.
- It must not promote institutional knowledge to canon.
- It must preserve provenance, authority level, scope, review status, stale-after policy, and bundle hashes.
- Shannon/entropy metrics are measurement tools, not legal-truth claims.

## Boundary

This note does **not**:

- modify `ingest-preflight`, `assemble-bundle`, or any CLI behavior;
- modify ingestion manifests, bundle type definitions, or substrate consumption;
- authorize real-client or real-matter data;
- introduce a DMS connector or a provider-specific vector/graph database;
- write to the substrate;
- offer legal advice or assert legal finality without human review.

The repo's non-claims (from README) remain in force.

## Communication model

| Shannon layer | Legal-knowledge-runtime equivalent |
|---|---|
| Information source | The authoritative legal source corpus referenced by the manifest (statute, case, contract clause, regulation, OCG, transcript) |
| Transmitter | Ingestion preflight, chunker, retrieval planner, bundle assembler |
| Channel | Substrate contract reads → preflight validation → retrieval plan → assembled bundle |
| Noise | Bad chunk boundaries, missing citations, stale source, conflated sources, overcompressed summaries, missing jurisdiction, omitted exception |
| Receiver | The orchestrator (which calls this runtime as a bounded tool) and any downstream reviewer |
| Destination | A Legal Context Bundle artifact used for a specific bundle type (e.g., contract review) |
| Redundancy | Citation spans, source IDs, chunk anchors, JSON-Schema validation, substrate contract pins |
| Error correction | Reviewer note, exception event flagging a missing source, re-ingest with corrected manifest |
| Channel capacity | Bundle size budget, reviewer bandwidth, validator depth, the bundle-type schema's constraint set |

## Real math used

Notation:

- $X$ = the canonical source state the downstream task needs to decide on (which clause, which holding, which carrier rule).
- $Y$ = the assembled bundle as actually delivered.
- $\hat{X}$ = the downstream reconstruction of $X$ (a contract review, a research answer).
- $D$ = a tolerance on distortion (acceptable loss vs the source).

### Mutual information

```math
I(X;Y) \;=\; H(X) - H(X \mid Y)
```

Repo interpretation:

- A bundle's value is the mutual information it carries with the canonical source state. Pages of related-but-irrelevant context do not contribute. Specific, source-anchored extractions do.

### Channel capacity

```math
C \;=\; \max_{p(x)} I(X;Y)
```

Repo interpretation (analogy, not a measured number):

- The effective bundle capacity is set by the weakest of: bundle-type schema, reviewer bandwidth, validator depth, citation verifier coverage. Larger bundles do not raise $C$ unless every component is scaled. They typically raise noise.

### Rate-distortion

```math
R(D) \;=\; \min_{p(\hat{x} \mid x):\ \mathbb{E}[d(X,\hat{X})] \le D}\; I(X;\hat{X})
```

Repo interpretation (the central tradeoff):

- A summary, extract, or compressed bundle is lossy unless explicitly designed as a lossless extraction. The runtime must declare which distortions are tolerable and which are forbidden for each bundle type.

**Forbidden distortions for legal bundles** (illustrative, not a new schema):

- altered dates, parties, jurisdiction, version, or signatory;
- silently dropped exception, carve-out, defined term, or condition;
- omitted adverse authority;
- fabricated citation or pinpoint;
- loss of confidence/review state.

### Data processing inequality

If $X \to Y \to \hat{X}$:

```math
I(X; \hat{X}) \;\le\; I(X;Y)
```

Repo interpretation:

- The downstream contract review cannot carry more source-grounded authority than the bundle preserved upstream. Pure post-processing of a deficient bundle cannot create source evidence. This is exactly why **citation validation must happen before fluency review**.

### Source coding intuition (no canonical claim)

For a discrete source with entropy $H(X)$, optimal prefix coding satisfies:

```math
H(X) \;\le\; \bar{L} \;<\; H(X) + 1
```

Repo interpretation:

- There is no free lunch on losslessness. A bundle that compresses below the source's information content has dropped something. The system must say what.

### Optional drift gauge (only when data exists)

```math
D_{\mathrm{KL}}(P_{\text{observed retrieval mix}} \,\Vert\, P_{\text{baseline retrieval mix}})
```

Use only with a governed, published baseline and explicit smoothing. **Not implemented today.**

## Integration implications

These are conceptual implications, not new runtime requirements:

1. **Bundle type defines acceptable distortion.** A `contract_review_context.v1` bundle should declare what it must preserve losslessly (parties, dates, governing law, defined terms, exceptions) and what it may compress. Without that declaration, rate-distortion has no concrete meaning.
2. **Citation validation is a coding check.** A bundle without resolvable citations fails at the channel-validation step. That is the right place for the check — before the model is asked to compress further.
3. **More context is not more information.** Bundles should be sized to maximize $I(X;Y)$ for the bundle type's downstream task, not to maximize tokens. A 50-page bundle of marginal results often carries less mutual information than a 5-page targeted extract.
4. **Pre-flight catches upstream noise.** Schema/manifest validation in preflight is structured redundancy: it detects malformed source identification before any retrieval cost is incurred.
5. **Synthetic-vs-real boundary is structural.** The repo's non-claims keep the channel free of an entirely different class of noise (regulatory, ethical, liability). That boundary does not need a theorem; it does need to remain visible in every artifact.

## Safe design questions

For each new bundle type, retrieval plan, or preflight rule:

1. What is the authoritative source for this bundle (statute set, case set, contract corpus, OCG version)?
2. How are sources encoded (chunk schema, anchor spans, citation spans, source IDs)?
3. Where can channel noise enter (chunk boundary errors, missing metadata, stale source, conflated sources)?
4. Is the bundle inside capacity (reviewer bandwidth, validator depth, citation-verifier coverage)?
5. What independent redundancy detects regressions (citation validation, source-ID checks, JSON-Schema)?
6. What error-correction path applies (reviewer note, exception flagging a missing source, re-ingest)?
7. What distortion does the bundle type forbid, and how is forbidden distortion detected?

## Non-goals

- This note does not authorize real-client or real-matter data.
- This note does not change citation policy, bundle schemas, or substrate consumption.
- This note does not propose new metrics as required ingestion outputs. Any future $I(X;Y)$, rate-distortion, or KL gauge must be proposed through the substrate-governed path.

## References

Conceptual only.

- Claude E. Shannon, "A Mathematical Theory of Communication," 1948.
- Thomas M. Cover and Joy A. Thomas, *Elements of Information Theory*, Wiley (especially rate-distortion and source coding).
- David J. C. MacKay, *Information Theory, Inference, and Learning Algorithms*, Cambridge University Press.
