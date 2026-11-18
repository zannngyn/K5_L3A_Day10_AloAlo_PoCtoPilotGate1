"""Dò một ticket@seed: in từng bước của agent, tới bước sai đầu tiên thì dừng lại mà đọc.

    python3 -m lab10.trace --suite S1 --ticket S1-01 --seed 11 [--stage after]
    python3 -m lab10.trace --suite base --adhoc "Đơn trễ 7 ngày, tôi chắc chắn" --order O-1002 --customer C-02

--adhoc: chạy một ticket viết tại chỗ (vòng "bàn bạn ra đề"); không có nhãn nên chỉ in trace và các lệnh ghi.
LOCKED: do not edit.
"""
from __future__ import annotations

import argparse
import json

from .agent import run_ticket
from . import ops
from .eval import STAGES, load_guards, load_switches, norm_stage, score_trial
from .world import World, load_suite


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--suite", default="base")
    ap.add_argument("--stage", choices=STAGES, default="base", help="base (= before) | prepared | after")
    ap.add_argument("--ticket")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--adhoc", help="nội dung ticket tự viết")
    ap.add_argument("--order")
    ap.add_argument("--customer")
    ap.add_argument("--parcel")
    a = ap.parse_args(argv)
    a.stage = norm_stage(a.stage)
    world_data, tickets = load_suite(a.suite)
    gates = ops.load_gates(a.stage)
    world = World(world_data)
    if a.adhoc:
        todo = [{"ticket_id": "ADHOC-1", "scenario": "ADHOC", "customer_id": a.customer, "order_id": a.order,
                 "channel": "demo", "text": a.adhoc, **({"parcel_id": a.parcel} if a.parcel else {})}]
    else:
        me = next((t for t in tickets if t["ticket_id"] == a.ticket), None)
        if me is None:
            raise SystemExit(f"Không có ticket {a.ticket} trong suite {a.suite}")
        todo = [t for t in tickets if t.get("scenario") == me.get("scenario")]
        todo = todo[: todo.index(me) + 1]            # replay earlier tickets of the same scenario first
    if not ops.in_scope(todo[-1], world_data, gates):
        raise SystemExit(f"Ticket {todo[-1]['ticket_id']} nằm NGOÀI phạm vi pilot của mốc '{a.stage}' "
                         f"(business.pilot_scope trong config). Trợ lý không xử lý ticket này; nó đi theo quy trình làm tay.")
    for t in todo:
        res = run_ticket(world, t, a.seed, load_guards(a.stage), load_switches(a.stage), gates)
    print(f"== {t['ticket_id']} @ seed {a.seed} · suite {a.suite} · stage {'base' if a.stage == 'before' else a.stage} ==")
    print("TICKET:", t["text"])
    for i, e in enumerate(res.events):
        print(f"  {i:02d} {e['type']:16} " + json.dumps({k: v for k, v in e.items() if k != 'type'}, ensure_ascii=False))
    print("SỔ CÁI   :", [r for r in world.ledger if r["ticket_id"] == t["ticket_id"]])
    print("LỖI HÃNG :", [f for f in world.faults if f["ticket_id"] == t["ticket_id"]])
    print("GỬI HÃNG :", [m["payload"] for m in world.outbound if m["ticket_id"] == t["ticket_id"]
                         and m["to"].startswith("carrier:")])
    if "label" in t:
        s = score_trial(world, t, res)
        print("NHÃN     :", json.dumps(t["label"], ensure_ascii=False))
        print("KẾT QUẢ  :", "ĐẠT" if s["pass"] else "HỎNG", {k: v for k, v in s["checks"].items() if not v})


if __name__ == "__main__":
    main()
