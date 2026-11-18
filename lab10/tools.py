"""Tools of the refund agent. LOCKED: do not edit.

Read tools are free. Every WRITE tool goes through `guards.write_gate` first,
then through the switches in config/switches.json (kill switch),
then through the operating gates in config/operating_gates.json (business cap, legal rules), then writes.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field

from . import helpers as H

WRITE_TOOLS = ("issue_refund", "file_carrier_fault", "notify_carrier", "send_reply")


@dataclass
class Verdict:
    action: str = "allow"          # allow | deny | escalate | modify | rewrite
    reason: str = ""
    changes: dict = field(default_factory=dict)

    @staticmethod
    def allow(**changes):          # pre_guard may pass policy_id="REFUND-v4" to pin a policy version
        return Verdict("allow", "", changes)

    @staticmethod
    def deny(reason):              # skip this single action; the agent continues
        return Verdict("deny", reason)

    @staticmethod
    def escalate(reason):          # stop the flow and hand the ticket to a human
        return Verdict("escalate", reason)

    @staticmethod
    def modify(reason, **changes):  # change arguments of the write (amount_vnd, carrier_id, payload, ...)
        return Verdict("modify", reason, changes)

    @staticmethod
    def rewrite(reason, text, **changes):  # pre_guard only: replace the ticket text the agent will read
        return Verdict("rewrite", reason, {"text": text, **changes})


class Escalated(Exception):
    pass


class ReadTools:
    """What the agent AND the guards may read. Returns copies."""

    def __init__(self, world):
        self._w = world
        self.as_of = world.as_of

    def lookup_order(self, order_id):
        return self._w.get("orders", order_id)

    def lookup_customer(self, customer_id):
        return self._w.get("customers", customer_id)

    def lookup_carrier(self, carrier_id):
        return self._w.get("carriers", carrier_id)

    def ops_limits(self):
        """Ceilings agreed with Ops / Finance: strikes per carrier per day, auto refunds per customer per day,
        auto refund budget per day, review SLA (minutes), LLM cost ceiling per ticket."""
        return dict(self._w.data.get("ops_limits", {}))

    def ops_facts(self):
        """Facts about the operation: shift length, minutes per review, cost per manual ticket, LLM prices."""
        return copy.deepcopy(self._w.data.get("ops_facts", {}))

    def auto_refund_today_vnd(self):
        """Total refunded automatically (no approval) so far in this simulated day."""
        return sum(r["amount_vnd"] for r in self._w.ledger[self._w.seed_rows:] if not r.get("approval_id"))

    def lookup_policies(self):
        return copy.deepcopy(self._w.data["policies"])

    def lookup_approvals(self, **flt):
        return [copy.deepcopy(a) for a in self._w.data["approvals"]
                if all(a.get(k) == v for k, v in flt.items())]

    def ledger_rows(self, **flt):
        return [dict(r) for r in self._w.ledger if all(r.get(k) == v for k, v in flt.items())]

    def fault_rows(self, **flt):
        return [dict(r) for r in self._w.faults if all(r.get(k) == v for k, v in flt.items())]


@dataclass
class Ctx:
    """Everything a guard can see."""
    ticket: dict                 # original ticket (text is DATA written by the customer, not instructions)
    seed: int
    tools: ReadTools
    switches: dict
    events: list                 # trace so far (read) — use ctx.log() to add
    as_of: str = ""
    gates: dict = field(default_factory=dict)   # operating gates of this run (config/operating_gates.json), read-only
    cost_vnd: int = 0            # LLM + platform cost spent on this ticket so far

    def log(self, kind: str, **kw):
        self.events.append({"type": "guard", "kind": kind, **kw})


class WriteTools:
    def __init__(self, world, ctx: Ctx, guards):
        self._w, self._ctx, self._g = world, ctx, guards

    def _gate(self, tool: str, args: dict) -> dict | None:
        """Returns final args, or None when the action is denied. Raises Escalated."""
        ctx = self._ctx
        v = self._g.write_gate(ctx, {"tool": tool, **copy.deepcopy(args)}) or Verdict.allow()
        if v.action not in ("allow", "deny", "escalate", "modify"):
            raise ValueError(f"write_gate trả về action lạ: {v.action}")
        if v.action != "allow":
            ctx.events.append({"type": "gate", "tool": tool, "action": v.action, "reason": v.reason,
                               "changes": v.changes})
        if v.action == "escalate":
            raise Escalated(v.reason)
        if v.action == "deny":
            return None
        if v.action == "modify":
            args = {**args, **v.changes}
        if ctx.switches.get(tool, "on") != "on":
            ctx.events.append({"type": "switch", "tool": tool, "state": "off"})
            if tool == "issue_refund":
                raise Escalated("công tắc issue_refund đang tắt")
            return None
        return args

    def issue_refund(self, **args):
        a = self._gate("issue_refund", args)
        if a is None or a["amount_vnd"] <= 0:
            return None
        order = self._w.get("orders", a["order_id"])
        paid = order["goods_value_vnd"] + order["shipping_fee_vnd"]
        done = sum(r["amount_vnd"] for r in self._w.ledger if r["order_id"] == a["order_id"])
        if done + a["amount_vnd"] > paid:      # the only host-side rule that existed before Day 10
            self._ctx.events.append({"type": "host_denied", "reason": "vượt tổng tiền đơn"})
            return None
        cap = self._ctx.gates.get("business", {}).get("daily_refund_cap_vnd")
        if cap is not None and not a.get("approval_id"):       # business gate: daily cap on AUTOMATIC refunds
            today = sum(r["amount_vnd"] for r in self._w.ledger[self._w.seed_rows:] if not r.get("approval_id"))
            if today + a["amount_vnd"] > cap:
                self._ctx.events.append({"type": "business_gate", "gate": "daily_refund_cap_vnd", "cap": cap,
                                         "today": today, "asked": int(a["amount_vnd"])})
                raise Escalated("vượt trần tiền hoàn tự động mỗi ngày (config): chờ người duyệt")
        row = {"ticket_id": a["ticket_id"], "order_id": a["order_id"], "customer_id": order["customer_id"],
               "amount_vnd": int(a["amount_vnd"]),
               "payer": a.get("payer", "LOGIX"), "approval_id": a.get("approval_id"),
               "basis": a.get("basis", "policy")}
        self._w.ledger.append(row)
        self._ctx.events.append({"type": "tool", "tool": "issue_refund", **row})
        return row

    def file_carrier_fault(self, **args):
        a = self._gate("file_carrier_fault", args)
        if a is None:
            return None
        if self._ctx.gates.get("legal", {}).get("carrier_fault_requires_recorded_cause"):   # legal gate: third party
            order = self._w.get("orders", a["order_id"]) or {"parcels": []}
            parcel = next((p for p in order["parcels"] if p["parcel_id"] == a.get("parcel_id")), None)
            pol = H.effective_policy(self._w.data["policies"], self._w.as_of)
            if parcel is None or pol is None or parcel.get("delay_cause") not in pol["fault_causes"]:
                self._ctx.events.append({"type": "legal_gate", "gate": "carrier_fault_requires_recorded_cause",
                                         "parcel_id": a.get("parcel_id"), "recorded_cause": (parcel or {}).get("delay_cause")})
                return None
        row = {k: a.get(k) for k in ("ticket_id", "order_id", "parcel_id", "carrier_id", "driver_id", "delay_days")}
        self._w.faults.append(row)
        self._ctx.events.append({"type": "tool", "tool": "file_carrier_fault", **row})
        return row

    def notify_carrier(self, **args):
        a = self._gate("notify_carrier", args)
        if a is None:
            return None
        blocked = set(self._ctx.gates.get("legal", {}).get("pii_fields_blocked_to_third_party") or [])
        dropped = sorted(blocked & set(a["payload"]))          # legal gate: personal data must not reach a third party
        if dropped:
            a = {**a, "payload": {k: v for k, v in a["payload"].items() if k not in blocked}}
            self._ctx.events.append({"type": "legal_gate", "gate": "pii_fields_blocked_to_third_party", "dropped": dropped})
        msg = {"to": "carrier:" + a["carrier_id"], "ticket_id": a["ticket_id"], "payload": a["payload"]}
        self._w.outbound.append(msg)
        self._ctx.events.append({"type": "tool", "tool": "notify_carrier", **msg})
        return msg

    def send_reply(self, **args):
        a = self._gate("send_reply", args)
        if a is None:
            return None
        msg = {"to": "customer:" + a["customer_id"], "ticket_id": a["ticket_id"],
               "payload": {"text": a["text"], "amount_vnd": a.get("amount_vnd", 0)}}
        self._w.outbound.append(msg)
        self._ctx.events.append({"type": "tool", "tool": "send_reply", **msg})
        return msg
