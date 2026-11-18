# LAB 10 · Bộ thẻ sự cố (mục lục cả 8 thẻ)

> **Bàn chỉ làm đúng thẻ có số đã bốc từ Lab Coach.** Mở `incidents/Sx/card.md` của số đó (thay `Sx` bằng số của bàn).
> File này gom cả 8 thẻ vào một chỗ để Lab Coach và các bàn cặp dễ đối chiếu lúc demo; đừng đọc trước thẻ của bàn khác.
> Mọi tên người, số điện thoại, hãng vận chuyển, shop, số tiền và mức phạt trong thẻ là dữ liệu giả do người soạn lab đặt ra.

## Cách đọc một thẻ

- **MẶT TRƯỚC** là một tin nhắn hoặc email vận hành. Nó chỉ kể triệu chứng, không nói nguyên nhân.
- **MẶT SAU** có gói bằng chứng (ticket nên dò trước, trường dữ liệu cần xem), ô **Khung tư duy**, nhiệm vụ theo phút, luật,
  sản phẩm nộp và ba dòng bắt buộc.
- Gói dữ liệu của thẻ nằm ở `incidents/Sx/`: `tickets.jsonl` (các ticket có kèm kết quả đúng), `world_patch.json` (đơn hàng,
  phê duyệt, sổ cái có sẵn của sự cố), `card.json` (lệnh chạy và tự kiểm tra). Các file này bị khoá: đừng sửa.
- Tác hại ở mọi thẻ rơi vào **một bên thứ ba cụ thể**: hãng vận chuyển nhỏ, tài xế, shop, người nhận quà, hoặc người đứng tên duyệt.
- Một sự cố thật hiếm khi chỉ có một nguyên nhân. Đừng dừng ở nguyên nhân đầu tiên tìm thấy, và đừng quên những nguyên nhân không
  sửa được bằng code (con số trong `config/operating_gates.json`, số người trực, phạm vi chạy thử).
- Thứ tự phân tích (tác hại → đặc tả phần mềm → giả định về môi trường → biện pháp ngoài model, ghi rõ giảm hay ngăn → cập nhật
  cây nguyên nhân).

## Bảng tổng quan

| Thẻ | Tên | Nguồn tin | Khung tư duy |
|---|---|---|---|
| S1 | Hãng Sông Hồng khiếu nại bị ghi lỗi oan | Email khiếu nại của hãng vận chuyển | Fault tree + HAZOP guideword WRONG / INCOMPLETE; bảng soát lỗi tách ba loại lỗi |
| S2 | Đối soát: shop bị trừ tiền lạ | Tin nhắn của kế toán đối soát trong kênh #doi-soat | HAZOP guideword PERTURBED trên đầu vào, specification vs giả định môi trường + Mức kiểm soát của con người |
| S3 | Hãng miền Tây bị phạt vì bão | Tin nhắn Zalo OA của điều phối Mekong Delta Ship | Concept drift + HAZOP guideword INVALID / INCOMPLETE; mở lại bản đồ dữ liệu của câu 2.3 |
| S4 | Đêm 11.11: ticket gấp ba, hàng chờ duyệt ngập | Tin nhắn của giám sát vận hành trên kênh #van-hanh-tro-ly | Pre-mortem mở rộng sang vận hành và kinh doanh + HAZOP guideword INCAPABLE; runbook vận hành |
| S5 | CFO: mỗi ticket qua trợ lý đang đắt hơn làm tay | Email của Giám đốc tài chính gửi nhóm dự án | Thước đo → Dữ liệu → Cách tính cho một con số kinh doanh + pre-mortem mở rộng sang kinh doanh; phạm vi pilot |
| S6 | Tài xế bị trừ thưởng vì kiện của hãng khác | Tin nhắn thoại được ghi lại từ trưởng nhóm tài xế Sông Hồng | Hình dung của người và của hệ thống + HAZOP guideword WRONG / INCOMPLETE và fault tree |
| S7 | Email pháp chế: lộ số điện thoại người nhận quà | Email của bộ phận Pháp chế | Specification vs giả định môi trường, giảm hay bảo đảm + Hiệu chỉnh lòng tin |
| S8 | Trưởng ca CSKH: chúng tôi không tin trợ lý, đang kiểm tay hết | Tin nhắn của trưởng ca CSKH gửi quản lý | Hiệu chỉnh lòng tin + Mức kiểm soát của con người + HAZOP guideword INVALID |

---

## Thẻ sự cố S1 · Hãng Sông Hồng khiếu nại bị ghi lỗi oan

### MẶT TRƯỚC

*Email khiếu nại của hãng vận chuyển, gửi phòng Đối tác, 16/11/2026 08:12*

> **Từ:** Điều phối, Giao Hàng Sông Hồng (GHSH)
> **Tới:** Phòng Đối tác LogiX-VN · **CC:** chị Oanh (đối soát)
>
> Kính gửi LogiX, bảng lỗi sáng nay ghi Sông Hồng **nhiều lỗi giao trễ chỉ trong một ngày**. Theo hợp đồng, đủ 3 lỗi trong 7 ngày là
> tạm ngưng tuyến, mỗi lỗi phạt 150.000đ. Chúng tôi đối chiếu sổ giao thì không khớp: có đơn chỉ trễ 2 ngày nhưng phiếu ghi 5;
> có đơn tài xế đã giao, có chữ ký người nhận, mà phiếu ghi trễ gần cả tuần; và hôm nay lỗi đổ về dồn dập không ai bên LogiX
> duyệt. Đề nghị rà lại trước 17h, nếu không 12 anh em tài xế nghỉ tuyến từ mai.

*(Thẻ chỉ mô tả triệu chứng. Tìm nguyên nhân là việc của bàn. Đừng dừng ở nguyên nhân đầu tiên tìm thấy.)*

**Thẻ này chỉ dành cho bàn bốc được số S1.** Bàn bốc số khác thì làm thẻ khác. Việc đầu tiên: ghi `Thẻ đã bốc: S1` vào dòng
đầu Phiếu C (`templates/form-c-incident.md`). Mọi lệnh tự kiểm tra của bàn dùng `--incident S1`.

### MẶT SAU

**Gói bằng chứng** (thư mục `incidents/S1/`: `tickets.jsonl` có nhãn, `world_patch.json`)
- Ticket nên dò trước: `S1-01`, `S1-07`, `S1-20`, và cả loạt `S1-40` … `S1-43` (cùng một ngày vận hành).
- Dữ kiện data: `data/world.json` → `carriers` (GHSH: `penalty_per_strike_vnd`, `suspend_after_strikes_7d`), `ops_limits`;
  `incidents/S1/world_patch.json` → xem kỹ các trường của từng `parcel` (`promised_date`, `delivered_date`, `status`).
- Trên trace, để ý sự kiện `tracking`, `model_override`, `proposal`, và số dòng `file_carrier_fault` của cùng một hãng.

> **Khung tư duy: Fault tree + HAZOP guideword WRONG / INCOMPLETE; bảng soát lỗi tách ba loại lỗi**
> - Câu hỏi dẫn dắt: Lỗi này do hệ thống hiểu sai người dùng, do dữ liệu, hay do hệ thống được phép làm quá nhiều? Với lệnh `file_carrier_fault`: nếu giá trị đưa vào là SAI (WRONG) thì sao? Nếu THIẾU (INCOMPLETE) thì sao?
> - Ví dụ cách nghĩ (không phải đáp án của thẻ): WRONG đã gặp ở bộ nền: `T-002@55` (số khách tự khai đè lên tracking). INCOMPLETE: với từng trường của `parcel` trong gói thẻ, hỏi: nếu trường này trống thì độ trễ được tính bằng gì (đọc `lab10/helpers.py`), và ai chịu?
> - Viết vào Phiếu C (`templates/form-c-incident.md`); mục lục ở đầu phiếu.

**Nhiệm vụ** (khối 3 = phút 125–185, rồi v2 ở 185–200: bước 0 phút 125–135 · bước 1–4 phút 135–155, 20 phút phân tích · bước 5–7 phút 155–180, 25 phút sửa và chạy lại · bước 8 phút 180–185 · bước 9 phút 185–200).
Mọi câu trả lời viết vào **Phiếu C** (`templates/form-c-incident.md`), đúng mục ghi trong ngoặc.
0. **Trước khi sửa bất cứ thứ gì** (câu 3.0, Phiếu C mục C0–C1): `python3 -m lab10.grade --incident S1`. Đây là mốc **prepared**: chỉ có cổng vòng 1 của bàn.
   Ghi lại: cổng vòng 1 đã đỡ được ô nào, còn dòng "vượt trần" nào. Ghi **mã lần chạy** của mốc base và prepared.
1. Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau: `python3 -m lab10.trace --suite S1 --ticket <ID> --seed 11`. Tìm bước sai đầu tiên.
   Ghi từng lỗi vào **bảng soát lỗi** (câu 3.1, Phiếu C mục C2: loại lỗi, nguồn lỗi, hướng xử lý).
2. Đọc khối **kinh doanh và vận hành** và khối **theo kho và hãng** của report: hàng chờ, chi phí mỗi ticket, ROI, tổng hoàn so với trần. Nguyên nhân có thể nằm ở đây chứ không ở code.
3. **Phần riêng của thẻ này** (câu 3.1, Phiếu C mục C3): mở lại pre-mortem bàn đã làm ở vòng 1 (Phiếu B mục B6) và ghi ở Phiếu C mục C1: sự cố trên thẻ có nằm trong các lý do bàn đã viết không? Thuộc lăng kính nào (kỹ thuật, kinh doanh, con người và vận hành, pháp lý)? Thêm lý do còn thiếu bằng bút khác màu. Khi điền bảng soát lỗi, mở lại bản đồ dữ liệu của câu 2.3 (ghi ở mục C3.5): với từng trường của `parcel`, bàn đã coi nó là nguồn sự thật hay chưa hỏi?
4. Một vòng **HAZOP của thẻ** (câu 3.1, Phiếu C mục C4, ≥ 3 dòng; không ghi đè HAZOP vòng 1 ở Phiếu B), viết **specification** và **giả định môi trường** (câu 3.2–3.3, mục C5),
   rồi vẽ **fault tree** (câu 3.4, mục C6): sự kiện đỉnh là tác hại trong tin nhắn; đừng dừng ở nhánh đầu tiên tìm thấy.
5. Sửa NGOÀI model (câu 3.5, mục C7). Ba chỗ được sửa, chọn đúng chỗ cho từng nguyên nhân: `lab10/guards.py` (chặn trước lệnh ghi, chuyển người, trần);
   `config/operating_gates.json` (phạm vi pilot, số người trực, trần tiền, ngân sách mỗi ticket, quy trình kiểm, cổng pháp lý);
   và ít nhất một chỉ số trong `lab10/monitors.py` (câu 3.6, mục C8).
6. Chạy lại: `python3 -m lab10.eval --suite S1 --stage after --note "đổi MỘT thứ: ..."`. Ghi **mã lần chạy** (mục C0).
7. Tự kiểm tra: `python3 -m lab10.grade --incident S1`. Report so ba mốc base · prepared · after. Lệnh này không cho điểm.
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

---

## Thẻ sự cố S2 · Đối soát: shop bị trừ tiền lạ

### MẶT TRƯỚC

*Tin nhắn của kế toán đối soát trong kênh #doi-soat, 16/11/2026 10:05*

> **Phạm Kiều Oanh (kế toán đối soát):** Cả nhà ơi, bảng đối soát shop tuần này có mấy dòng **trừ tiền shop** cho yêu cầu
> *giao trễ*, trong khi giao trễ thì LogiX chịu phí chứ. Gốm Bát Tràng Cô Lụa bị trừ **475.000đ** cho một đơn chỉ trễ 4 ngày,
> thêm một khoản **3.230.000đ** không có mã phê duyệt nào. Cô Lụa gọi em hai lần rồi. Có đơn em đọc ticket thấy khách viết
> rất bình thường mà vẫn bị trừ cả đơn. Ngoài ra có một khách nhận 5 khoản hoàn tự động trong cùng một ngày, cộng lại
> vượt mức mà Ops từng thống nhất. Ai kiểm giúp em trước kỳ chốt 16h.

*(Thẻ chỉ mô tả triệu chứng. Tìm nguyên nhân là việc của bàn. Đừng dừng ở nguyên nhân đầu tiên tìm thấy.)*

**Thẻ này chỉ dành cho bàn bốc được số S2.** Bàn bốc số khác thì làm thẻ khác. Việc đầu tiên: ghi `Thẻ đã bốc: S2` vào dòng
đầu Phiếu C (`templates/form-c-incident.md`). Mọi lệnh tự kiểm tra của bàn dùng `--incident S2`.

### MẶT SAU

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

---

## Thẻ sự cố S3 · Hãng miền Tây bị phạt vì bão

### MẶT TRƯỚC

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

### MẶT SAU

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

---

## Thẻ sự cố S4 · Đêm 11.11: ticket gấp ba, hàng chờ duyệt ngập

### MẶT TRƯỚC

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

### MẶT SAU

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

---

## Thẻ sự cố S5 · CFO: mỗi ticket qua trợ lý đang đắt hơn làm tay

### MẶT TRƯỚC

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

### MẶT SAU

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

---

## Thẻ sự cố S6 · Tài xế bị trừ thưởng vì kiện của hãng khác

### MẶT TRƯỚC

*Tin nhắn thoại được ghi lại từ trưởng nhóm tài xế Sông Hồng, chuyển tiếp qua phòng Đối tác, 16/11/2026 14:20*

> “Chị ơi, anh em bên em tháng này bị trừ thưởng chuyên cần vì mấy lỗi giao trễ, mà kiện bên em giao **đúng hẹn** hết. Em tra
> ra thì toàn đơn tách kiện: kiện của Sông Hồng tới trước, kiện kia hãng khác chở tới sau mấy ngày, nhưng lỗi lại ghi
> cho bên em. Có đơn hai hãng cùng trễ, khách chẳng nói rõ kiện nào, hệ thống cũng tự chọn bên em. Hôm nay còn bị
> ghi một lèo mấy lỗi liền. Bên chị xem giúp chứ hãng nhỏ như em chịu không nổi.”

*(Thẻ chỉ mô tả triệu chứng. Tìm nguyên nhân là việc của bàn. Đừng dừng ở nguyên nhân đầu tiên tìm thấy.)*

**Thẻ này chỉ dành cho bàn bốc được số S6.** Bàn bốc số khác thì làm thẻ khác. Việc đầu tiên: ghi `Thẻ đã bốc: S6` vào dòng
đầu Phiếu C (`templates/form-c-incident.md`). Mọi lệnh tự kiểm tra của bàn dùng `--incident S6`.

### MẶT SAU

**Gói bằng chứng** (thư mục `incidents/S6/`: `tickets.jsonl` có nhãn, `world_patch.json`)
- Ticket nên dò trước: `S6-01`, `S6-04`, `S6-20`, `S6-21`, và loạt `S6-40` … `S6-43`.
- Dữ kiện data: `incidents/S6/world_patch.json` → mỗi đơn có danh sách `parcels`, mỗi kiện có `carrier_id`, `driver_id` riêng;
  ticket có thể có hoặc không có `parcel_id`.
- Trên trace, so sự kiện `tracking.parcels` (kiện nào trễ) với dòng `file_carrier_fault` (ghi cho kiện nào, hãng nào).

> **Khung tư duy: Hình dung của người và của hệ thống + HAZOP guideword WRONG / INCOMPLETE và fault tree**
> - Câu hỏi dẫn dắt: Hệ thống đang mang mô hình nào về “một đơn hàng”? Mô hình đó sai ở đâu so với thực tế vận hành? Khi đầu vào không đủ để biết ai có lỗi, hành động an toàn là gì, và phải dừng TRƯỚC bước nào?
> - Ví dụ cách nghĩ (không phải đáp án của thẻ): Ví dụ ngoài thẻ: bảng công tính theo ngày, người làm thì tính theo ca, nên ai làm hai ca chỉ được trả một. Đi tìm chỗ “đơn vị” của người trong nghề và của hệ thống khác nhau, rồi hỏi: khi đầu vào không đủ, hệ thống được phép đoán không?
> - Viết vào Phiếu C (`templates/form-c-incident.md`); mục lục ở đầu phiếu.

**Nhiệm vụ** (khối 3 = phút 125–185, rồi v2 ở 185–200: bước 0 phút 125–135 · bước 1–4 phút 135–155, 20 phút phân tích · bước 5–7 phút 155–180, 25 phút sửa và chạy lại · bước 8 phút 180–185 · bước 9 phút 185–200).
Mọi câu trả lời viết vào **Phiếu C** (`templates/form-c-incident.md`), đúng mục ghi trong ngoặc.
0. **Trước khi sửa bất cứ thứ gì** (câu 3.0, Phiếu C mục C0–C1): `python3 -m lab10.grade --incident S6`. Đây là mốc **prepared**: chỉ có cổng vòng 1 của bàn.
   Ghi lại: cổng vòng 1 đã đỡ được ô nào, còn dòng "vượt trần" nào. Ghi **mã lần chạy** của mốc base và prepared.
1. Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau: `python3 -m lab10.trace --suite S6 --ticket <ID> --seed 11`. Tìm bước sai đầu tiên.
   Ghi từng lỗi vào **bảng soát lỗi** (câu 3.1, Phiếu C mục C2: loại lỗi, nguồn lỗi, hướng xử lý).
2. Đọc khối **kinh doanh và vận hành** và khối **theo kho và hãng** của report: hàng chờ, chi phí mỗi ticket, ROI, tổng hoàn so với trần. Nguyên nhân có thể nằm ở đây chứ không ở code.
3. **Phần riêng của thẻ này** (câu 3.1, Phiếu C mục C3): mục **C3.2 Hình dung của người và của hệ thống** (thay pre-mortem): điền cho hai nhóm người (gợi ý: điều phối hãng, kế toán đối soát) cách họ xác định ai chịu lỗi, rồi đọc trace để ghi hình dung của hệ thống và chỗ vênh.
4. Một vòng **HAZOP của thẻ** (câu 3.1, Phiếu C mục C4, ≥ 3 dòng; không ghi đè HAZOP vòng 1 ở Phiếu B), viết **specification** và **giả định môi trường** (câu 3.2–3.3, mục C5),
   rồi vẽ **fault tree** (câu 3.4, mục C6): sự kiện đỉnh là tác hại trong tin nhắn; đừng dừng ở nhánh đầu tiên tìm thấy.
5. Sửa NGOÀI model (câu 3.5, mục C7). Ba chỗ được sửa, chọn đúng chỗ cho từng nguyên nhân: `lab10/guards.py` (chặn trước lệnh ghi, chuyển người, trần);
   `config/operating_gates.json` (phạm vi pilot, số người trực, trần tiền, ngân sách mỗi ticket, quy trình kiểm, cổng pháp lý);
   và ít nhất một chỉ số trong `lab10/monitors.py` (câu 3.6, mục C8).
6. Chạy lại: `python3 -m lab10.eval --suite S6 --stage after --note "đổi MỘT thứ: ..."`. Ghi **mã lần chạy** (mục C0).
7. Tự kiểm tra: `python3 -m lab10.grade --incident S6`. Report so ba mốc base · prepared · after. Lệnh này không cho điểm.
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

---

## Thẻ sự cố S7 · Email pháp chế: lộ số điện thoại người nhận quà

### MẶT TRƯỚC

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

### MẶT SAU

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

---

## Thẻ sự cố S8 · Trưởng ca CSKH: chúng tôi không tin trợ lý, đang kiểm tay hết

### MẶT TRƯỚC

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

### MẶT SAU

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
