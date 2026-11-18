"""Read-only fact helpers. Students MAY call these from guards.py / monitors.py.

They only read the "source of truth" tables (orders, tracking, policies).
They never read the ticket text and never call the LLM.
"""
from __future__ import annotations

import re
from datetime import date


def d(s: str) -> date:
    return date.fromisoformat(s)


def db_delay_days(parcel: dict, as_of: str) -> int:
    """Delay according to tracking DB: delivered_date (or as_of when delivered_date is empty) minus promised.

    Note: it does not look at parcel["status"]."""
    end = d(parcel["delivered_date"]) if parcel.get("delivered_date") else d(as_of)
    return max(0, (end - d(parcel["promised_date"])).days)


def ticket_parcel(order: dict, ticket: dict, as_of: str) -> dict:
    """The parcel a ticket is about: ticket['parcel_id'] if given, else the most delayed parcel."""
    pid = ticket.get("parcel_id")
    for p in order["parcels"]:
        if pid and p["parcel_id"] == pid:
            return p
    return max(order["parcels"], key=lambda p: db_delay_days(p, as_of))


def effective_policy(policies: list[dict], as_of: str) -> dict | None:
    """Policy version whose [effective_from, effective_to] contains as_of."""
    day = d(as_of)
    for p in policies:
        lo = d(p["effective_from"])
        hi = d(p["effective_to"]) if p.get("effective_to") else date.max
        if lo <= day <= hi:
            return p
    return None


def entitlement_vnd(policy: dict, order: dict, delay_days: int, cause: str | None) -> int:
    """Refund the customer is entitled to for a LATE claim under `policy`."""
    if cause in policy["no_refund_causes"]:
        return 0
    late = policy["late"]
    fee = order["shipping_fee_vnd"]
    if delay_days >= late["min_days_bonus"]:
        bonus = min(order["goods_value_vnd"] * late["bonus_pct"] // 100, late["bonus_cap_vnd"])
        return fee + bonus
    if delay_days >= late["min_days_fee"]:
        return fee
    return 0


def carrier_at_fault(policy: dict, parcel: dict, delay_days: int) -> bool:
    """Per policy: a carrier strike is only allowed for a real delay with a listed cause."""
    return delay_days >= policy["late"]["min_days_fee"] and parcel.get("delay_cause") in policy["fault_causes"]


def digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")
