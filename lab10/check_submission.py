"""Tự kiểm tra BÀI NỘP đã đủ thành phần chưa. Lệnh này không chấm điểm.

    python3 -m lab10.check_submission --collect   # gom file máy sinh vào submission/, rồi kiểm
    python3 -m lab10.check_submission             # chỉ kiểm

Bài nộp nằm trong thư mục submission/ (xem submission/README.md):
  submission.json    bàn tự điền: tên bàn, thành viên, số thẻ, quyết định v1 và v2, ba dòng bắt buộc
  Nộp: đẩy lên repo của bàn đặt tên đúng dạng K5_Day10_3A_<TenNhom> hoặc K5_Day10_3B_<TenNhom>
  (ví dụ K5_Day10_3A_TenNhom; TenNhom không dấu, không cách) rồi gửi link repo cho team chấm.
  code/              cổng vòng 1 (bản đã chốt) và cổng vòng 2, chỉ số theo dõi
  config/            cổng kinh doanh + vận hành + pháp lý (vòng 1 và hiện tại), tiêu chí đã ký kèm hash
  runs/              báo cáo tự kiểm tra, ba mốc base / prepared / after (kèm mã lần chạy), journal.jsonl (mọi lần chạy)
  docs/              ba phiếu: form-a-criteria.md, form-b-evaluation-gates.md, form-c-incident.md
  manifest.json      do lệnh --collect ghi: hash từng file, mã lần chạy, thời điểm gom

Exit 0 = đủ thành phần · 1 = còn thiếu (lệnh in rõ thiếu gì và làm gì tiếp). LOCKED: do not edit.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from . import checkpoint, criteria, ops
from .eval import RUNS, code_hash
from .world import ROOT

SUB = ROOT / "submission"
FORM = SUB / "submission.json"
DECISIONS = ("Tiếp tục", "Thu hẹp", "Cải tiến thêm", "Dừng")
CARDS = tuple(f"S{i}" for i in range(1, 9))
CODE = {"code/guards_round1.py": "lab10/guards_round1.py", "code/guards.py": "lab10/guards.py",
        "code/monitors.py": "lab10/monitors.py"}
CONFIG = {f"config/{n}": f"config/{n}" for n in ("operating_gates.round1.json", "operating_gates.json", "switches.json",
                                                   "acceptance_criteria.json", "acceptance_criteria.lock", "round1.lock")}
DOCS_REQUIRED = ("form-a-criteria.md", "form-b-evaluation-gates.md", "form-c-incident.md")
DOCS_OPTIONAL: tuple = ()
DRAWN_FORM = "form-c-incident.md"          # dòng `Thẻ đã bốc:` nằm ở đầu Phiếu C
SECTION_EXEMPT = {("form-c-incident.md", "C3"): {"S4"}}   # S4: phần riêng nằm ở C1 + Phiếu B mục B7.6 (bảng đầu mục C3)
THREE = ("environment_assumption", "reduce_or_prevent", "measure_in_pilot")
BLANK = {"team": "", "members": [], "incident": "", "decision_v1": "", "decision_v2": "",
         "three_lines": {k: "" for k in THREE}}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _form() -> dict:
    try:
        return json.loads(FORM.read_text(encoding="utf-8")) if FORM.exists() else {}
    except json.JSONDecodeError:
        return {"_broken": True}


def latest_grade(incident: str) -> Path | None:
    reps = sorted(RUNS.glob(f"R-{incident}-grade-*.json"), key=lambda p: p.stat().st_mtime) if RUNS.exists() else []
    return reps[-1] if reps else None


def form_sections(text: str) -> dict:
    """Hash từng mục `## A1 …` / `## B7 …` / `## C12 …` của một phiếu (để biết mục nào còn nguyên mẫu)."""
    out, code, buf = {}, None, []
    for line in text.splitlines() + ["## END"]:
        m = re.match(r"## ([A-C]\d+)\b", line)
        if line.startswith("## "):
            if code:
                out[code] = hashlib.sha256("\n".join(l.rstrip() for l in buf).strip().encode("utf-8")).hexdigest()
            code, buf = (m.group(1) if m else None), []
        buf.append(line)
    return out


def first_eval_time(journal: Path) -> str | None:
    """Thời điểm (ISO, giờ máy) của lần chạy sớm nhất trong journal, đọc từ mã lần chạy R-<bộ>-<mốc>-YYYYMMDD-HHMMSS-<hash>."""
    if not journal.exists():
        return None
    stamps = []
    for line in journal.read_text(encoding="utf-8").splitlines():
        try:
            rid = json.loads(line).get("run_id", "")
        except json.JSONDecodeError:
            continue
        m = re.search(r"-(\d{8})-(\d{6})-", rid)
        if m:
            d, t = m.groups()
            stamps.append(f"{d[:4]}-{d[4:6]}-{d[6:]}T{t[:2]}:{t[2:4]}:{t[4:]}")
    return min(stamps) if stamps else None


def collect() -> list[str]:
    """Copy machine-made parts into submission/. Never touches submission.json fields the team has filled."""
    did = []
    SUB.mkdir(exist_ok=True)
    if not FORM.exists():
        FORM.write_text(json.dumps(BLANK, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        did.append("tạo submission/submission.json (mẫu trống, bàn cần điền)")
    for dst, src in {**CODE, **CONFIG, **{f"docs/{n}": f"templates/{n}" for n in DOCS_REQUIRED + DOCS_OPTIONAL}}.items():
        if (ROOT / src).exists():
            (SUB / dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / src, SUB / dst)
            did.append(f"chép {src} -> submission/{dst}")
    inc = str(_form().get("incident", "")).strip().upper()
    rep = latest_grade(inc) if inc in CARDS else None
    runs = {}
    if rep:
        (SUB / "runs").mkdir(exist_ok=True)
        shutil.copyfile(rep, SUB / "runs" / "grade-report.json")
        if rep.with_suffix(".md").exists():
            shutil.copyfile(rep.with_suffix(".md"), SUB / "runs" / "grade-report.md")
        r = json.loads(rep.read_text(encoding="utf-8"))
        for mark, rid in r.get("run_ids", {}).items():
            name = "base" if mark == "before" else mark
            runs[name] = rid
            src = RUNS / rid / "report.json"
            if src.exists():
                (SUB / "runs" / rid).mkdir(exist_ok=True)
                shutil.copyfile(src, SUB / "runs" / rid / "report.json")
        did.append(f"chép báo cáo tự kiểm tra {rep.name} và {len(runs)} mốc: {runs}")
    if (RUNS / "journal.jsonl").exists():            # nhật ký MỌI lần chạy: bằng chứng đã commit cho "ký trước khi đo"
        (SUB / "runs").mkdir(exist_ok=True)
        shutil.copyfile(RUNS / "journal.jsonl", SUB / "runs" / "journal.jsonl")
        did.append("chép runs/journal.jsonl -> submission/runs/journal.jsonl")
    files = {p.relative_to(SUB).as_posix(): _sha(p) for p in sorted(SUB.rglob("*"))
             if p.is_file() and p.name not in ("manifest.json", "README.md")}
    (SUB / "manifest.json").write_text(json.dumps({
        "collected_at": datetime.now().isoformat(timespec="seconds"), "incident": inc or None, "run_ids": runs,
        "grade_run_id": json.loads(rep.read_text(encoding="utf-8"))["run_id"] if rep else None,
        "criteria_hash": criteria.file_hash() if criteria.CRITERIA.exists() else None,
        "round1_hash": checkpoint.status().get("hash"), "code_hash": code_hash(), "files": files},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    did.append(f"ghi submission/manifest.json ({len(files)} file)")
    return did


def check() -> list[tuple[bool, str, str]]:
    """Returns rows (ok, what, what-to-do-if-missing)."""
    rows: list[tuple[bool, str, str]] = []
    add = lambda ok, what, fix="": rows.append((bool(ok), what, fix))   # noqa: E731
    f = _form()
    add(FORM.exists() and not f.get("_broken"), "submission/submission.json đọc được",
        "chạy `python3 -m lab10.check_submission --collect` để tạo mẫu; nếu file hỏng, sửa cho đúng JSON")
    crit = criteria.load() if criteria.CRITERIA.exists() else {}
    team = str(f.get("team", "")).strip()
    add(team and team == str(crit.get("team", "")).strip(), f"tên bàn (`team`): {team or '(trống)'}",
        f"điền `team` giống hệt trong Bản tiêu chí đã ký ({crit.get('team') or 'chưa điền'})")
    mem = f.get("members") or []
    add(isinstance(mem, list) and len([m for m in mem if str(m).strip()]) >= 1, f"thành viên (`members`): {len(mem)} người",
        "điền danh sách họ tên thành viên, ví dụ [\"Nguyễn A\", \"Trần B\"]")
    inc = str(f.get("incident", "")).strip().upper()
    add(inc in CARDS, f"số thẻ đã bốc (`incident`): {inc or '(trống)'}", "điền số thẻ bàn bốc được, ví dụ \"S3\"")
    for k, name in (("decision_v1", "quyết định v1"), ("decision_v2", "quyết định v2")):
        add(f.get(k) in DECISIONS, f"{name} (`{k}`): {f.get(k) or '(trống)'}", "điền một trong: " + " / ".join(DECISIONS))
    three = f.get("three_lines") or {}
    for k, name in zip(THREE, ("giả định về môi trường", "giảm hay ngăn, vì sao", "cần đo lại gì trong pilot thật")):
        add(len(str(three.get(k, "")).strip()) >= 15, f"ba dòng bắt buộc · {name} (`three_lines.{k}`)",
            "viết một câu đầy đủ (từ 15 ký tự)")
    # ---- code + config
    for dst in list(CODE) + list(CONFIG):
        add((SUB / dst).exists(), f"có file submission/{dst}",
            "chạy `python3 -m lab10.check_submission --collect`" + (
                "; nếu vẫn thiếu, bàn chưa chốt cổng vòng 1: `python3 -m lab10.checkpoint`" if "round1" in dst else
                "; nếu vẫn thiếu, bàn chưa ký tiêu chí: `python3 -m lab10.criteria sign`" if dst.endswith(".lock") else ""))
    lock, cfile = SUB / "config" / "acceptance_criteria.lock", SUB / "config" / "acceptance_criteria.json"
    if lock.exists() and cfile.exists():
        h = json.loads(lock.read_text(encoding="utf-8"))["sha256"]
        add(_sha(cfile) == h, f"tiêu chí trong bài nộp khớp hash đã ký ({h[:8]})",
            "file tiêu chí đã bị đổi sau khi ký: trả về đúng bản lúc ký rồi --collect lại")
    ok_g, what_g, fix_g = criteria.check_sign_git_history()
    if what_g:                                        # bỏ qua im lặng khi thư mục lab không phải repo git
        add(ok_g, what_g, fix_g)
    r1, g1, c1 = SUB / "config" / "round1.lock", SUB / "code" / "guards_round1.py", SUB / "config" / "operating_gates.round1.json"
    if r1.exists() and g1.exists() and c1.exists():
        lk = json.loads(r1.read_text(encoding="utf-8"))
        add(_sha(g1) == lk["guards_sha256"] and _sha(c1) == lk["gates_sha256"], f"cổng vòng 1 trong bài nộp khớp bản đã chốt ({lk['sha256'][:8]})",
            "bản chốt vòng 1 đã bị sửa: không sửa guards_round1.py và operating_gates.round1.json")
    g2 = SUB / "config" / "operating_gates.json"
    if g2.exists():
        try:
            cfg = json.loads(g2.read_text(encoding="utf-8"))
            bad = ops.problems(cfg)
            add(not bad, "config cổng (operating_gates.json) dùng được", "; ".join(bad))
            o = ops.merged(cfg)["operations"]
            add(all(str(o[k]).strip() for k in ("pic", "approver_id", "alert_channel")) and o["stop_conditions"],
                "cổng con người đã điền: PIC, người duyệt, kênh báo tin, điều kiện dừng",
                "điền operations.pic, approver_id, alert_channel và ít nhất một câu trong stop_conditions rồi --collect lại")
        except json.JSONDecodeError:
            add(False, "config cổng (operating_gates.json) dùng được", "file không phải JSON hợp lệ")
    # ---- runs
    rep = SUB / "runs" / "grade-report.json"
    add(rep.exists(), "có báo cáo tự kiểm tra (runs/grade-report.json)",
        "điền `incident` trong submission.json, chạy `python3 -m lab10.grade --incident Sx`, rồi --collect lại")
    if rep.exists():
        r = json.loads(rep.read_text(encoding="utf-8"))
        add(r.get("incident") == inc, f"báo cáo là của đúng thẻ đã bốc ({r.get('incident')})", "chạy grade với đúng số thẻ rồi --collect lại")
        ids = r.get("run_ids", {})
        for mark, name in (("before", "base"), ("prepared", "prepared"), ("after", "after")):
            rid = ids.get(mark)
            add(rid and (SUB / "runs" / rid / "report.json").exists(), f"mốc {name}: mã lần chạy {rid or '(chưa có)'}",
                "chưa có mốc prepared: bàn chưa chốt cổng vòng 1 trước khi chạy grade" if mark == "prepared" and not rid
                else "chạy lại grade rồi --collect lại")
        add(r.get("code_hash") == code_hash(), "báo cáo được chạy trên đúng code và config hiện tại",
            "bàn đã sửa code hoặc config sau lần grade cuối: chạy lại `python3 -m lab10.grade --incident Sx` rồi --collect lại")
        add(r.get("criteria", {}).get("ok") is True, "báo cáo ghi nhận tiêu chí đã ký, còn nguyên", "xem mục criteria trong báo cáo")
    # ---- docs
    try:
        pristine = json.loads((ROOT / "lab10" / "TEMPLATE_HASHES.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        pristine = {}
    for n in DOCS_REQUIRED:
        p = SUB / "docs" / n
        filled = p.exists() and _sha(p) != pristine.get(n)
        add(filled, f"phiếu docs/{n} đã điền", f"điền templates/{n} rồi --collect lại" if p.exists() else
            f"thiếu file: điền templates/{n} rồi chạy --collect")
        blank = (pristine.get("_sections") or {}).get(n) or {}
        if filled and blank:
            now = form_sections(p.read_text(encoding="utf-8"))
            untouched = [c for c, h in blank.items() if now.get(c) == h and inc not in SECTION_EXEMPT.get((n, c), ())]
            add(not untouched, f"phiếu docs/{n}: mọi mục đều đã điền" if not untouched else
                f"phiếu docs/{n}: mục còn nguyên mẫu: {', '.join(untouched)}",
                f"điền các mục {', '.join(untouched)} trong templates/{n} rồi --collect lại")
    gd = SUB / "docs" / DRAWN_FORM
    if gd.exists():
        m = re.search(r"Thẻ đã bốc:\**\s*`?(S[1-8])\b", gd.read_text(encoding="utf-8"))
        add(bool(m) and m.group(1) == inc, f"dòng 'Thẻ đã bốc' trong {DRAWN_FORM}: {m.group(1) if m else '(trống)'}",
            f"ghi đúng số thẻ vào dòng `Thẻ đã bốc:` ở đầu templates/{DRAWN_FORM} rồi --collect lại")
    for n in DOCS_OPTIONAL:
        p = SUB / "docs" / n
        if not (p.exists() and _sha(p) != pristine.get(n)):
            rows.append((True, f"(không bắt buộc) phiếu docs/{n} chưa điền", ""))
    first = first_eval_time(SUB / "runs" / "journal.jsonl")
    signed_at = None
    if lock.exists():
        signed_at = json.loads(lock.read_text(encoding="utf-8")).get("signed_at")
    commit_at = criteria.sign_commit_time()
    if first:
        late = [n for n, t in (("lúc ký", signed_at), ("commit 'Sign acceptance criteria'", commit_at)) if t and first < t]
        rows.append((True, f"lần đánh giá đầu tiên (submission/runs/journal.jsonl): {first}; ký: {signed_at or '?'}; commit ký: {commit_at or '?'}"
                     + (f" · CẢNH BÁO: chạy đánh giá TRƯỚC {', '.join(late)}; team chấm sẽ xem xét" if late else ""), ""))
    add((SUB / "manifest.json").exists(), "có submission/manifest.json", "chạy --collect")
    if (SUB / "manifest.json").exists():
        man = json.loads((SUB / "manifest.json").read_text(encoding="utf-8"))["files"]
        stale = sorted(k for k, h in man.items() if not (SUB / k).exists() or _sha(SUB / k) != h)
        add(not stale, "manifest khớp các file trong submission/", f"file đổi sau khi gom: {stale[:5]}. Chạy --collect lại")
    return rows


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if "--collect" in args:
        for line in collect():
            print("  +", line)
        print()
    rows = check()
    missing = [r for r in rows if not r[0]]
    print("KIỂM BÀI NỘP (submission/) · đây là kiểm ĐỦ THÀNH PHẦN, không phải chấm điểm\n")
    for ok, what, fix in rows:
        print(f"  [{'ĐỦ  ' if ok else 'THIẾU'}] {what}" + (f"\n          -> {fix}" if not ok and fix else ""))
    print()
    if missing:
        print(f"CHƯA ĐỦ: còn {len(missing)} mục. Làm theo dòng '->' rồi chạy lại lệnh này.")
        sys.exit(1)
    print("ĐỦ THÀNH PHẦN. Đẩy lên repo của bàn (tên đúng dạng K5_Day10_3A_<TenNhom> hoặc K5_Day10_3B_<TenNhom>, ví dụ K5_Day10_3A_TenNhom; TenNhom không dấu, không cách) rồi gửi link repo cho team chấm theo cách Lab Coach hướng dẫn.")


if __name__ == "__main__":
    main()
