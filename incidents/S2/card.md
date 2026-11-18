# Thẻ sự cố S2 · Đối soát: shop bị trừ tiền lạ

## MẶT TRƯỚC

*Tin nhắn của kế toán đối soát trong kênh #doi-soat, 16/11/2026 10:05*

> **Phạm Kiều Oanh (kế toán đối soát):** Cả nhà ơi, bảng đối soát shop tuần này có mấy dòng **trừ tiền shop** cho yêu cầu
> *giao trễ*, trong khi giao trễ thì LogiX chịu phí chứ. Gốm Bát Tràng Cô Lụa bị trừ **475.000đ** cho một đơn chỉ trễ 4 ngày,
> thêm một khoản **3.230.000đ** không có mã phê duyệt nào. Cô Lụa gọi em hai lần rồi. Có đơn em đọc ticket thấy khách viết
> rất bình thường mà vẫn bị trừ cả đơn. Ngoài ra có một khách nhận 5 khoản hoàn tự động trong cùng một ngày, cộng lại
> vượt mức mà Ops từng thống nhất. Ai kiểm giúp em trước kỳ chốt 16h.

*(Thẻ chỉ mô tả triệu chứng. Tìm nguyên nhân là việc của bàn. Đừng dừng ở nguyên nhân đầu tiên tìm thấy.)*

**Thẻ này chỉ dành cho bàn bốc được số S2.** Bàn bốc số khác thì làm thẻ khác. Việc đầu tiên: ghi `Thẻ đã bốc: S2` vào dòng
đầu Phiếu C (`templates/form-c-incident.md`). Mọi lệnh tự kiểm tra của bàn dùng `--incident S2`.

## MẶT SAU

**Gói bằng chứng** (thư mục `incidents/S2/`: `tickets.jsonl` có nhãn, `world_patch.json`)
- Ticket nên dò trước: `S2-01`, `S2-04`, `S2-20`, `S2-07`, và loạt `S2-40` … `S2-44` (một khách, một ngày).
- Dữ kiện data: mỗi đơn có `merchant_id`, có đơn có thêm `checkout_note`; `data/world.json` → `ops_limits`, `policies[].auto_limit_vnd`.
- Trên trace, để ý `llm_extract`, `llm_extract_note`, `directive_obeyed`, `proposal` (trường `payer`), dòng sổ cái có `approval_id` hay không.

> **Khung tư duy: HAZOP guideword PERTURBED trên đầu vào, specification vs giả định môi trường + Mức kiểm soát của con người**
> - Câu hỏi dẫn dắt: Những chữ nào đi vào model mà KHÔNG do LogiX viết? Hệ thống đang giả định gì về các chữ đó? Specification nào của `issue_refund` mà nếu bị vi phạm thì shop mất tiền?
> - Ví dụ cách nghĩ (không phải đáp án của thẻ): Một giả định sai thường có dạng “chữ đi vào hệ thống chỉ là …”. Một spec tốt có dạng “với loại yêu cầu X, trường Y của lệnh ghi luôn phải bằng Z lấy từ nguồn sự thật”. Bàn tự điền X, Y, Z cho `issue_refund` từ trace của thẻ.
> - Viết vào Phiếu C (`templates/form-c-incident.md`); mục lục ở đầu phiếu.

**Nhiệm vụ** (khối 3 = phút 125–185, rồi v2 ở 185–200: bước 0 phút 125–135 · bước 1–4 phút 135–155, 20 phút phân tích · bước 5–7 phút 155–180, 25 phút sửa và chạy lại · bước 8 phút 180–185 · bước 9 phút 185–200).
Mọi câu trả lời viết vào **Phiếu C** (`templates/form-c-incident.md`), đúng mục ghi trong ngoặc.
0. **Trước khi sửa bất cứ thứ gì** (câu 3.0, Phiếu C mục C0–C1): `python3 -m lab10.grade --incident S2`. Đây là mốc **prepared**: chỉ có cổng vòng 1 của bàn.
   Ghi lại: cổng vòng 1 đã đỡ được ô nào, còn dòng "vượt trần" nào. Ghi **mã lần chạy** của mốc base và prepared.
1. Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau: `python3 -m lab10.trace --suite S2 --ticket <ID> --seed 11`. Tìm bước sai đầu tiên.
   Ghi từng lỗi vào **bảng soát lỗi** (câu 3.1, Phiếu C mục C2: loại lỗi, nguồn lỗi, hướng xử lý).
2. Đọc khối **kinh doanh và vận hành** và khối **theo kho và hãng** của report: hàng chờ, chi phí mỗi ticket, ROI, tổng hoàn so với trần. Nguyên nhân có thể nằm ở đây chứ không ở code.
3. **Phần riêng của thẻ này** (câu 3.1, Phiếu C mục C3): mục **C3.1 Mức kiểm soát của con người** (thay pre-mortem): soát 5 dấu hiệu, rồi điền bảng *ai · lệnh ghi nào · mức kiểm soát cần · mức hệ thống đang cho*. Mỗi dòng lệch là một nhánh của fault tree.
4. Một vòng **HAZOP của thẻ** (câu 3.1, Phiếu C mục C4, ≥ 3 dòng; không ghi đè HAZOP vòng 1 ở Phiếu B), viết **specification** và **giả định môi trường** (câu 3.2–3.3, mục C5),
   rồi vẽ **fault tree** (câu 3.4, mục C6): sự kiện đỉnh là tác hại trong tin nhắn; đừng dừng ở nhánh đầu tiên tìm thấy.
5. Sửa NGOÀI model (câu 3.5, mục C7). Ba chỗ được sửa, chọn đúng chỗ cho từng nguyên nhân: `lab10/guards.py` (chặn trước lệnh ghi, chuyển người, trần);
   `config/operating_gates.json` (phạm vi pilot, số người trực, trần tiền, ngân sách mỗi ticket, quy trình kiểm, cổng pháp lý);
   và ít nhất một chỉ số trong `lab10/monitors.py` (câu 3.6, mục C8).
6. Chạy lại: `python3 -m lab10.eval --suite S2 --stage after --note "đổi MỘT thứ: ..."`. Ghi **mã lần chạy** (mục C0).
7. Tự kiểm tra: `python3 -m lab10.grade --incident S2`. Report so ba mốc base · prepared · after. Lệnh này không cho điểm.
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
