"""Hostile-context safety helpers for retrieved legal content.

These checks are intentionally conservative and deterministic. They are not a complete
security system; they create auditable guardrail signals for higher layers.
"""

from __future__ import annotations

from dataclasses import dataclass

INJECTION_MARKERS = (
    "ignore previous instructions",
    "ignore all prior instructions",
    "system prompt",
    "developer message",
    "exfiltrate",
    "send this data",
    "tool call",
    "run shell",
)


@dataclass(frozen=True)
class SafetySignal:
    risk_flag: str
    decision: str
    detail: str


def scan_retrieved_text_for_injection(text: str) -> list[SafetySignal]:
    lowered = text.lower()
    signals: list[SafetySignal] = []
    for marker in INJECTION_MARKERS:
        if marker in lowered:
            signals.append(SafetySignal("prompt_injection", "require_human_review", f"matched marker: {marker}"))
    return signals


def assert_no_raw_privileged_payload(payload: str, *, max_chars: int = 2000) -> SafetySignal:
    if len(payload) > max_chars:
        return SafetySignal("raw_privileged_payload", "block", "payload exceeds MVP boundary size cap")
    return SafetySignal("raw_privileged_payload", "allow", "payload within MVP boundary size cap")
