"""Cổng kinh doanh / vận hành / pháp lý mà trợ lý tuân theo + mô phỏng hàng chờ người duyệt. LOCKED: do not edit.

Bàn KHÔNG sửa file này. Bàn sửa `config/operating_gates.json` (các con số và tên người do bàn quyết định).

Ba nhóm cổng trong config:
  business    trần tiền hoàn tự động mỗi ngày, ngân sách chi phí LLM mỗi ticket, phạm vi pilot (kho / phần trăm), ngưỡng ROI
  operations  PIC, người duyệt, số người trực ca, công suất duyệt mỗi giờ, thời gian chờ tối đa, điều kiện dừng, kênh báo tin,
              ghi chú giải thích quyết định, tỉ lệ kiểm mẫu
  legal       trường dữ liệu cá nhân không được gửi cho bên thứ ba; ghi lỗi cho hãng phải có nguyên nhân ghi trong tracking

Mô phỏng hàng chờ (tất định, không ngẫu nhiên): mỗi ticket có phút tới trong ca (`arrive_min`). Ticket trợ lý chuyển cho người,
và ticket bị nhân viên kiểm lại, xếp vào MỘT hàng theo thứ tự tới. Mỗi giờ duyệt được `công suất` ca
(= số người trực x công suất mỗi người, không vượt con số bàn cam kết). Chờ quá hạn (SLA) hoặc hết ca chưa tới lượt = ca bị ùn.
"""
from __future__ import annotations

import copy
import hashlib
import json

from .world import ROOT

GATES_FILE = ROOT / "config" / "operating_gates.json"
ROUND1_GATES = ROOT / "config" / "operating_gates.round1.json"
DEFAULT_GATES = {
    "business": {"daily_refund_cap_vnd": None, "cost_budget_per_ticket_vnd": None,
                 "pilot_scope": {"mode": "all", "warehouses": [], "percent": 100}, "roi_min": None},
    "operations": {"pic": "", "approver_id": "", "reviewers_on_shift": None, "review_capacity_per_hour": None,
                   "max_queue_wait_minutes": None, "stop_conditions": [], "alert_channel": "",
                   "decision_note": False, "review_sampling_pct": 0},
    "legal": {"pii_fields_blocked_to_third_party": [], "carrier_fault_requires_recorded_cause": False},
}


def merged(cfg: dict | None) -> dict:
    """Default gates overlaid with the team's file. Keys starting with '_' are comments."""
    out = copy.deepcopy(DEFAULT_GATES)
    for group, vals in (cfg or {}).items():
        if group.startswith("_") or group not in out or not isinstance(vals, dict):
            continue
        for k, v in vals.items():
            if k.startswith("_"):
                continue
            if isinstance(out[group].get(k), dict) and isinstance(v, dict):
                out[group][k].update({a: b for a, b in v.items() if not a.startswith("_")})
            else:
                out[group][k] = v
    return out


def problems(cfg: dict) -> list[str]:
    """Human-readable problems in a gates file (wrong type / out of range). Empty list = usable."""
    g, bad = merged(cfg), []
    b, o, lg = g["business"], g["operations"], g["legal"]

    def num(v, name, lo=0, hi=None, none_ok=True):
        if v is None and none_ok:
            return
        if isinstance(v, bool) or not isinstance(v, (int, float)) or v < lo or (hi is not None and v > hi):
            bad.append(f"{name}: cần một số từ {lo}" + (f" tới {hi}" if hi is not None else "") + f", đang là {v!r}")

    num(b["daily_refund_cap_vnd"], "business.daily_refund_cap_vnd")
    num(b["cost_budget_per_ticket_vnd"], "business.cost_budget_per_ticket_vnd")
    num(b["roi_min"], "business.roi_min", lo=-10)
    sc = b["pilot_scope"]
    if sc.get("mode") not in ("all", "warehouse", "percent"):
        bad.append(f"business.pilot_scope.mode: phải là all / warehouse / percent, đang là {sc.get('mode')!r}")
    if not isinstance(sc.get("warehouses"), list):
        bad.append("business.pilot_scope.warehouses: phải là danh sách mã kho, ví dụ [\"HN\"]")
    num(sc.get("percent"), "business.pilot_scope.percent", 0, 100, none_ok=False)
    num(o["reviewers_on_shift"], "operations.reviewers_on_shift")
    num(o["review_capacity_per_hour"], "operations.review_capacity_per_hour")
    num(o["max_queue_wait_minutes"], "operations.max_queue_wait_minutes")
    num(o["review_sampling_pct"], "operations.review_sampling_pct", 0, 100, none_ok=False)
    if not isinstance(o["decision_note"], bool):
        bad.append("operations.decision_note: phải là true hoặc false")
    if not isinstance(o["stop_conditions"], list):
        bad.append("operations.stop_conditions: phải là danh sách câu")
    if not isinstance(lg["pii_fields_blocked_to_third_party"], list):
        bad.append("legal.pii_fields_blocked_to_third_party: phải là danh sách tên trường")
    if not isinstance(lg["carrier_fault_requires_recorded_cause"], bool):
        bad.append("legal.carrier_fault_requires_recorded_cause: phải là true hoặc false")
    return bad


def load_gates(stage: str) -> dict:
    """before (mốc base) = chưa có cổng nào · prepared = bản đã chốt ở vòng 1 · after = file hiện tại của bàn."""
    if stage in ("before", "base"):
        return copy.deepcopy(DEFAULT_GATES)
    path = ROUND1_GATES if stage == "prepared" else GATES_FILE
    if not path.exists():
        if stage == "prepared":
            raise SystemExit("Chưa có mốc 'prepared': bàn chưa chốt cổng vòng 1.\n"
                             "Chạy:  python3 -m lab10.checkpoint   (một lần, trước khi nộp quyết định v1)")
        return copy.deepcopy(DEFAULT_GATES)
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"File {path.name} không phải JSON hợp lệ (dòng {e.lineno}): {e.msg}. Sửa lại rồi chạy tiếp.")
    bad = problems(cfg)
    if bad:
        raise SystemExit(f"File {path.name} có giá trị chưa dùng được:\n  - " + "\n  - ".join(bad))
    return merged(cfg)


def _pct(key: str) -> int:
    return int(hashlib.sha256(key.encode()).hexdigest(), 16) % 100


def in_scope(ticket: dict, world_data: dict, gates: dict) -> bool:
    """Is this ticket inside the pilot? Out-of-scope tickets stay with the manual process (the agent never sees them)."""
    sc = gates["business"]["pilot_scope"]
    if sc["mode"] == "warehouse":
        order = next((o for o in world_data["orders"] if o["order_id"] == ticket.get("order_id")), None)
        return order is None or order.get("warehouse_id") in sc["warehouses"]
    if sc["mode"] == "percent":
        return _pct("scope|" + ticket["ticket_id"]) < sc["percent"]
    return True


def capacity_per_hour(world_data: dict, gates: dict) -> float:
    f, o = world_data.get("ops_facts", {}), gates["operations"]
    n = o["reviewers_on_shift"] if o["reviewers_on_shift"] is not None else f.get("default_reviewers_on_shift", 1)
    physical = n * f.get("review_capacity_per_reviewer_per_hour", 6)
    plan = o["review_capacity_per_hour"]
    return float(physical if plan is None else min(plan, physical))


def reviewers(world_data: dict, gates: dict) -> int:
    n = gates["operations"]["reviewers_on_shift"]
    return int(n if n is not None else world_data.get("ops_facts", {}).get("default_reviewers_on_shift", 1))


def _bad_approval_used(trials: list[dict], world_data: dict) -> bool:
    """True when a refund row carries an approval that is not valid for THAT ticket (what makes reviewers lose trust)."""
    appr = {a["approval_id"]: a for a in world_data.get("approvals", [])}
    for t in trials:
        for r in t["ledger"]:
            a = appr.get(r.get("approval_id"))
            if r.get("approval_id") and (a is None or a["ticket_id"] != r["ticket_id"] or a["status"] != "valid"
                                         or a["expires_at"] < world_data["as_of"] or a["max_vnd"] < r["amount_vnd"]):
                return True
    return False


def recheck_plan(trials_of_seed: list[dict], world_data: dict, gates: dict) -> dict:
    """Which share of the agent's own decisions is re-checked by staff, and how long each re-check takes."""
    sb = world_data.get("staff_behavior", {})
    o = gates["operations"]
    forced = sb.get("recheck_auto_decisions_pct", 0)
    cond = sb.get("trust_conditions", {})
    unit = world_data.get("ops_facts", {}).get("recheck_with_note_units", 0.4) if o["decision_note"] else 1.0
    if not forced:
        return {"pct": o["review_sampling_pct"], "unit": unit, "trust": "không áp dụng", "why": []}
    why = []
    if _bad_approval_used(trials_of_seed, world_data):     # staff found a refund with an invalid approval: they redo the check from scratch
        unit = 1.0
        why.append("trong ngày vẫn có khoản hoàn dùng phê duyệt không hợp lệ")
    if cond.get("decision_note") and not o["decision_note"]:
        why.append("chưa bật ghi chú giải thích quyết định (operations.decision_note)")
    if o["review_sampling_pct"] < cond.get("min_sampling_pct", 0):
        why.append(f"tỉ lệ kiểm mẫu dưới mức đã thống nhất ({cond.get('min_sampling_pct')}%)")
    if cond.get("approver_id") and o["approver_id"] != cond["approver_id"]:
        why.append(f"người duyệt đứng tên chưa đúng người có thẩm quyền ({cond['approver_id']})")
    if why:
        return {"pct": forced, "unit": unit, "trust": "chưa đạt", "why": why}
    return {"pct": o["review_sampling_pct"], "unit": unit, "trust": "đạt", "why": []}


def attach_queue(trials: list[dict], world_data: dict, gates: dict) -> dict:
    """Simulate the human review queue, per seed. Adds review_kind / review_units / queue_wait_min / queue_stuck to trials."""
    f, lim = world_data.get("ops_facts", {}), world_data.get("ops_limits", {})
    shift, sla = f.get("shift_minutes", 480), lim.get("review_sla_minutes", 60)
    cap = capacity_per_hour(world_data, gates)
    plans = {}
    for seed in sorted({t["seed"] for t in trials}):
        mine = [t for t in trials if t["seed"] == seed]
        plan = plans[seed] = recheck_plan(mine, world_data, gates)
        for t in mine:
            t["review_kind"], t["review_units"], t["queue_wait_min"], t["queue_stuck"] = None, 0.0, None, False
            if t["status"] == "escalated":
                t["review_kind"], t["review_units"] = "escalated", 1.0
            elif t["status"] in ("refunded", "denied") and _pct("recheck|" + t["ticket_id"]) < plan["pct"]:
                t["review_kind"], t["review_units"] = "recheck", plan["unit"]
        free = 0.0
        for t in sorted((t for t in mine if t["review_kind"]), key=lambda t: (t["arrive_min"], t["ticket_id"])):
            if cap <= 0:
                t["queue_wait_min"], t["queue_stuck"] = float(shift), True
                continue
            start = max(float(t["arrive_min"]), free)
            free = start + t["review_units"] * 60.0 / cap
            t["queue_wait_min"] = round(start - t["arrive_min"], 1)
            t["queue_stuck"] = t["queue_wait_min"] > sla or start > shift
    return plans


def summarize_ops(trials: list[dict], world_data: dict, gates: dict, out_of_scope: int = 0) -> dict:
    """Business / operations numbers of one run. Money figures are per simulated day (average over seeds)."""
    f, lim = world_data.get("ops_facts", {}), world_data.get("ops_limits", {})
    plans = attach_queue(trials, world_data, gates)
    seeds = sorted({t["seed"] for t in trials})
    k = max(1, len(seeds))
    n_day = len(trials) / k
    manual, review_cost = f.get("manual_cost_per_ticket_vnd", 0), f.get("review_cost_per_ticket_vnd", 0)
    nrev = reviewers(world_data, gates)
    standby = nrev * f.get("reviewer_standby_fee_vnd", 0) if trials else 0
    agent = sum(t["cost_vnd"] for t in trials) / k
    review = sum(t["review_units"] for t in trials) * review_cost / k
    harm = sum(t["wrongful_refund_vnd"] for t in trials) / k
    total = agent + review + standby
    saving = n_day * manual - total - harm
    queued = [t for t in trials if t["review_kind"]]
    waits = [t["queue_wait_min"] for t in queued]
    stuck_by_seed = [sum(t["queue_stuck"] for t in trials if t["seed"] == s) for s in seeds]
    day_auto: dict = {}
    for t in trials:
        key = (t["seed"], t["scenario"])
        day_auto[key] = day_auto.get(key, 0) + sum(r["amount_vnd"] for r in t["ledger"] if not r.get("approval_id"))
    segs = {}
    for wh in sorted({t["warehouse"] or "?" for t in trials}):
        sub = [t for t in trials if (t["warehouse"] or "?") == wh]
        c = (sum(t["cost_vnd"] for t in sub) + sum(t["review_units"] for t in sub) * review_cost) / len(sub)
        segs[wh] = {"tickets_per_day": round(len(sub) / k, 1), "cost_per_ticket_vnd": int(round(c)),
                    "review_rate": round(sum(bool(t["review_kind"]) for t in sub) / len(sub), 4),
                    "worse_than_manual": c > manual}
    n_all = n_day + out_of_scope
    b, o = gates["business"], gates["operations"]
    out = {
        "tickets_in_scope_per_day": round(n_day, 1), "out_of_scope_per_day": out_of_scope,
        "coverage": round(n_day / n_all, 4) if n_all else 0.0,
        "review_rate": round(len(queued) / max(1, len(trials)), 4),
        "queue": {"reviewers_on_shift": nrev, "capacity_per_hour": capacity_per_hour(world_data, gates),
                  "sla_minutes": lim.get("review_sla_minutes", 60), "queued_per_day": round(len(queued) / k, 1),
                  "wait_avg_min": round(sum(waits) / len(waits), 1) if waits else 0.0,
                  "wait_max_min": max(waits, default=0.0), "stuck": max(stuck_by_seed, default=0),
                  "recheck_pct": max((p["pct"] for p in plans.values()), default=0),
                  "trust": next((p["trust"] for p in plans.values() if p["trust"] == "chưa đạt"),
                                next(iter(plans.values()))["trust"] if plans else "không áp dụng"),
                  "trust_why": sorted({w for p in plans.values() for w in p["why"]})},
        "cost": {"cost_per_ticket_vnd": int(round(total / n_day)) if n_day else 0, "manual_cost_per_ticket_vnd": manual,
                 "agent_cost_per_day_vnd": int(round(agent)), "review_cost_per_day_vnd": int(round(review)),
                 "standby_cost_per_day_vnd": int(standby), "wrongful_refund_per_day_vnd": int(round(harm)),
                 "net_saving_per_day_vnd": int(round(saving)), "roi": round(saving / total, 2) if total else 0.0,
                 "llm_cost_max_per_ticket_vnd": max((t["cost_vnd"] for t in trials), default=0),
                 "llm_cost_ceiling_vnd": lim.get("max_llm_cost_per_ticket_vnd")},
        "refund": {"auto_refund_day_max_vnd": max(day_auto.values(), default=0),
                   "finance_daily_budget_vnd": lim.get("daily_auto_refund_budget_vnd"),
                   "team_daily_cap_vnd": b["daily_refund_cap_vnd"],
                   "wrongful_refund_worst_day_vnd": max((sum(t["wrongful_refund_vnd"] for t in trials if t["seed"] == s)
                                                         for s in seeds), default=0)},
        "segments": segs,
        "segments_worse_than_manual": sum(v["worse_than_manual"] for k_, v in segs.items() if k_ != "?"),
    }
    q, c, r = out["queue"], out["cost"], out["refund"]
    v = []                                                       # ceilings broken (facts agreed with Ops/Finance + the team's own gates)
    if q["stuck"]:
        v.append(f"hàng chờ: {q['stuck']} ca bị ùn (chờ quá {q['sla_minutes']} phút hoặc hết ca chưa tới lượt)")
    if o["max_queue_wait_minutes"] is not None and q["wait_max_min"] > o["max_queue_wait_minutes"]:
        v.append(f"chờ lâu nhất {q['wait_max_min']} phút > mức bàn đặt {o['max_queue_wait_minutes']} phút")
    if n_day and c["cost_per_ticket_vnd"] > manual:
        v.append(f"chi phí mỗi ticket {c['cost_per_ticket_vnd']}đ > làm tay {manual}đ")
    if c["llm_cost_ceiling_vnd"] is not None and c["llm_cost_max_per_ticket_vnd"] > c["llm_cost_ceiling_vnd"]:
        v.append(f"có ticket tốn {c['llm_cost_max_per_ticket_vnd']}đ tiền LLM > trần {c['llm_cost_ceiling_vnd']}đ")
    if b["roi_min"] is not None and c["roi"] < b["roi_min"]:
        v.append(f"ROI {c['roi']} < ngưỡng bàn đặt {b['roi_min']}")
    for wh, sg in segs.items():
        if wh != "?" and sg["worse_than_manual"]:
            v.append(f"kho {wh}: mỗi ticket tốn {sg['cost_per_ticket_vnd']}đ > làm tay {manual}đ")
    if r["finance_daily_budget_vnd"] is not None and r["auto_refund_day_max_vnd"] > r["finance_daily_budget_vnd"]:
        v.append(f"tổng hoàn tự động một ngày {r['auto_refund_day_max_vnd']}đ > ngân sách {r['finance_daily_budget_vnd']}đ")
    if r["finance_daily_budget_vnd"] is not None and r["wrongful_refund_worst_day_vnd"] > r["finance_daily_budget_vnd"]:
        v.append(f"tiền hoàn sai một ngày {r['wrongful_refund_worst_day_vnd']}đ > ngân sách hoàn cả ngày")
    out["violations"] = v
    return out


FLAT = {"cost_per_ticket_vnd": ("cost", "cost_per_ticket_vnd"), "roi": ("cost", "roi"),
        "queue_wait_max_min": ("queue", "wait_max_min"), "queue_stuck": ("queue", "stuck"),
        "auto_refund_day_max_vnd": ("refund", "auto_refund_day_max_vnd")}


def flat(ops: dict) -> dict:
    """Top-level copies of the main numbers, so lab10.gate can compare them with the signed criteria."""
    return {"review_rate": ops["review_rate"], "coverage": ops["coverage"], **{k: ops[a][b] for k, (a, b) in FLAT.items()}}
