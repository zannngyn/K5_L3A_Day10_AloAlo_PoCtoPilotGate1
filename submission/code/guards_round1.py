"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    # Pin the effective version before the agent reads the stale policy index.
    try:
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    except (KeyError, TypeError, ValueError):
        policy = None
    if policy is None:
        return Verdict.escalate("không xác định được chính sách hiệu lực")
    return Verdict.allow(policy_id=policy["policy_id"])


def _facts(ctx):
    """Use DB facts only; ticket text and model proposals are not authority."""
    order = ctx.tools.lookup_order(ctx.ticket.get("order_id"))
    if not order or order.get("customer_id") != ctx.ticket.get("customer_id"):
        raise ValueError("không xác minh được đơn và chủ đơn")
    if not order.get("parcels"):
        raise ValueError("thiếu tracking kiện hàng")
    parcel_id = ctx.ticket.get("parcel_id")
    if parcel_id and not any(p.get("parcel_id") == parcel_id for p in order["parcels"]):
        raise ValueError("kiện yêu cầu không thuộc đơn")
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        raise ValueError("không có chính sách hiệu lực")
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)
    return order, parcel, policy, delay


def write_gate(ctx, action):
    tool = action.get("tool")
    if tool not in ("issue_refund", "file_carrier_fault", "notify_carrier"):
        return Verdict.allow()
    try:
        order, parcel, policy, delay = _facts(ctx)
    except (KeyError, TypeError, ValueError) as exc:
        if tool == "issue_refund":
            return Verdict.escalate("thiếu căn cứ hoàn tiền: " + str(exc))
        return Verdict.deny("thiếu căn cứ gửi/ghi lỗi hãng: " + str(exc))

    if action.get("ticket_id") != ctx.ticket.get("ticket_id"):
        return Verdict.deny("lệnh ghi không thuộc ticket đang xử lý")

    # Gate 1: refund entitlement and approval belong to this transaction.
    if tool == "issue_refund":
        if action.get("order_id") != order["order_id"]:
            return Verdict.escalate("lệnh hoàn không thuộc đơn đang xử lý")
        if parcel.get("delay_cause") is None:
            return Verdict.escalate("chưa ghi nhận nguyên nhân trễ; cần xác minh")
        amount = action.get("amount_vnd")
        entitled = H.entitlement_vnd(policy, order, delay, parcel["delay_cause"])
        if entitled <= 0:
            return Verdict.deny("tracking DB và chính sách hiệu lực chưa cho phép hoàn")
        if type(amount) is not int or amount != entitled or action.get("payer") != "LOGIX":
            return Verdict.escalate("tiền hoàn hoặc bên chịu phí không khớp quyền lợi từ DB")
        approval_id = action.get("approval_id")
        if amount > policy["auto_limit_vnd"] and not approval_id:
            return Verdict.escalate("vượt hạn mức tự động, cần phê duyệt hợp lệ")
        if approval_id:
            approvals = ctx.tools.lookup_approvals(approval_id=approval_id)
            approval = approvals[0] if len(approvals) == 1 else {}
            expected_approver = (ctx.gates or {}).get("operations", {}).get("approver_id")
            try:
                valid = (
                    approval.get("status") == "valid"
                    and approval.get("ticket_id") == ctx.ticket["ticket_id"]
                    and approval.get("order_id") == order["order_id"]
                    and approval.get("customer_id") == order["customer_id"]
                    and H.d(approval["expires_at"]) >= H.d(ctx.as_of)
                    and approval["max_vnd"] >= amount
                    and (not expected_approver or approval.get("approver_id") == expected_approver)
                    and not ctx.tools.ledger_rows(approval_id=approval_id)
                )
            except (KeyError, TypeError, ValueError):
                valid = False
            if not valid:
                return Verdict.escalate("phê duyệt sai đối tượng, hết hạn, đã dùng hoặc thiếu hạn mức")

    # Gate 2: check the actual parcel, carrier, cause and delay before a strike.
    elif tool == "file_carrier_fault":
        if (action.get("order_id") != order["order_id"]
                or action.get("parcel_id") != parcel["parcel_id"]
                or action.get("carrier_id") != parcel["carrier_id"]
                or action.get("driver_id") != parcel.get("driver_id")
                or action.get("delay_days") != delay
                or not H.carrier_at_fault(policy, parcel, delay)):
            return Verdict.deny("lỗi hãng không khớp kiện, tracking DB hoặc chính sách hiệu lực")

    # Gate 3: rebuild an allowlisted message from DB, never forward free text.
    elif tool == "notify_carrier":
        payload = action.get("payload")
        if (not isinstance(payload, dict)
                or payload.get("order_id") != order["order_id"]
                or payload.get("parcel_id") != parcel["parcel_id"]
                or action.get("carrier_id") != parcel["carrier_id"]
                or not H.carrier_at_fault(policy, parcel, delay)
                or not ctx.tools.fault_rows(ticket_id=ctx.ticket["ticket_id"],
                                            order_id=order["order_id"],
                                            parcel_id=parcel["parcel_id"],
                                            carrier_id=parcel["carrier_id"])):
            return Verdict.deny("thông báo hãng chưa có bản ghi lỗi hợp lệ cho đúng kiện")
        allowed = set(policy.get("carrier_notice_fields") or [])
        blocked = set((ctx.gates or {}).get("legal", {}).get("pii_fields_blocked_to_third_party") or [])
        facts = {"order_id": order["order_id"], "parcel_id": parcel["parcel_id"],
                 "district": order.get("recipient", {}).get("district"), "delay_days": delay}
        clean = {k: v for k, v in facts.items() if k in allowed and k not in blocked and v is not None}
        if clean != payload:
            ctx.log("carrier_payload_filtered", dropped_fields=sorted(set(payload) - set(clean)))
            return Verdict.modify("chỉ gửi dữ kiện DB thuộc allowlist và không bị cấm", payload=clean)
    return Verdict.allow()
