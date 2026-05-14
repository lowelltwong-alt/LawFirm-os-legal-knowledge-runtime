"""Deterministic document-integrity helpers.

The MVP does not edit real legal documents. These helpers support synthetic fixtures
and future claim-check based validation.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class IntegrityResult:
    check_type: str
    status: str
    detail: str


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def compare_text_hashes(baseline_text: str, candidate_text: str) -> IntegrityResult:
    baseline = sha256_text(baseline_text)
    candidate = sha256_text(candidate_text)
    if baseline == candidate:
        return IntegrityResult("hash_match", "pass", "baseline and candidate hashes match")
    return IntegrityResult("hash_match", "warn", f"hash changed from {baseline} to {candidate}")


def require_terms_preserved(baseline_text: str, candidate_text: str, terms: list[str]) -> list[IntegrityResult]:
    results: list[IntegrityResult] = []
    for term in terms:
        if term in baseline_text and term not in candidate_text:
            results.append(IntegrityResult("defined_term_preservation", "fail", f"missing defined term: {term}"))
        else:
            results.append(IntegrityResult("defined_term_preservation", "pass", f"term preserved or not applicable: {term}"))
    return results
