# Thẻ sự cố S8 · Trưởng ca CSKH: chúng tôi không tin trợ lý, đang kiểm tay hết

## MẶT TRƯỚC

*Tin nhắn của trưởng ca CSKH gửi quản lý, 16/11/2026 15:10, sau khi nhận bảng kiểm toán nội bộ*

> **Trần Thị Hạnh (trưởng ca CSKH):** Anh ơi, bảng kiểm toán ghi em là người duyệt mấy khoản bồi thường trên 200.000đ hôm nay.
> Em **không duyệt** các khoản đó. Có mã em cấp cho ticket khác, có mã hết hạn từ 10/11, có mã em đã thu hồi, có mã em chỉ
> duyệt tới 150.000đ mà khoản chi là 235.000đ. Người đứng tên duyệt phải giải trình, nên từ trưa em đã bảo cả ca
> **kiểm lại bằng tay mọi quyết định của trợ lý**, kể cả mấy khoản 20.000đ.
> Giờ hàng chờ của em hơn bốn chục ca, có ca chờ mấy tiếng, mà trợ lý cũng không nói **vì sao** nó quyết như vậy nên bọn em
> phải tra lại từ đầu. Làm thế này còn chậm và tốn hơn hồi chưa có trợ lý. Em cần biết: hệ thống lấy mã duyệt kiểu gì,
> và bao giờ thì bọn em được thôi kiểm tay từng cái.

*(Thẻ chỉ mô tả triệu chứng. Tìm nguyên nhân là việc của bàn. Đừng dừng ở nguyên nhân đầu tiên tìm thấy.)*

**Thẻ này chỉ dành cho bàn bốc được số S8.** Bàn bốc số khác thì làm thẻ khác. Việc đầu tiên: ghi `Thẻ đã bốc: S8` vào dòng
đầu Phiếu C (`templates/form-c-incident.md`). Mọi lệnh tự kiểm tra của bàn dùng `--incident S8`.

## MẶT SAU

**Gói bằng chứng** (thư mục `incidents/S8/`: `tickets.jsonl` có nhãn, `world_patch.json`)
- Chạy `python3 -m lab10.eval --suite S8 --stage base` rồi đọc khối **kinh doanh và vận hành**: nhân viên kiểm lại bao nhiêu phần trăm
  quyết định tự động, hàng chờ, số ca ùn, chi phí mỗi ticket so với làm tay.
- Dữ kiện data: `incidents/S8/world_patch.json` → `staff_behavior` (nhân viên đang kiểm lại bao nhiêu, và **điều kiện để họ chuyển sang kiểm mẫu**),
  `approvals` (đọc từng trường: `ticket_id`, `order_id`, `customer_id`, `max_vnd`, `expires_at`, `status`); `data/world.json` → `staff`, `ops_facts`.
- Ticket nên dò: `S8-01`, `S8-02`, `S8-03`, `S8-06`; đối chứng `S8-05` (phê duyệt hợp lệ); loạt `S8-40` … `S8-44`; và một ticket nhỏ bất kỳ `S8-60` … `S8-99`.
- Trên trace, để ý sự kiện `approval_used`, rồi tự đối chiếu mã đó với bảng `approvals`. Trong report grade, đọc dòng "Niềm tin của nhân viên duyệt".

> **Khung tư duy: Hiệu chỉnh lòng tin + Mức kiểm soát của con người + HAZOP guideword INVALID**
> - Câu hỏi dẫn dắt: Người duyệt đang tin hệ thống quá mức, hay không tin? Vì dữ liệu nào, vì điều gì họ không được biết? Một “phê duyệt” phải thoả những điều kiện gì mới còn giá trị? Để người ta thôi kiểm tay từng cái, họ cần thấy gì, và cần được giữ quyền ở đâu?
> - Ví dụ cách nghĩ (không phải đáp án của thẻ): Lòng tin không sửa được bằng một dòng code. Hỏi: nhân viên duyệt đã thấy gì khiến họ thôi tin? Họ cần thấy gì ở mỗi quyết định, và quy trình nào hai bên chấp nhận, để thôi kiểm tay từng cái?
> - Viết vào Phiếu C (`templates/form-c-incident.md`); mục lục ở đầu phiếu.

**Nhiệm vụ** (khối 3 = phút 125–185, rồi v2 ở 185–200: bước 0 phút 125–135 · bước 1–4 phút 135–155, 20 phút phân tích · bước 5–7 phút 155–180, 25 phút sửa và chạy lại · bước 8 phút 180–185 · bước 9 phút 185–200).
Mọi câu trả lời viết vào **Phiếu C** (`templates/form-c-incident.md`), đúng mục ghi trong ngoặc.
0. **Trước khi sửa bất cứ thứ gì** (câu 3.0, Phiếu C mục C0–C1): `python3 -m lab10.grade --incident S8`. Đây là mốc **prepared**: chỉ có cổng vòng 1 của bàn.
   Ghi lại: cổng vòng 1 đã đỡ được ô nào, còn dòng "vượt trần" nào. Ghi **mã lần chạy** của mốc base và prepared.
1. Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau: `python3 -m lab10.trace --suite S8 --ticket <ID> --seed 11`. Tìm bước sai đầu tiên.
   Ghi từng lỗi vào **bảng soát lỗi** (câu 3.1, Phiếu C mục C2: loại lỗi, nguồn lỗi, hướng xử lý).
2. Đọc khối **kinh doanh và vận hành** và khối **theo kho và hãng** của report: hàng chờ, chi phí mỗi ticket, ROI, tổng hoàn so với trần. Nguyên nhân có thể nằm ở đây chứ không ở code.
3. **Phần riêng của thẻ này** (câu 3.1, Phiếu C mục C3): mục **C3.4 Hiệu chỉnh lòng tin**: điền cho hai nhóm người (nhân viên duyệt, trưởng ca đứng tên) hai mốc “tin quá mức” (trước kiểm toán) và “không tin” (sau kiểm toán): dữ liệu nào của hệ thống làm lòng tin lệch, họ cần thấy gì để về mốc “tin vừa đủ”. Kèm **một dòng** “hoàn trên hạn mức” ở bảng mục C3.1 Bước 2.
4. Một vòng **HAZOP của thẻ** (câu 3.1, Phiếu C mục C4, ≥ 3 dòng; không ghi đè HAZOP vòng 1 ở Phiếu B), viết **specification** và **giả định môi trường** (câu 3.2–3.3, mục C5),
   rồi vẽ **fault tree** (câu 3.4, mục C6): sự kiện đỉnh là tác hại trong tin nhắn; đừng dừng ở nhánh đầu tiên tìm thấy.
5. Sửa NGOÀI model (câu 3.5, mục C7). Ba chỗ được sửa, chọn đúng chỗ cho từng nguyên nhân: `lab10/guards.py` (chặn trước lệnh ghi, chuyển người, trần);
   `config/operating_gates.json` (phạm vi pilot, số người trực, trần tiền, ngân sách mỗi ticket, quy trình kiểm, cổng pháp lý);
   và ít nhất một chỉ số trong `lab10/monitors.py` (câu 3.6, mục C8).
6. Chạy lại: `python3 -m lab10.eval --suite S8 --stage after --note "đổi MỘT thứ: ..."`. Ghi **mã lần chạy** (mục C0).
7. Tự kiểm tra: `python3 -m lab10.grade --incident S8`. Report so ba mốc base · prepared · after. Lệnh này không cho điểm.
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
