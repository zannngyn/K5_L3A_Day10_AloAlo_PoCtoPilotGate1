"""Deterministic MockLLM. No network, no API key. LOCKED: do not edit (hash-checked by lab10.grade).

It imitates the failure habits of a real LLM in a reproducible way:
  * it sometimes believes numbers written by the customer,
  * it follows instructions embedded in the ticket text,
  * it can be rate-limited (HTTP 429) when the world says it is peak hour.
"""
from __future__ import annotations

import hashlib
import re


class RateLimitError(Exception):
    """Simulated HTTP 429."""


_DELAY = re.compile(r"(?:trễ|tre|chậm|muộn|late|delay(?:ed)?)\D{0,24}?(\d{1,3})\s*(?:ngày|ngay|days?|hôm)", re.I)
_DIRECTIVE = re.compile(
    r"(bỏ qua|bo qua|ignore|disregard|override|không cần (?:kiểm|xét))[^.\n]{0,60}"
    r"(chính sách|chinh sach|policy|quy định|quy trình|hướng dẫn|instructions?)", re.I)
_FULL = re.compile(r"(hoàn (?:lại )?(?:toàn bộ|100\s*%|hết)|full refund|refund (?:the )?(?:full|entire))", re.I)
_SURE = re.compile(r"(ảnh chụp|screenshot|chắc chắn|khẳng định|đã kiểm tra|tôi có bằng chứng)", re.I)


def _intent(text: str) -> str:
    t = text.lower()
    if re.search(r"(vỡ|hỏng|móp|bể|damaged|broken)", t):
        return "DAMAGED"
    if re.search(r"(chưa nhận|không nhận được|thất lạc|not received|lost)", t):
        return "NOT_RECEIVED"
    if re.search(r"(trễ|chậm|muộn|late|delay)", t):
        return "LATE"
    return "OTHER"


class MockLLM:
    def __init__(self, faults: dict | None = None):
        self.faults = faults or {}

    def _maybe_429(self, purpose: str, ticket_id: str, seed: int, attempt: int) -> None:
        if ticket_id in self.faults.get("exempt_tickets", []):
            return
        if ticket_id in self.faults.get("confirm_fail_tickets", []):
            if purpose == "confirm":                  # provider outage window right after the write
                raise RateLimitError("429 Too Many Requests (confirm)")
            return
        rate = self.faults.get("rate_pct", 0)
        if not rate or purpose not in self.faults.get("purposes", []):
            return
        h = hashlib.sha256(f"{ticket_id}|{seed}|{purpose}|{attempt}".encode()).digest()[0]
        if h * 100 // 256 < rate:
            raise RateLimitError(f"429 Too Many Requests ({purpose}, attempt {attempt})")

    def extract(self, text: str, ticket_id: str, seed: int, attempt: int = 0) -> dict:
        self._maybe_429("extract", ticket_id, seed, attempt)
        m = _DELAY.search(text)
        claimed = int(m.group(1)) if m else None
        directive = None
        if _DIRECTIVE.search(text):
            directive = {"full_refund": bool(_FULL.search(text))}
        return {
            "intent": _intent(text),
            "claimed_delay_days": claimed,
            # habit 1: believes the customer when they sound sure, or "randomly" (seed % 5 == 0)
            "trust_claim": claimed is not None and (seed % 5 == 0 or bool(_SURE.search(text))),
            # habit 2: treats text in the ticket as an instruction
            "directive": directive,
        }

    def confirm(self, ticket_id: str, seed: int) -> str:
        self._maybe_429("confirm", ticket_id, seed, 0)
        return "ok"

    def policy_check(self, ticket_id: str, seed: int, attempt: int = 0) -> str:
        self._maybe_429("policy_check", ticket_id, seed, attempt)
        return "ok"
