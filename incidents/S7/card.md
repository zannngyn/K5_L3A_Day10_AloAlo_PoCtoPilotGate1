# Thẻ sự cố S7 · Email pháp chế: lộ số điện thoại người nhận quà

## MẶT TRƯỚC

*Email của bộ phận Pháp chế, 16/11/2026 11:30, đánh dấu KHẨN*

> **Tiêu đề: [KHẨN] Phản ánh lộ thông tin người nhận hàng**
>
> Một người nhận quà (không phải khách đặt hàng) phản ánh bị nhân viên hãng vận chuyển gọi điện “xin lỗi vì giao trễ” và đọc
> đúng tên, địa chỉ nhà. Bà chưa từng cung cấp số điện thoại cho hãng. Kiểm sơ bộ: thông báo lỗi LogiX gửi hãng có chứa
> thông tin liên hệ của người nhận. Theo quy định dữ liệu chia sẻ trong hợp đồng, thông báo cho hãng chỉ gồm mã đơn, mã
> kiện, quận/huyện và số ngày trễ. Có trường hợp khách **không hề gõ** thông tin đó vào ticket mà thông báo vẫn có.
> Đề nghị báo cáo nguyên nhân và biện pháp trong ngày. *(Căn cứ pháp lý cụ thể do Pháp chế bổ sung: cần kiểm.)*

*(Thẻ chỉ mô tả triệu chứng. Tìm nguyên nhân là việc của bàn. Đừng dừng ở nguyên nhân đầu tiên tìm thấy.)*

**Thẻ này chỉ dành cho bàn bốc được số S7.** Bàn bốc số khác thì làm thẻ khác. Việc đầu tiên: ghi `Thẻ đã bốc: S7` vào dòng
đầu Phiếu C (`templates/form-c-incident.md`). Mọi lệnh tự kiểm tra của bàn dùng `--incident S7`.

## MẶT SAU

**Gói bằng chứng** (thư mục `incidents/S7/`: `tickets.jsonl` có nhãn, `world_patch.json`)
- Ticket nên dò trước: `S7-01`, `S7-04`, `S7-20`, `S7-21`; đối chứng với `S7-05` (ticket có dãy số nhưng không phải SĐT).
- Dữ kiện data: `data/world.json` → `policies[].carrier_notice_fields`; trong gói: `orders[].recipient`, `orders[].is_gift`.
- Trên trace, đọc kỹ dòng `GỬI HÃNG` (payload của `notify_carrier`): có những trường nào, mỗi trường lấy từ đâu.

> **Khung tư duy: Specification vs giả định môi trường, giảm hay bảo đảm + Hiệu chỉnh lòng tin**
> - Câu hỏi dẫn dắt: Dữ liệu nào rời khỏi hệ thống, tới ai, và ai đã đồng ý? Spec của kênh gửi hãng là gì? Biện pháp của đội là giảm khả năng lộ (dò và che) hay bảo đảm không lộ (chỉ cho đi những gì được phép)?
> - Ví dụ cách nghĩ (không phải đáp án của thẻ): Ví dụ ngoài thẻ: che số thẻ ngân hàng bằng mẫu ký tự là GIẢM (mẫu viết khác sẽ lọt); chỉ cho đi những trường đã liệt kê là BẢO ĐẢM. Spec của kênh gửi hãng do bàn tự viết từ dữ liệu của thẻ.
> - Viết vào Phiếu C (`templates/form-c-incident.md`); mục lục ở đầu phiếu.

**Nhiệm vụ** (khối 3 = phút 125–185, rồi v2 ở 185–200: bước 0 phút 125–135 · bước 1–4 phút 135–155, 20 phút phân tích · bước 5–7 phút 155–180, 25 phút sửa và chạy lại · bước 8 phút 180–185 · bước 9 phút 185–200).
Mọi câu trả lời viết vào **Phiếu C** (`templates/form-c-incident.md`), đúng mục ghi trong ngoặc.
0. **Trước khi sửa bất cứ thứ gì** (câu 3.0, Phiếu C mục C0–C1): `python3 -m lab10.grade --incident S7`. Đây là mốc **prepared**: chỉ có cổng vòng 1 của bàn.
   Ghi lại: cổng vòng 1 đã đỡ được ô nào, còn dòng "vượt trần" nào. Ghi **mã lần chạy** của mốc base và prepared.
1. Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau: `python3 -m lab10.trace --suite S7 --ticket <ID> --seed 11`. Tìm bước sai đầu tiên.
   Ghi từng lỗi vào **bảng soát lỗi** (câu 3.1, Phiếu C mục C2: loại lỗi, nguồn lỗi, hướng xử lý).
2. Đọc khối **kinh doanh và vận hành** và khối **theo kho và hãng** của report: hàng chờ, chi phí mỗi ticket, ROI, tổng hoàn so với trần. Nguyên nhân có thể nằm ở đây chứ không ở code.
3. **Phần riêng của thẻ này** (câu 3.1, Phiếu C mục C3): mục **C3.3 Hiệu chỉnh lòng tin** (thay pre-mortem): điền hai mốc “tin quá mức” và “không tin” cho người đặt hàng và người nhận hàng, ghi dữ liệu nào rời hệ thống mà họ không biết.
4. Một vòng **HAZOP của thẻ** (câu 3.1, Phiếu C mục C4, ≥ 3 dòng; không ghi đè HAZOP vòng 1 ở Phiếu B), viết **specification** và **giả định môi trường** (câu 3.2–3.3, mục C5),
   rồi vẽ **fault tree** (câu 3.4, mục C6): sự kiện đỉnh là tác hại trong tin nhắn; đừng dừng ở nhánh đầu tiên tìm thấy.
5. Sửa NGOÀI model (câu 3.5, mục C7). Ba chỗ được sửa, chọn đúng chỗ cho từng nguyên nhân: `lab10/guards.py` (chặn trước lệnh ghi, chuyển người, trần);
   `config/operating_gates.json` (phạm vi pilot, số người trực, trần tiền, ngân sách mỗi ticket, quy trình kiểm, cổng pháp lý);
   và ít nhất một chỉ số trong `lab10/monitors.py` (câu 3.6, mục C8).
6. Chạy lại: `python3 -m lab10.eval --suite S7 --stage after --note "đổi MỘT thứ: ..."`. Ghi **mã lần chạy** (mục C0).
7. Tự kiểm tra: `python3 -m lab10.grade --incident S7`. Report so ba mốc base · prepared · after. Lệnh này không cho điểm.
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
