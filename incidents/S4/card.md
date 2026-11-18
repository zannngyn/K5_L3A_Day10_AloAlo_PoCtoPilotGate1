# Thẻ sự cố S4 · Đêm 11.11: ticket gấp ba, hàng chờ duyệt ngập

## MẶT TRƯỚC

*Tin nhắn của giám sát vận hành trên kênh #van-hanh-tro-ly, 11/11, 23:40, kèm ảnh chụp hàng chờ*

> **Lê Thanh Tùng (giám sát vận hành):** Tối nay số ticket **gấp ba ngày thường**, dồn gần hết vào một giờ sau 20h.
> Hàng chờ người duyệt đang có ca **chờ hơn một tiếng**, mà cả ca chỉ có **một mình chị Hạnh** trực. Phần lớn là hàng vỡ và
> thất lạc, trợ lý không được tự xử lý nên đẩy hết sang người.
> Lúc nhà cung cấp LLM nghẽn thì trợ lý lại *duyệt nhiều hơn*: có đơn chưa đủ điều kiện, có đơn do **shop bàn giao muộn**, vẫn
> được hoàn phí, và hãng vẫn bị ghi lỗi.
> Chị Oanh bên Finance vừa nhắn: tổng hoàn tự động hôm nay đã **vượt 300.000đ**, là mức Finance chốt riêng cho ngày sale.
> Mai còn một đợt sale nữa. Tôi cần biết: giữ nguyên, thêm người, thu hẹp, hay tắt?

*(Thẻ chỉ mô tả triệu chứng. Tìm nguyên nhân là việc của bàn. Đừng dừng ở nguyên nhân đầu tiên tìm thấy.)*

**Thẻ này chỉ dành cho bàn bốc được số S4.** Bàn bốc số khác thì làm thẻ khác. Việc đầu tiên: ghi `Thẻ đã bốc: S4` vào dòng
đầu Phiếu C (`templates/form-c-incident.md`). Mọi lệnh tự kiểm tra của bàn dùng `--incident S4`.

## MẶT SAU

**Gói bằng chứng** (thư mục `incidents/S4/`: `tickets.jsonl` có nhãn, `world_patch.json`)
- Cả ngày 11.11 là MỘT ngày vận hành: các ticket `S4-01` … `S4-41` chạy nối nhau trên cùng một sổ cái, mỗi ticket có phút tới (`arrive_min`).
- Chạy `python3 -m lab10.eval --suite S4 --stage base` rồi đọc khối **kinh doanh và vận hành** ở cuối: số ca vào hàng chờ, chờ lâu nhất,
  số ca bị ùn, tổng hoàn tự động một ngày so với ngân sách, chi phí mỗi ticket, ROI.
- Dữ kiện data: `incidents/S4/world_patch.json` → `ops_limits` (ngân sách hoàn tự động riêng ngày 11.11, hạn chờ 60 phút), `llm_faults`;
  `data/world.json` → `ops_facts` (một người duyệt được mấy ca mỗi giờ, phí giữ chỗ mỗi người trực, công làm tay một ticket), `warehouses`.
- Ticket nên dò: một ticket vỡ hàng giữa giờ cao điểm (`S4-07`), và `S4-08` ở nhiều seed (11, 22, 33…): seed nào đạt, seed nào hỏng.
- Trên trace, để ý `llm_error`, `llm_fallback`, `proposal.basis`; trong report, để ý dòng "vượt trần".

> **Khung tư duy: Pre-mortem mở rộng sang vận hành và kinh doanh + HAZOP guideword INCAPABLE; runbook vận hành**
> - Câu hỏi dẫn dắt: Khi lượng việc tăng gấp ba, thứ gì hết trước: máy, tiền, hay người? Hệ thống rơi về trạng thái an toàn hay tiện lợi khi một thành phần không trả lời? Ai được quyền quyết thêm người, thu hẹp, hay tắt, và nhìn con số nào để quyết?
> - Ví dụ cách nghĩ (không phải đáp án của thẻ): INCAPABLE không chỉ là máy lỗi. Một người duyệt 6 ca mỗi giờ cũng là một thành phần có giới hạn: 14 ca tới trong một giờ thì ca cuối chờ hơn 60 phút.
> - Viết vào Phiếu C (`templates/form-c-incident.md`); mục lục ở đầu phiếu.

**Nhiệm vụ** (khối 3 = phút 125–185, rồi v2 ở 185–200: bước 0 phút 125–135 · bước 1–4 phút 135–155, 20 phút phân tích · bước 5–7 phút 155–180, 25 phút sửa và chạy lại · bước 8 phút 180–185 · bước 9 phút 185–200).
Mọi câu trả lời viết vào **Phiếu C** (`templates/form-c-incident.md`), đúng mục ghi trong ngoặc.
0. **Trước khi sửa bất cứ thứ gì** (câu 3.0, Phiếu C mục C0–C1): `python3 -m lab10.grade --incident S4`. Đây là mốc **prepared**: chỉ có cổng vòng 1 của bàn.
   Ghi lại: cổng vòng 1 đã đỡ được ô nào, còn dòng "vượt trần" nào. Ghi **mã lần chạy** của mốc base và prepared.
1. Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau: `python3 -m lab10.trace --suite S4 --ticket <ID> --seed 11`. Tìm bước sai đầu tiên.
   Ghi từng lỗi vào **bảng soát lỗi** (câu 3.1, Phiếu C mục C2: loại lỗi, nguồn lỗi, hướng xử lý).
2. Đọc khối **kinh doanh và vận hành** và khối **theo kho và hãng** của report: hàng chờ, chi phí mỗi ticket, ROI, tổng hoàn so với trần. Nguyên nhân có thể nằm ở đây chứ không ở code.
3. **Phần riêng của thẻ này** (câu 3.1, Phiếu C mục C3): mở lại pre-mortem bàn đã làm ở vòng 1 (Phiếu B mục B6) và ghi ở Phiếu C mục C1: sự cố trên thẻ có nằm trong các lý do bàn đã viết không? Thuộc lăng kính nào (kỹ thuật, kinh doanh, con người và vận hành, pháp lý)? Thêm lý do còn thiếu bằng bút khác màu. Rồi điền ngay mục **Giờ cao điểm** (Phiếu B mục B7.6, bổ sung bằng bút khác màu): ai trực, mấy người, ngưỡng nào thì gọi thêm người, ngưỡng nào thì thu hẹp hoặc tắt.
4. Một vòng **HAZOP của thẻ** (câu 3.1, Phiếu C mục C4, ≥ 3 dòng; không ghi đè HAZOP vòng 1 ở Phiếu B), viết **specification** và **giả định môi trường** (câu 3.2–3.3, mục C5),
   rồi vẽ **fault tree** (câu 3.4, mục C6): sự kiện đỉnh là tác hại trong tin nhắn; đừng dừng ở nhánh đầu tiên tìm thấy.
5. Sửa NGOÀI model (câu 3.5, mục C7). Ba chỗ được sửa, chọn đúng chỗ cho từng nguyên nhân: `lab10/guards.py` (chặn trước lệnh ghi, chuyển người, trần);
   `config/operating_gates.json` (phạm vi pilot, số người trực, trần tiền, ngân sách mỗi ticket, quy trình kiểm, cổng pháp lý);
   và ít nhất một chỉ số trong `lab10/monitors.py` (câu 3.6, mục C8).
6. Chạy lại: `python3 -m lab10.eval --suite S4 --stage after --note "đổi MỘT thứ: ..."`. Ghi **mã lần chạy** (mục C0).
7. Tự kiểm tra: `python3 -m lab10.grade --incident S4`. Report so ba mốc base · prepared · after. Lệnh này không cho điểm.
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
