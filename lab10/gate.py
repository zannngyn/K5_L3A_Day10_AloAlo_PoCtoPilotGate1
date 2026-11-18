"""So một report với Bản tiêu chí chấp nhận đã ký (và với baseline nếu có). Gate KHÔNG quyết định hộ đội.

    python3 -m lab10.gate --run runs/<mã lần chạy>/report.json [--baseline runs/<mã>/report.json]

LOCKED: do not edit.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import criteria


def check(report: dict, crit: dict) -> list[dict]:
    rows = []
    for group in ("required", "nice_to_have", "business_ops"):
        for key, thr in crit.get(group, {}).items():
            if thr is None:
                continue
            if key.startswith("_"):
                continue
            metric, kind = key.rsplit("_", 1)
            val = report.get(metric)
            ok = val is not None and (val >= thr if kind == "min" else val <= thr)
            rows.append({"group": group, "metric": metric, "rule": f"{'≥' if kind == 'min' else '≤'} {thr}",
                         "value": val, "ok": ok})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--baseline")
    a = ap.parse_args(argv)
    st = criteria.status()
    rep = json.loads(Path(a.run).read_text(encoding="utf-8"))
    print(f"Lần chạy {rep['run_id']} · tiêu chí hash {str(st['hash'])[:8]} · "
          f"{'đã ký, còn nguyên' if st['ok'] else 'CẢNH BÁO: ' + str(st['problem'])}")
    rows = check(rep, criteria.load())
    for r in rows:
        print(f"  [{'ĐẠT ' if r['ok'] else 'CHƯA'}] {r['group']:12} {r['metric']:26} {r['rule']:10} thực tế {r['value']}")
    regress = []
    if a.baseline:
        base = json.loads(Path(a.baseline).read_text(encoding="utf-8"))
        regress = sorted(set(rep["failed"]) - set(base["failed"])) if base["suite"] == rep["suite"] else []
        print(f"  So với {base['run_id']}: pass_rate {base['pass_rate']} → {rep['pass_rate']}; "
              f"ca mới hỏng: {regress or 'không'}")
    req_ok = all(r["ok"] for r in rows if r["group"] == "required")
    biz_ok = all(r["ok"] for r in rows if r["group"] == "business_ops")
    for v in rep.get("ops", {}).get("violations", []):
        print(f"  [VƯỢT TRẦN] {v}")
    print("  Chỉ số bắt buộc:", "đều đạt" if req_ok else "CHƯA đạt đủ",
          "· Ngưỡng kinh doanh/vận hành đã ký:", "đều đạt" if biz_ok else "CHƯA đạt đủ",
          "· Quyết định là việc của đội, ghi vào bản ghi Gate 1.")
    sys.exit(0 if st["ok"] and req_ok and not regress else 1)


if __name__ == "__main__":
    main()
