"""Chốt cổng vòng 1 (mốc "prepared"): chụp lại code cổng và config cổng TRƯỚC khi bàn biết sự cố.

    python3 -m lab10.checkpoint           # chốt MỘT lần, trước khi nộp quyết định v1 (phút ~105-115)
    python3 -m lab10.checkpoint verify    # kiểm bản chốt còn nguyên

Lệnh chép:  lab10/guards.py               -> lab10/guards_round1.py
            config/operating_gates.json   -> config/operating_gates.round1.json
và ghi dấu vân tay (hash) của hai bản chép vào config/round1.lock.
Sau khi chốt, bàn tiếp tục sửa lab10/guards.py và config/operating_gates.json ở vòng 2. KHÔNG sửa hai file .round1.
Mốc "prepared" của lab10.eval / lab10.grade chạy đúng hai bản chép này.
LOCKED: do not edit (hash-checked by lab10.grade).
"""
from __future__ import annotations

import hashlib
import importlib
import json
import shutil
import sys
from datetime import datetime

from . import ops
from .world import ROOT

GUARDS, GUARDS_R1 = ROOT / "lab10" / "guards.py", ROOT / "lab10" / "guards_round1.py"
LOCK = ROOT / "config" / "round1.lock"


def _sha(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def status() -> dict:
    """ok only if the lock exists and both snapshots still match it."""
    out = {"ok": False, "taken": LOCK.exists(), "hash": None, "problem": None}
    if not LOCK.exists():
        out["problem"] = "chưa chốt cổng vòng 1 (chưa chạy python3 -m lab10.checkpoint)"
        return out
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    out["hash"], out["taken_at"] = lock["sha256"], lock.get("taken_at")
    if not GUARDS_R1.exists() or not ops.ROUND1_GATES.exists():
        out["problem"] = "thiếu file bản chốt vòng 1 (guards_round1.py hoặc operating_gates.round1.json)"
    elif _sha(GUARDS_R1) != lock["guards_sha256"] or _sha(ops.ROUND1_GATES) != lock["gates_sha256"]:
        out["problem"] = "bản chốt vòng 1 ĐÃ BỊ SỬA sau khi chốt"
    else:
        out["ok"] = True
    return out


def main(argv=None):
    cmd = (argv if argv is not None else sys.argv[1:] or ["take"])
    cmd = cmd[0] if cmd else "take"
    if cmd == "verify":
        s = status()
        print(json.dumps(s, ensure_ascii=False, indent=1))
        sys.exit(0 if s["ok"] else 1)
    if LOCK.exists():
        sys.exit("Đã chốt cổng vòng 1 rồi. Mốc 'prepared' giữ nguyên tới hết buổi. "
                 "Ở vòng 2, hãy sửa lab10/guards.py và config/operating_gates.json.")
    if not ops.GATES_FILE.exists():
        sys.exit("Thiếu config/operating_gates.json.")
    try:
        cfg = json.loads(ops.GATES_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"Chưa chốt được: config/operating_gates.json không phải JSON hợp lệ (dòng {e.lineno}): {e.msg}")
    bad = ops.problems(cfg)
    if bad:
        sys.exit("Chưa chốt được: config/operating_gates.json có giá trị chưa dùng được:\n  - " + "\n  - ".join(bad))
    try:
        g = importlib.import_module("lab10.guards")
        assert callable(g.pre_guard) and callable(g.write_gate)
    except Exception as e:                                    # a broken guards.py must not become the checkpoint
        sys.exit(f"Chưa chốt được: lab10/guards.py đang lỗi ({type(e).__name__}: {e}). Sửa cho chạy được rồi chốt lại.")
    shutil.copyfile(GUARDS, GUARDS_R1)
    shutil.copyfile(ops.GATES_FILE, ops.ROUND1_GATES)
    gs, cs = _sha(GUARDS_R1), _sha(ops.ROUND1_GATES)
    h = hashlib.sha256((gs + cs).encode()).hexdigest()
    LOCK.write_text(json.dumps({"sha256": h, "guards_sha256": gs, "gates_sha256": cs,
                                "taken_at": datetime.now().isoformat(timespec="seconds")}, indent=1), encoding="utf-8")
    print(f"ĐÃ CHỐT cổng vòng 1 (mốc prepared). 8 ký tự đầu: {h[:8]}")
    print("  Đã chép: lab10/guards_round1.py · config/operating_gates.round1.json  (không sửa hai file này)")
    print("  Vòng 2 sửa tiếp ở: lab10/guards.py · config/operating_gates.json")


if __name__ == "__main__":
    main()
