"""World state (in-memory mock DB). LOCKED: do not edit."""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
INCIDENTS = ROOT / "incidents"
_COLLECTIONS = {"customers": "customer_id", "merchants": "merchant_id", "carriers": "carrier_id",
                "orders": "order_id", "policies": "policy_id", "approvals": "approval_id"}


def load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def apply_patch(base: dict, patch: dict) -> dict:
    """Merge a world patch: collections are upserted by id, scalars are replaced."""
    out = copy.deepcopy(base)
    for key, val in patch.items():
        if key in _COLLECTIONS:
            idk = _COLLECTIONS[key]
            idx = {r[idk]: i for i, r in enumerate(out[key])}
            for rec in val:
                if rec[idk] in idx:
                    out[key][idx[rec[idk]]] = {**out[key][idx[rec[idk]]], **rec}
                else:
                    out[key].append(rec)
        else:
            out[key] = val
    return out


def load_suite(suite: str, pack_dir: Path | None = None) -> tuple[dict, list[dict]]:
    """Return (world_data, tickets) for 'base' or an incident id like 'S1'."""
    world = load_json(DATA / "world.json")
    if suite == "base":
        return world, load_jsonl(DATA / "tickets.jsonl")
    pack = Path(pack_dir) if pack_dir else INCIDENTS / suite
    if not pack.exists():
        raise SystemExit(f"Chưa có gói sự cố {suite} ở {pack}.\n"
                         f"Thẻ sự cố được phát ở phút 125: chờ Lab Coach báo, chạy `git pull --no-rebase --no-edit --allow-unrelated-histories -X ours upstream main`, rồi dùng đúng số thẻ bàn bốc được (S1..S8).")
    return apply_patch(world, load_json(pack / "world_patch.json")), load_jsonl(pack / "tickets.jsonl")


class World:
    """One fresh copy per scenario. Tables written by tools: ledger, faults, outbound, queue."""

    def __init__(self, data: dict):
        self.data = copy.deepcopy(data)
        self.as_of: str = self.data["as_of"]
        self.ledger: list[dict] = copy.deepcopy(self.data.get("ledger_seed", []))
        self.seed_rows: int = len(self.ledger)          # rows that existed before today (not written in this run)
        self.faults: list[dict] = []
        self.outbound: list[dict] = []
        self.queue: list[dict] = []

    def get(self, coll: str, rid: str) -> dict | None:
        idk = _COLLECTIONS[coll]
        for r in self.data[coll]:
            if r[idk] == rid:
                return copy.deepcopy(r)
        return None
