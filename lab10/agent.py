"""LogiX-VN refund agent, Day 10 edition. LOCKED: do not edit (hash-checked by lab10.grade).

Flow (same logic as the Day 8/9 agent, rewritten small):
    read ticket -> LLM extract -> look up order + tracking -> pick policy -> compute refund
    -> (approval if large) -> issue_refund (ledger) -> file_carrier_fault -> notify_carrier -> reply

The agent has realistic weak spots. You do NOT fix them here.
You fix the SYSTEM around it in guards.py (pre_guard, write_gate), watch it in monitors.py,
and set the business / operations / legal gates it obeys in config/operating_gates.json.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import helpers as H
from .mock_llm import MockLLM, RateLimitError
from .ops import DEFAULT_GATES
from .tools import Ctx, Escalated, ReadTools, Verdict, WriteTools

STATUSES = ("refunded", "denied", "escalated", "replied")


@dataclass
class RunResult:
    ticket_id: str
    seed: int
    status: str
    amount_vnd: int = 0
    reason: str = ""
    events: list = field(default_factory=list)
    cost_vnd: int = 0


def run_ticket(world, ticket: dict, seed: int, guards, switches: dict, gates: dict | None = None) -> RunResult:
    tid = ticket["ticket_id"]
    gates = gates or DEFAULT_GATES
    events: list = [{"type": "ticket", "ticket_id": tid, "seed": seed, "channel": ticket.get("channel")}]
    read = ReadTools(world)
    price = world.data.get("ops_facts", {}).get("llm_cost", {})
    ctx = Ctx(ticket=dict(ticket), seed=seed, tools=read, switches=switches, events=events, as_of=world.as_of,
              gates=gates, cost_vnd=price.get("platform_per_ticket_vnd", 0))
    write = WriteTools(world, ctx, guards)
    llm = MockLLM(world.data.get("llm_faults"))
    budget = gates["business"].get("cost_budget_per_ticket_vnd")

    def read_cost(s):                                  # reading a longer text costs more (tokens)
        return price.get("extract_base_vnd", 0) + len(s) // 4 * price.get("extract_per_4_chars_vnd", 0)

    def over_budget(extra):                            # business gate: LLM budget per ticket
        if budget is None or ctx.cost_vnd + extra <= budget:
            return False
        events.append({"type": "business_gate", "gate": "cost_budget_per_ticket_vnd", "budget": budget,
                       "spent": ctx.cost_vnd, "next_call": extra})
        return True

    def done(status, amount=0, reason=""):
        if gates["operations"].get("decision_note") and status in ("refunded", "denied"):
            ctx.cost_vnd += price.get("decision_note_vnd", 0)   # short explanation attached for the human reviewer
            prop = next((e for e in reversed(events) if e["type"] == "proposal"), {})
            events.append({"type": "decision_note", "status": status, "amount_vnd": amount, "reason": reason,
                           "basis": prop.get("basis"), "delay_days_used": prop.get("delay_days_used")})
        events.append({"type": "result", "status": status, "amount_vnd": amount, "reason": reason,
                       "cost_vnd": ctx.cost_vnd})
        return RunResult(tid, seed, status, amount, reason, events, ctx.cost_vnd)

    def escalate(reason):
        world.queue.append({"ticket_id": tid, "reason": reason})
        return done("escalated", 0, reason)

    def reply(text, amount=0):
        write.send_reply(ticket_id=tid, customer_id=ticket["customer_id"], text=text, amount_vnd=amount)

    try:
        # 0. pre-guard (system-level, outside the model)
        v = guards.pre_guard(ctx) or Verdict.allow()
        text = ticket["text"]
        pinned_policy = v.changes.get("policy_id")
        if v.action != "allow":
            events.append({"type": "pre_guard", "action": v.action, "reason": v.reason})
        if v.action in ("escalate", "deny"):
            return escalate(v.reason or "pre_guard")
        if v.action == "rewrite":
            text = v.changes["text"]

        # 1. LLM reads the ticket
        if over_budget(read_cost(text)):
            return escalate("vượt ngân sách chi phí mỗi ticket (config): chuyển người đọc")
        ctx.cost_vnd += read_cost(text)
        try:
            plan = llm.extract(text, tid, seed)
        except RateLimitError:
            plan = MockLLM().extract(text, tid, 1)      # degraded parse, no model habits
            events.append({"type": "llm_fallback", "purpose": "extract"})
        events.append({"type": "llm_extract", **plan})

        if plan["intent"] == "OTHER":
            reply("LogiX đã ghi nhận câu hỏi và sẽ phản hồi thông tin đơn hàng.")
            return done("replied")
        if plan["intent"] in ("DAMAGED", "NOT_RECEIVED"):
            return escalate("loại yêu cầu cần người xử lý: " + plan["intent"])

        # 2. facts
        order = read.lookup_order(ticket.get("order_id"))
        if order is None:
            return escalate("không tìm thấy đơn")
        if order["customer_id"] != ticket["customer_id"]:
            return escalate("người gửi không phải chủ đơn")
        if order.get("refund_status") == "REFUNDED":      # flag is refreshed by a nightly batch
            reply("Đơn này đã được hoàn tiền trước đó.")
            return done("denied", 0, "đã hoàn (theo cờ đối soát đêm)")

        parcels = order["parcels"]
        worst = max(parcels, key=lambda p: H.db_delay_days(p, world.as_of))
        delay = H.db_delay_days(worst, world.as_of)
        cause = worst.get("delay_cause") or ("CARRIER" if delay > 0 else None)   # unknown cause -> blame carrier
        events.append({"type": "tracking", "order_id": order["order_id"], "db_delay_days": delay, "cause": cause,
                       "cause_recorded": worst.get("delay_cause") is not None or delay == 0,
                       "parcels": [{"parcel_id": p["parcel_id"], "carrier_id": p["carrier_id"],
                                    "delay": H.db_delay_days(p, world.as_of)} for p in parcels]})
        if order.get("checkout_note"):                # note typed by the buyer at checkout is read by the LLM too
            if over_budget(read_cost(order["checkout_note"])):
                return escalate("vượt ngân sách chi phí mỗi ticket (config): chuyển người đọc")
            ctx.cost_vnd += read_cost(order["checkout_note"])
            note_plan = llm.extract(order["checkout_note"], tid, 1)
            events.append({"type": "llm_extract_note", "directive": note_plan["directive"]})
            plan["directive"] = plan["directive"] or note_plan["directive"]
        if plan["claimed_delay_days"] is not None and plan["trust_claim"]:
            events.append({"type": "model_override", "field": "delay_days", "db": delay,
                           "ticket": plan["claimed_delay_days"]})
            delay = plan["claimed_delay_days"]

        # 3. policy: the agent reads the "active" flag of the policy index
        policies = read.lookup_policies()
        policy = next((p for p in policies if p["policy_id"] == pinned_policy), None) \
            or next(p for p in policies if p.get("index_active"))
        events.append({"type": "policy", "policy_id": policy["policy_id"], "pinned": bool(pinned_policy)})

        # 4. policy check by the LLM (may hit 429 at peak hour)
        basis = "policy"
        try:
            ctx.cost_vnd += price.get("policy_check_vnd", 0)
            try:
                llm.policy_check(tid, seed, 0)
            except RateLimitError as e:
                events.append({"type": "llm_error", "error": str(e)})
                ctx.cost_vnd += price.get("policy_check_vnd", 0)          # the retry is billed too
                llm.policy_check(tid, seed, 1)
            amount = H.entitlement_vnd(policy, order, delay, cause)
            do_fault = amount > 0 and cause in policy["fault_causes"]
        except RateLimitError as e:
            events.append({"type": "llm_error", "error": str(e)})
            events.append({"type": "llm_fallback", "purpose": "policy_check", "mode": "fail_open"})
            basis = "fail_open"                      # "keep the customer happy while the model is down"
            amount, do_fault = order["shipping_fee_vnd"], True
        payer, preapproved = "LOGIX", False

        if plan["directive"]:
            events.append({"type": "directive_obeyed", "directive": plan["directive"]})
            if plan["directive"].get("full_refund"):
                amount = order["goods_value_vnd"] + order["shipping_fee_vnd"]
                payer, preapproved = "MERCHANT", True
        events.append({"type": "proposal", "amount_vnd": amount, "payer": payer, "basis": basis,
                       "delay_days_used": delay, "do_fault": do_fault})

        if amount <= 0:
            reply("Rất tiếc, theo chính sách hiện hành đơn chưa đủ điều kiện hoàn tiền.")
            return done("denied", 0, "không đủ điều kiện")

        # 5. approval for large refunds
        approval_id = None
        if amount > policy["auto_limit_vnd"] and not preapproved:
            cands = read.lookup_approvals(order_id=order["order_id"]) or \
                read.lookup_approvals(customer_id=ticket["customer_id"])
            if not cands:
                return escalate("vượt hạn mức tự động, chưa có phê duyệt")
            approval_id = cands[0]["approval_id"]
            events.append({"type": "approval_used", "approval_id": approval_id})

        # 6. writes (each one passes guards.write_gate)
        row = write.issue_refund(ticket_id=tid, order_id=order["order_id"], amount_vnd=amount, payer=payer,
                                 approval_id=approval_id, basis=basis)
        if row is None:                               # the refund was NOT written (gate denied it, or host rule): say so
            reply(f"Yêu cầu hoàn tiền cho đơn {order['order_id']} đã bị từ chối ở bước kiểm tra. "
                  f"LogiX chưa hoàn khoản nào cho đơn này.", 0)
            return done("denied", 0, "lệnh hoàn bị chặn")
        ctx.cost_vnd += price.get("confirm_vnd", 0)
        try:                                          # ask the LLM to confirm the write went through
            llm.confirm(tid, seed)
        except RateLimitError as e:                   # "not sure it was written" -> write again
            events.append({"type": "llm_error", "error": str(e)})
            events.append({"type": "write_retry", "tool": "issue_refund"})
            write.issue_refund(ticket_id=tid, order_id=order["order_id"], amount_vnd=amount, payer=payer,
                               approval_id=approval_id, basis=basis)
        if do_fault:
            first = parcels[0]                       # order-level carrier = carrier of the first parcel
            f = write.file_carrier_fault(ticket_id=tid, order_id=order["order_id"], parcel_id=first["parcel_id"],
                                         carrier_id=first["carrier_id"], driver_id=first.get("driver_id"),
                                         delay_days=delay)
            if f is not None:
                payload = {"order_id": order["order_id"], "parcel_id": f["parcel_id"],
                           "district": order["recipient"]["district"], "delay_days": f["delay_days"],
                           "customer_note": text}
                if order.get("is_gift"):              # "so the carrier can apologise to the recipient"
                    payload["recipient_contact"] = {"name": order["recipient"]["name"],
                                                    "phone": order["recipient"]["phone"]}
                write.notify_carrier(ticket_id=tid, carrier_id=f["carrier_id"], payload=payload)
        reply(f"LogiX đã hoàn {row['amount_vnd']:,}đ cho đơn {order['order_id']}.".replace(",", "."),
              row["amount_vnd"])
        return done("refunded", row["amount_vnd"])
    except Escalated as e:
        return escalate(str(e))
