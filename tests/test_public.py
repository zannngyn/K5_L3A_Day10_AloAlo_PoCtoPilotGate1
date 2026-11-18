"""Test công khai (unittest, stdlib). Chạy: python3 -m unittest discover -s tests -v

Đây là "test cũ": bản SAU của đội không được làm hỏng chúng.
"""
import importlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lab10 import SEEDS, helpers as H, ops  # noqa: E402
from lab10.eval import run_suite, summarize  # noqa: E402
from lab10.tools import Verdict  # noqa: E402
from lab10.world import load_suite  # noqa: E402


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world, cls.tickets = load_suite("base")

    def run_with(self, modname, switches=None):
        return run_suite(self.world, self.tickets, importlib.import_module(modname), switches or {})

    def test_baseline_known_numbers(self):
        """Bản TRƯỚC: 22 ticket x 5 seed = 110 lần chạy, hỏng đúng một ca T-002@55 (agent tin số ngày khách ghi)."""
        s = summarize(self.run_with("lab10._noop_guards"))
        self.assertEqual(s["trials"], len(self.tickets) * len(SEEDS))
        self.assertEqual(s["failed"], ["T-002@55"])

    def test_team_guards_do_not_break_base(self):
        """Bản SAU: ca nào trước đạt thì sau vẫn đạt."""
        before = set(summarize(self.run_with("lab10._noop_guards"))["failed"])
        after = set(summarize(self.run_with("lab10.guards"))["failed"])
        self.assertFalse(sorted(after - before))

    def test_deterministic(self):
        a = [(t["ticket_id"], t["seed"], t["status"], t["paid_vnd"]) for t in self.run_with("lab10._noop_guards")]
        b = [(t["ticket_id"], t["seed"], t["status"], t["paid_vnd"]) for t in self.run_with("lab10._noop_guards")]
        self.assertEqual(a, b)

    def test_kill_switch_stops_all_refunds(self):
        trials = self.run_with("lab10._noop_guards", {"issue_refund": "off"})
        self.assertEqual(sum(t["paid_vnd"] for t in trials), 0)

    def test_helpers(self):
        o = next(o for o in self.world["orders"] if o["order_id"] == "O-1003")
        pol = H.effective_policy(self.world["policies"], self.world["as_of"])
        self.assertEqual(pol["policy_id"], "REFUND-v3")
        self.assertEqual(H.db_delay_days(o["parcels"][0], self.world["as_of"]), 8)
        self.assertEqual(H.entitlement_vnd(pol, o, 8, "CARRIER"), 30000 + 60000)
        self.assertEqual(H.effective_policy(self.world["policies"], "2026-12-01")["policy_id"], "REFUND-v4")

    def test_verdict_api(self):
        self.assertEqual(Verdict.modify("x", amount_vnd=1).changes, {"amount_vnd": 1})
        self.assertEqual(Verdict.escalate("x").action, "escalate")

    def test_denied_refund_is_not_announced_as_paid(self):
        """Cổng chặn lệnh hoàn tiền thì khách KHÔNG được báo là đã hoàn: sổ cái trống, tin nhắn nói yêu cầu bị từ chối."""
        class DenyRefund:
            @staticmethod
            def pre_guard(ctx):
                return Verdict.allow()

            @staticmethod
            def write_gate(ctx, action):
                return Verdict.deny("kiểm thử: chặn mọi lệnh hoàn") if action["tool"] == "issue_refund" else Verdict.allow()

        tickets = [t for t in self.tickets if t["ticket_id"] in ("T-001", "T-003")]      # hai ticket lẽ ra được hoàn
        self.assertTrue(all(t["label"]["refund_vnd"] > 0 for t in tickets))
        trials = run_suite(self.world, tickets, DenyRefund, {})
        self.assertEqual(len(trials), len(tickets) * len(SEEDS))
        for t in trials:
            self.assertEqual(t["ledger"], [])                                    # (a) không có khoản hoàn nào trong sổ cái
            self.assertEqual(t["paid_vnd"], 0)
            self.assertEqual(t["fault_rows"], [])                                # không hoàn thì cũng không ghi lỗi hãng
            replies = [m for m in t["outbound"] if m["to"].startswith("customer:")]
            self.assertEqual(len(replies), 1)
            for m in t["outbound"]:                                              # (b) không tin nào nói đã hoàn tiền
                blob = str(m["payload"]).lower()
                self.assertNotIn("đã hoàn", blob)
                self.assertEqual(m["payload"].get("amount_vnd", 0), 0)
            self.assertIn("từ chối", replies[0]["payload"]["text"])              # (c) nói thật: yêu cầu đã bị từ chối
            self.assertIn("chưa hoàn", replies[0]["payload"]["text"])
            self.assertEqual(t["status"], "denied")


class TestOperatingGates(unittest.TestCase):
    """Cổng kinh doanh / vận hành trong config và mô phỏng hàng chờ người duyệt (tất định)."""

    @classmethod
    def setUpClass(cls):
        cls.world, cls.tickets = load_suite("base")

    def gates(self, **groups):
        return ops.merged(groups)

    def run_with(self, gates):
        return run_suite(self.world, self.tickets, importlib.import_module("lab10._noop_guards"), {}, gates=gates)

    def test_default_gates_change_nothing(self):
        a = summarize(self.run_with(ops.merged({})))
        b = summarize(run_suite(self.world, self.tickets, importlib.import_module("lab10._noop_guards"), {}))
        self.assertEqual(a["failed"], b["failed"])

    def test_pilot_scope_by_warehouse(self):
        trials = self.run_with(self.gates(business={"pilot_scope": {"mode": "warehouse", "warehouses": ["HN"]}}))
        self.assertTrue(trials)
        self.assertEqual({t["warehouse"] for t in trials} - {None}, {"HN"})
        none = self.run_with(self.gates(business={"pilot_scope": {"mode": "percent", "percent": 0}}))
        self.assertEqual(none, [])

    def test_daily_refund_cap_sends_auto_refunds_to_a_human(self):
        trials = self.run_with(self.gates(business={"daily_refund_cap_vnd": 1000}))
        auto = [r for t in trials for r in t["ledger"] if not r.get("approval_id")]
        self.assertEqual(auto, [])                                  # mọi khoản hoàn tự động vượt trần 1.000đ đều bị giữ lại
        self.assertTrue(any(e.get("gate") == "daily_refund_cap_vnd" for t in trials for e in t["events"]))

    def test_cost_budget_stops_before_calling_the_llm(self):
        trials = self.run_with(self.gates(business={"cost_budget_per_ticket_vnd": 100}))
        self.assertTrue(all(t["status"] == "escalated" for t in trials))
        self.assertFalse(any(e["type"] == "llm_extract" for t in trials for e in t["events"]))

    def test_review_queue_backs_up_when_understaffed(self):
        def day(n_reviewers):
            trials = [{"seed": 11, "ticket_id": f"Q-{i:02d}", "status": "escalated", "arrive_min": 2 * i, "ledger": []}
                      for i in range(10)]                           # 10 ca cần người, cứ 2 phút tới một ca
            ops.attach_queue(trials, self.world, self.gates(operations={"reviewers_on_shift": n_reviewers}))
            return trials
        one, two = day(1), day(2)
        self.assertEqual([t["queue_wait_min"] for t in one], [8.0 * i for i in range(10)])   # 1 người: 10 phút/ca
        self.assertEqual(sum(t["queue_stuck"] for t in one), 2)     # hai ca cuối chờ 64 và 72 phút > hạn 60 phút
        self.assertEqual(sum(t["queue_stuck"] for t in two), 0)     # 2 người: không ca nào ùn
        self.assertEqual([t["queue_wait_min"] for t in day(1)], [t["queue_wait_min"] for t in one])   # chạy lại ra y hệt

    def test_ops_summary_has_business_numbers(self):
        gates = ops.merged({})
        o = ops.summarize_ops(self.run_with(gates), self.world, gates)
        self.assertEqual(o["queue"]["stuck"], 0)
        self.assertLess(o["cost"]["cost_per_ticket_vnd"], o["cost"]["manual_cost_per_ticket_vnd"])
        self.assertGreater(o["cost"]["roi"], 0)
        self.assertEqual(o["violations"], [])


if __name__ == "__main__":
    unittest.main()
