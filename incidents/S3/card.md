# Thẻ sự cố S3 · Hãng miền Tây bị phạt vì bão

## MẶT TRƯỚC

*Tin nhắn Zalo OA của điều phối Mekong Delta Ship, 02/12/2026 09:30, kèm ghi chú của CSKH*

> **Điều phối Mekong Delta Ship:** Bên em ký phụ lục theo chính sách mới hiệu lực **01/12**: trễ do bão lũ thì không ghi lỗi
> hãng. Vậy mà mấy đơn kẹt bão số 9 vẫn bị ghi lỗi, 120.000đ mỗi lỗi. Có đơn tracking còn chưa ghi nguyên nhân trễ
> cũng ghi lỗi luôn cho bên em. Riêng hôm nay bên em nhận liền mấy lỗi, không thấy ai bên LogiX xác nhận.
>
> **Ghi chú CSKH cùng ngày:** vài khách trễ 2 ngày bị trợ lý từ chối hoàn phí, trong khi thông báo chính sách mới ghi
> từ 2 ngày là được hoàn.

*(Thẻ chỉ mô tả triệu chứng. Tìm nguyên nhân là việc của bàn. Đừng dừng ở nguyên nhân đầu tiên tìm thấy.)*

**Thẻ này chỉ dành cho bàn bốc được số S3.** Bàn bốc số khác thì làm thẻ khác. Việc đầu tiên: ghi `Thẻ đã bốc: S3` vào dòng
đầu Phiếu C (`templates/form-c-incident.md`). Mọi lệnh tự kiểm tra của bàn dùng `--incident S3`.

## MẶT SAU

**Gói bằng chứng** (thư mục `incidents/S3/`: `tickets.jsonl` có nhãn, `world_patch.json`)
- Ticket nên dò trước: `S3-01`, `S3-02`, `S3-04`, `S3-20`, và loạt `S3-40` … `S3-43`.
- Dữ kiện data: `data/world.json` → `policies` (so `effective_from` / `effective_to` với `index_active`; đọc `fault_causes`, `auto_limit_vnd`);
  `incidents/S3/world_patch.json` → `as_of`, và `delay_cause` của từng kiện.
- Trên trace, để ý sự kiện `policy` (đang dùng phiên bản nào), `tracking` (`cause`, `cause_recorded`), `proposal`.

> **Khung tư duy: Concept drift + HAZOP guideword INVALID / INCOMPLETE; mở lại bản đồ dữ liệu của câu 2.3**
> - Câu hỏi dẫn dắt: Thế giới đã đổi ở đâu mà hệ thống chưa đổi theo? Trường dữ liệu nào đang được coi là “sự thật” nhưng thực ra là bản sao cũ? Khi một trường bị trống, hệ thống mặc định về phía nào, và ai chịu thiệt vì mặc định đó?
> - Ví dụ cách nghĩ (không phải đáp án của thẻ): Drift có hai dạng: đầu vào đổi, hoặc quy tắc nghiệp vụ đổi mà hệ thống chưa đổi theo. Với mỗi trường bàn đang tin là “sự thật”: ai cập nhật nó, lần cuối khi nào? Với mỗi trường có thể trống: trống thì hệ thống nghiêng về phía ai?
> - Viết vào Phiếu C (`templates/form-c-incident.md`); mục lục ở đầu phiếu.

**Nhiệm vụ** (khối 3 = phút 125–185, rồi v2 ở 185–200: bước 0 phút 125–135 · bước 1–4 phút 135–155, 20 phút phân tích · bước 5–7 phút 155–180, 25 phút sửa và chạy lại · bước 8 phút 180–185 · bước 9 phút 185–200).
Mọi câu trả lời viết vào **Phiếu C** (`templates/form-c-incident.md`), đúng mục ghi trong ngoặc.
0. **Trước khi sửa bất cứ thứ gì** (câu 3.0, Phiếu C mục C0–C1): `python3 -m lab10.grade --incident S3`. Đây là mốc **prepared**: chỉ có cổng vòng 1 của bàn.
   Ghi lại: cổng vòng 1 đã đỡ được ô nào, còn dòng "vượt trần" nào. Ghi **mã lần chạy** của mốc base và prepared.
1. Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau: `python3 -m lab10.trace --suite S3 --ticket <ID> --seed 11`. Tìm bước sai đầu tiên.
   Ghi từng lỗi vào **bảng soát lỗi** (câu 3.1, Phiếu C mục C2: loại lỗi, nguồn lỗi, hướng xử lý).
2. Đọc khối **kinh doanh và vận hành** và khối **theo kho và hãng** của report: hàng chờ, chi phí mỗi ticket, ROI, tổng hoàn so với trần. Nguyên nhân có thể nằm ở đây chứ không ở code.
3. **Phần riêng của thẻ này** (câu 3.1, Phiếu C mục C3): mở lại pre-mortem bàn đã làm ở vòng 1 (Phiếu B mục B6) và ghi ở Phiếu C mục C1: sự cố trên thẻ có nằm trong các lý do bàn đã viết không? Thuộc lăng kính nào (kỹ thuật, kinh doanh, con người và vận hành, pháp lý)? Thêm lý do còn thiếu bằng bút khác màu. Mở lại bản đồ dữ liệu của câu 2.3 (ghi ở mục C3.5): bảng `policies` có trường nào là nguồn sự thật về “phiên bản đang hiệu lực”, trường nào là bản sao?
4. Một vòng **HAZOP của thẻ** (câu 3.1, Phiếu C mục C4, ≥ 3 dòng; không ghi đè HAZOP vòng 1 ở Phiếu B), viết **specification** và **giả định môi trường** (câu 3.2–3.3, mục C5),
   rồi vẽ **fault tree** (câu 3.4, mục C6): sự kiện đỉnh là tác hại trong tin nhắn; đừng dừng ở nhánh đầu tiên tìm thấy.
5. Sửa NGOÀI model (câu 3.5, mục C7). Ba chỗ được sửa, chọn đúng chỗ cho từng nguyên nhân: `lab10/guards.py` (chặn trước lệnh ghi, chuyển người, trần);
   `config/operating_gates.json` (phạm vi pilot, số người trực, trần tiền, ngân sách mỗi ticket, quy trình kiểm, cổng pháp lý);
   và ít nhất một chỉ số trong `lab10/monitors.py` (câu 3.6, mục C8).
6. Chạy lại: `python3 -m lab10.eval --suite S3 --stage after --note "đổi MỘT thứ: ..."`. Ghi **mã lần chạy** (mục C0).
7. Tự kiểm tra: `python3 -m lab10.grade --incident S3`. Report so ba mốc base · prepared · after. Lệnh này không cho điểm.
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
