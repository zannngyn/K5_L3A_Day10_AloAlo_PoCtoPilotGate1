"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def peak_hour_review_load(trials):
    """Số ca cần người xử lý (escalated hoặc recheck) lớn nhất dồn trong một khung 60 phút của một ngày (day, seed)."""
    if not trials:
        return 0.0
    buckets = {}
    for t in trials:
        needs_human = bool(t.get("review_kind")) or t.get("status") == "escalated"
        if needs_human and t.get("arrive_min") is not None:
            key = (t.get("day"), t.get("seed"))
            buckets.setdefault(key, []).append(float(t["arrive_min"]))
    if not buckets:
        return 0.0
    peak = 0
    for times in buckets.values():
        times.sort()
        for i, start in enumerate(times):
            count = sum(1 for x in times[i:] if x < start + 60.0)
            if count > peak:
                peak = count
    return float(peak)


def llm_degraded_rate(trials):
    """Tỉ lệ lượt chạy gặp lỗi 429 / fallback fail_open / retry từ nhà cung cấp LLM."""
    if not trials:
        return 0.0
    degraded = sum(
        any(e.get("type") in ("llm_error", "llm_fallback", "write_retry") for e in (t.get("events") or []))
        for t in trials
    )
    return degraded / len(trials)


def daily_cap_hit_rate(trials):
    """Tỉ lệ lượt chạy phải dừng hoàn tự động do chạm trần ngân sách hoàn tự động trong ngày."""
    if not trials:
        return 0.0
    hits = sum(
        any(
            (e.get("type") == "business_gate" and e.get("gate") == "daily_refund_cap_vnd")
            or (e.get("type") == "guard" and e.get("kind") == "daily_budget_guard")
            for e in (t.get("events") or [])
        )
        for t in trials
    )
    return hits / len(trials)


def model_override_rate(trials):
    """Tỉ lệ lượt chạy model tự đè số ngày khách khai lên dữ liệu tracking DB (bắt cả lỗi chìm ở bộ nền)."""
    if not trials:
        return 0.0
    overrides = sum(
        any(e.get("type") == "model_override" for e in (t.get("events") or []))
        for t in trials
    )
    return overrides / len(trials)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "peak_hour_review_load": peak_hour_review_load,
    "llm_degraded_rate": llm_degraded_rate,
    "daily_cap_hit_rate": daily_cap_hit_rate,
    "model_override_rate": model_override_rate,
}
STARTER_MONITORS = ("escalation_rate",)
