# Thẻ sự cố S5 · CFO: mỗi ticket qua trợ lý đang đắt hơn làm tay

## MẶT TRƯỚC

*Email của Giám đốc tài chính gửi nhóm dự án, 16/11/2026 09:30, kèm bảng chi phí hai tuần PoC*

> **Từ:** Giám đốc tài chính · **Tới:** nhóm trợ lý hoàn tiền · **CC:** chị Oanh (đối soát)
>
> Tôi xem bảng chi phí hai tuần. Ba chỗ tôi không ký được:
> 1. **Kho sỉ TP.HCM**: gần như ticket nào trợ lý cũng đọc xong rồi lại chuyển cho người. Vậy mỗi ticket ở đó tôi trả
>    **cả tiền trợ lý lẫn công người**, đắt hơn làm tay như cũ.
> 2. Có những ticket tiền LLM **cao gấp nhiều lần** ticket thường. Trần đã thống nhất là 1.500đ một ticket.
> 3. Chị Oanh báo có đơn **hoàn hai, ba lần**. Tiền đó mất thật, không phải chi phí vận hành.
>
> Tôi không hỏi mô hình có thông minh không. Tôi hỏi: **chạy thử thế này thì lời hay lỗ, và lỗ ở đâu?** Trước 17h.

*(Thẻ chỉ mô tả triệu chứng. Tìm nguyên nhân là việc của bàn. Đừng dừng ở nguyên nhân đầu tiên tìm thấy.)*

**Thẻ này chỉ dành cho bàn bốc được số S5.** Bàn bốc số khác thì làm thẻ khác. Việc đầu tiên: ghi `Thẻ đã bốc: S5` vào dòng
đầu Phiếu C (`templates/form-c-incident.md`). Mọi lệnh tự kiểm tra của bàn dùng `--incident S5`.

## MẶT SAU

**Gói bằng chứng** (thư mục `incidents/S5/`: `tickets.jsonl` có nhãn, `world_patch.json`)
- Chạy `python3 -m lab10.eval --suite S5 --stage base` rồi đọc khối **kinh doanh và vận hành**: chi phí mỗi ticket so với làm tay,
  ticket tốn LLM nhiều nhất so với trần, tiết kiệm ròng, ROI, và dòng "vượt trần" theo từng kho.
- Dữ kiện data: mỗi đơn có `warehouse_id`; `data/world.json` → `warehouses`, `ops_facts` (giá LLM tính theo độ dài chữ, công làm tay,
  công duyệt), `ops_limits.max_llm_cost_per_ticket_vnd`, `policies[].auto_limit_vnd`.
- Ticket nên dò: `S5-51` (kho sỉ: trợ lý làm tới bước nào rồi dừng?), `S5-50` và `S5-70` (xem `cost_vnd` ở sự kiện `result`, và độ dài nội dung),
  cặp `S5-01` → `S5-02` (cùng một đơn), `S5-20`.
- Trong `incidents/S5/world_patch.json` → `ledger_seed`: những dòng đã có trong sổ cái trước khi trợ lý chạy.

> **Khung tư duy: Thước đo → Dữ liệu → Cách tính cho một con số kinh doanh + pre-mortem mở rộng sang kinh doanh; phạm vi pilot**
> - Câu hỏi dẫn dắt: Tiền đi ra ở những dòng nào: tiền máy, công người, tiền mất? Dòng nào tăng theo số ticket, dòng nào tăng theo LOẠI ticket? Có nhóm ticket nào mà tự động hoá không thể có lời, dù model tốt đến đâu?
> - Ví dụ cách nghĩ (không phải đáp án của thẻ): Tách chi phí theo dòng tiền (máy, công người, tiền mất) VÀ theo nhóm ticket (kho, loại đơn). Nhóm nào mà trợ lý đọc xong vẫn phải chuyển người thì tự động hoá chỉ thêm tiền máy, không bớt được công người.
> - Viết vào Phiếu C (`templates/form-c-incident.md`); mục lục ở đầu phiếu.

**Nhiệm vụ** (khối 3 = phút 125–185, rồi v2 ở 185–200: bước 0 phút 125–135 · bước 1–4 phút 135–155, 20 phút phân tích · bước 5–7 phút 155–180, 25 phút sửa và chạy lại · bước 8 phút 180–185 · bước 9 phút 185–200).
Mọi câu trả lời viết vào **Phiếu C** (`templates/form-c-incident.md`), đúng mục ghi trong ngoặc.
0. **Trước khi sửa bất cứ thứ gì** (câu 3.0, Phiếu C mục C0–C1): `python3 -m lab10.grade --incident S5`. Đây là mốc **prepared**: chỉ có cổng vòng 1 của bàn.
   Ghi lại: cổng vòng 1 đã đỡ được ô nào, còn dòng "vượt trần" nào. Ghi **mã lần chạy** của mốc base và prepared.
1. Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau: `python3 -m lab10.trace --suite S5 --ticket <ID> --seed 11`. Tìm bước sai đầu tiên.
   Ghi từng lỗi vào **bảng soát lỗi** (câu 3.1, Phiếu C mục C2: loại lỗi, nguồn lỗi, hướng xử lý).
2. Đọc khối **kinh doanh và vận hành** và khối **theo kho và hãng** của report: hàng chờ, chi phí mỗi ticket, ROI, tổng hoàn so với trần. Nguyên nhân có thể nằm ở đây chứ không ở code.
3. **Phần riêng của thẻ này** (câu 3.1, Phiếu C mục C3): mở lại pre-mortem bàn đã làm ở vòng 1 (Phiếu B mục B6) và ghi ở Phiếu C mục C1: sự cố trên thẻ có nằm trong các lý do bàn đã viết không? Thuộc lăng kính nào (kỹ thuật, kinh doanh, con người và vận hành, pháp lý)? Thêm lý do còn thiếu bằng bút khác màu. Mở lại bản đồ dữ liệu (mục C3.5) nếu dữ liệu liên quan. Rồi dùng bảng ba ô ở Phiếu C mục C8 cho MỘT con số kinh doanh (chi phí mỗi ticket theo kho): thước đo, dữ liệu, cách tính, ngưỡng.
4. Một vòng **HAZOP của thẻ** (câu 3.1, Phiếu C mục C4, ≥ 3 dòng; không ghi đè HAZOP vòng 1 ở Phiếu B), viết **specification** và **giả định môi trường** (câu 3.2–3.3, mục C5),
   rồi vẽ **fault tree** (câu 3.4, mục C6): sự kiện đỉnh là tác hại trong tin nhắn; đừng dừng ở nhánh đầu tiên tìm thấy.
5. Sửa NGOÀI model (câu 3.5, mục C7). Ba chỗ được sửa, chọn đúng chỗ cho từng nguyên nhân: `lab10/guards.py` (chặn trước lệnh ghi, chuyển người, trần);
   `config/operating_gates.json` (phạm vi pilot, số người trực, trần tiền, ngân sách mỗi ticket, quy trình kiểm, cổng pháp lý);
   và ít nhất một chỉ số trong `lab10/monitors.py` (câu 3.6, mục C8).
6. Chạy lại: `python3 -m lab10.eval --suite S5 --stage after --note "đổi MỘT thứ: ..."`. Ghi **mã lần chạy** (mục C0).
7. Tự kiểm tra: `python3 -m lab10.grade --incident S5`. Report so ba mốc base · prepared · after. Lệnh này không cho điểm.
8. Câu 3.7: cập nhật fault tree (mục C9), thêm 1 dòng Risk register (C10), cập nhật checklist 9 nhóm việc (cột PIC) và viết **runbook phần 4–5** (C11).
9. Viết quyết định Gate 1 **v2** (Phiếu C mục C12, so với v1 ở Phiếu B mục B8) kèm lý do và số trong report. Điền `submission/submission.json`, rồi
   `python3 -m lab10.check_submission --collect` tới khi thấy `ĐỦ THÀNH PHẦN`.

**Luật**
- Không sửa Bản tiêu chí chấp nhận đã ký, không sửa bản chốt cổng vòng 1 (`guards_round1.py`, `operating_gates.round1.json`). Lệnh tự kiểm tra in hash của cả hai.
- Không sửa nhắm vào ID ticket hay câu chữ cụ thể. Bài kiểm tra ẩn dùng đơn mới, khách mới, cách viết khác.
- Không làm hỏng cái đang đúng: ca nào của bộ nền trước đạt thì sau vẫn phải đạt. Ca hợp lệ vẫn phải được phục vụ.
- Chỉ sửa `lab10/guards.py`, `lab10/monitors.py`, `config/operating_gates.json`, `config/switches.json`. Các file khác bị khoá.
- Thu hẹp phạm vi về 0, hay xếp thật nhiều người trực, không phải là cách sửa: độ phủ và ROI đều được đo.

**Nộp** (tất cả nằm trong `submission/`; lệnh `check_submission --collect` gom giúp)
- Mã lần chạy của **ba mốc** base · prepared · after và report tự kiểm tra.
- Code cổng vòng 1 (bản chốt) và vòng 2, config cổng vòng 1 và hiện tại, tiêu chí đã ký kèm hash.
- Ba phiếu A, B, C. Trong Phiếu C: bảng soát lỗi và phần riêng của thẻ, ≥ 3 dòng HAZOP của thẻ, fault tree trước và sau khi sửa,
  dòng Risk register mới, cập nhật checklist 9 nhóm việc (cột PIC), runbook phần 4–5.
- Quyết định Gate 1 v1 (Phiếu B) và v2 (Phiếu C), số thẻ đã bốc, và **ba dòng bắt buộc**:
  1. Một **giả định về môi trường** mà thiết kế của đội đang dựa vào, có thể sai ngoài thực tế: …
  2. Cổng của đội chỉ **GIẢM khả năng** hay thực sự **NGĂN** được tác hại? Vì sao: …
  3. Vì data ở đây là mock, **cần đo lại gì trong pilot thật** trước Bước đánh giá 2: …
