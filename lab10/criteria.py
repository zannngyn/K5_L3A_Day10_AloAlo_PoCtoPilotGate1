"""Bản tiêu chí chấp nhận: ký (niêm phong bằng hash) TRƯỚC khi đo, rồi giữ nguyên.

    python3 -m lab10.criteria sign      # ký một lần ở phút ~60, TRƯỚC khi chạy đánh giá lần nào.
                                        # Ngay sau đó bàn phải commit và push (lệnh in ra), rồi mới được eval.
    python3 -m lab10.criteria verify    # kiểm file có còn đúng bản đã ký

LOCKED: do not edit (hash-checked by lab10.grade).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from .world import ROOT

CRITERIA = ROOT / "config" / "acceptance_criteria.json"
LOCK = ROOT / "config" / "acceptance_criteria.lock"
REQUIRED = ("pass_rate_min", "pass_k_min", "wrongful_refund_vnd_max", "wrongful_carrier_faults_max", "pii_leaks_max")
SIGN_COMMIT = "Sign acceptance criteria"
SIGN_GIT = (
    "git add config/acceptance_criteria.json config/acceptance_criteria.lock "
    "&& git commit -m 'Sign acceptance criteria' && git push -u origin main"
)


def file_hash(path: Path = CRITERIA) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load() -> dict:
    return json.loads(CRITERIA.read_text(encoding="utf-8"))


def is_git_repo(root: Path = ROOT) -> bool:
    """True only when root itself is a git work tree (do not walk up to a parent repo)."""
    return (root / ".git").exists()


def _git(args: list[str], root: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def warn_if_lock_uncommitted(root: Path = ROOT) -> str | None:
    """Cảnh báo (không chặn) nếu file khoá chưa có trong lịch sử git. Bỏ qua nếu không phải repo git."""
    if not is_git_repo(root):
        return None
    r = _git(["log", "-1", "--oneline", "--", "config/acceptance_criteria.lock"], root)
    if r.returncode != 0 or not (r.stdout or "").strip():
        return ("CẢNH BÁO: chưa thấy commit cho config/acceptance_criteria.lock. "
                "Sau khi ký, trước khi chạy đánh giá, hãy chạy:\n  " + SIGN_GIT)
    return None


def check_sign_git_history(root: Path = ROOT) -> tuple[bool, str, str]:
    """Kiểm file tiêu chí không bị sửa sau commit ký. Bỏ qua (ok) nếu thư mục lab không phải repo git.

    Tìm commit theo đúng message 'Sign acceptance criteria' (không dùng --follow trên nhiều path:
    lệnh đó lỗi trên git). File json có thể đã được commit trước lúc ký; commit ký vẫn được tính.
    """
    if not is_git_repo(root):
        return True, "", ""
    r = _git(["log", "--format=%H %s", "--grep=^" + SIGN_COMMIT + "$"], root)
    if r.returncode != 0:
        return True, "", ""
    sign_lines = [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
    if not sign_lines:
        return (False,
                "chưa có commit 'Sign acceptance criteria' cho file tiêu chí/khoá",
                "sau khi ký, chạy: " + SIGN_GIT + "  (trước khi chạy đánh giá lần nào)")
    # git log is newest-first; the original sign commit is the last matching line
    sign_hash = sign_lines[-1].split()[0]
    later = _git(["log", f"{sign_hash}..HEAD", "--format=%H %s", "--",
                  "config/acceptance_criteria.json"], root)
    later_lines = [ln for ln in later.stdout.splitlines() if ln.strip()]
    if later_lines:
        return (False,
                f"file tiêu chí đã bị commit thêm sau commit ký ({len(later_lines)} lần)",
                "tiêu chí phải giữ nguyên sau khi ký; trả về đúng bản lúc ký rồi --collect lại")
    diff = _git(["diff", "--exit-code", sign_hash, "--", "config/acceptance_criteria.json"], root)
    if diff.returncode != 0:
        return (False,
                "file tiêu chí đã đổi so với commit 'Sign acceptance criteria'",
                "trả về đúng bản lúc ký (`git checkout -- config/acceptance_criteria.json`) rồi --collect lại")
    return True, "tiêu chí giữ nguyên từ commit 'Sign acceptance criteria'", ""


def sign_commit_time(root: Path = ROOT) -> str | None:
    """Thời điểm (giờ máy, ISO, không múi giờ) của commit 'Sign acceptance criteria' đầu tiên; None nếu không có git / chưa có commit."""
    if not is_git_repo(root):
        return None
    r = _git(["log", "--format=%cI", "--grep=^" + SIGN_COMMIT + "$"], root)
    lines = [ln.strip() for ln in (r.stdout or "").splitlines() if ln.strip()] if r.returncode == 0 else []
    if not lines:
        return None
    try:
        return datetime.fromisoformat(lines[-1]).astimezone().replace(tzinfo=None).isoformat(timespec="seconds")
    except ValueError:
        return None


def status(expect_hash: str | None = None) -> dict:
    """ok only if: lock exists, file hash == lock hash, and (if given) == optional instructor expect_hash."""
    out = {"ok": False, "hash": None, "signed_hash": None, "expect_hash": expect_hash, "problem": None}
    if not CRITERIA.exists():
        out["problem"] = "thiếu config/acceptance_criteria.json"
        return out
    out["hash"] = file_hash()
    if not LOCK.exists():
        out["problem"] = "chưa ký (chưa có acceptance_criteria.lock)"
        return out
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    out["signed_hash"], out["signed_at"] = lock["sha256"], lock.get("signed_at")
    if out["hash"] != lock["sha256"]:
        out["problem"] = "file tiêu chí ĐÃ BỊ SỬA sau khi ký"
    elif expect_hash and not lock["sha256"].startswith(expect_hash):
        out["problem"] = "hash đã ký KHÁC hash kỳ vọng (--expect-hash, tuỳ chọn cho giảng viên)"
    else:
        out["ok"] = True
    return out


def refuse_if_unsigned(what: str) -> str | None:
    """Câu từ chối (tiếng Việt) khi bàn định chạy đánh giá mà chưa ký tiêu chí; None nếu đã ký."""
    if LOCK.exists():
        return None
    return (f"TỪ CHỐI {what}: Bản tiêu chí chấp nhận chưa được ký.\n"
            f"  Luật của lab: bàn ký tiêu chí TRƯỚC khi nhìn bất kỳ con số đánh giá nào (phút 60–65).\n"
            f"  Việc cần làm:\n"
            f"    1. Điền xong config/acceptance_criteria.json (câu 1.6 của đề).\n"
            f"    2. Ký:  python3 -m lab10.criteria sign\n"
            f"    3. Lưu và đẩy:  {SIGN_GIT}\n"
            f"    4. Chạy lại lệnh vừa rồi.\n"
            f"  Chưa có gì được chạy, chưa có report nào được ghi.")


def main(argv=None):
    cmd = (argv or sys.argv[1:] or ["verify"])[0]
    if cmd == "sign":
        c = load()
        missing = [k for k in REQUIRED if c.get("required", {}).get(k) is None]
        if not c.get("team") or missing:
            sys.exit(f"Chưa ký được: thiếu team hoặc ngưỡng bắt buộc {missing}")
        if LOCK.exists():
            sys.exit("Đã ký rồi. Bản tiêu chí giữ nguyên tới hết buổi "
                     "(không xoá lock, không sửa file). Nếu chưa commit, chạy:\n  " + SIGN_GIT)
        h = file_hash()
        LOCK.write_text(json.dumps({"sha256": h, "signed_at": datetime.now().isoformat(timespec="seconds"),
                                    "team": c["team"]}, indent=1), encoding="utf-8")
        print("ĐÃ KÝ. Trước khi chạy đánh giá lần nào, lưu và đẩy lên repo của bàn bằng đúng lệnh sau:")
        print()
        print(SIGN_GIT)
        print()
        print(f"(hash file, chỉ để đối chiếu khi cần: {h})")
    else:
        s = status()
        print(json.dumps(s, ensure_ascii=False, indent=1))
        sys.exit(0 if s["ok"] else 1)


if __name__ == "__main__":
    main()
