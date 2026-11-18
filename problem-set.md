# LAB 10 · From PoC to Pilot (Gate 1) · Đề xuyên suốt: hồ sơ Gate 1 cho trợ lý hoàn tiền LogiX-VN

> **Không chấm điểm tại lớp.** Bài được một team chấm tự động chấm sau buổi học. Trong buổi, lệnh `lab10.grade` chỉ để bàn
> **tự kiểm tra**; Lab Coach hỗ trợ và hỏi soi lúc demo, không cho điểm. Bàn nộp thư mục `submission/` (xem phần D).
>
> **Viết câu trả lời ở đâu.** Mỗi câu dưới đây có một ô trả lời mang đúng số câu trong một trong ba phiếu ở `templates/`:
> **Phiếu A** `form-a-criteria.md` (khối 1), **Phiếu B** `form-b-evaluation-gates.md` (khối 2 và quyết định v1),
> **Phiếu C** `form-c-incident.md` (khối 3 và quyết định v2). Cột "Viết vào" chỉ đúng mục.

## Hai vòng, ba mốc

| Vòng | Bàn làm gì | Mốc để so sánh |
|---|---|---|
| **Vòng 1** (phút 15–115), chưa biết sự cố | Mục tiêu và thước đo → viết Bản tiêu chí → **ký tiêu chí TRƯỚC khi chạy đánh giá lần nào** (phút 60–65) → đo mốc base → pre-mortem, HAZOP, checklist 9 nhóm việc → **code 2–3 cổng phòng ngừa** và đặt cổng kinh doanh, vận hành, pháp lý → **chốt cổng vòng 1** → quyết định **v1** | **base**: chưa có cổng nào |
| **Vòng 2** (phút 125–200), sau khi nhận thẻ (`git pull --no-rebase --no-edit --allow-unrelated-histories -X ours upstream main`) và bốc thẻ | **Chạy tự kiểm tra trước, chỉ với cổng vòng 1** → phân tích → sửa → quyết định **v2** | **prepared**: chỉ có cổng vòng 1 · **after**: sau khi sửa |

Demo cuối buổi so sánh ba mốc **base · prepared · after**: cổng bàn chuẩn bị trước đỡ được gì, phần nào phải sửa sau.

## Thời gian

| Phần | Phút trên đồng hồ lab | Thời lượng | Phiếu |
|---|---|---|---|
| Mở đầu, cài đặt, chia vai | 0–15 | 15' | (`TEAM.md`: bảng thành viên) |
| Khối 1 · Mục tiêu và đo lường (viết xong Bản tiêu chí) | 15–60 | 45' | A |
| **Ký tiêu chí** (trước khi chạy đánh giá lần nào) | 60–65 | 5' | A mục A5 |
| Khối 2A · Tìm rủi ro trước khi nó xảy ra | 65–85 | 20' | B |
| Khối 2B · Cổng phòng ngừa | 85–105 | 20' | B |
| Chốt cổng vòng 1 · quyết định v1 | 105–115 | 10' | B mục B8 |
| Nghỉ | 115–125 | 10' | |
| Khối 3 · Sự cố (nhận thẻ từ repo mẫu, bốc thẻ, mốc prepared, phân tích, sửa) | 125–185 | 60' | C |
| Quyết định v2 · runbook · gom bài nộp | 185–200 | 15' | C mục C11–C12 |
| Demo ba mốc | 200–230 | 30' | |
| Tổng kết, đẩy bài lần cuối | 230–240 | 10' | |

## Ba vai trong bàn (3–4 người; vai nào cũng có việc ở cả hai vòng)

| Vai | Cầm bút ở vòng 1 | Cầm bút ở vòng 2 | File chính |
|---|---|---|---|
| **Kỹ sư cổng** (1–2 người) | Chạy mốc base, dò trace, behavioral test, code 2–3 cổng phòng ngừa | Dò trace sự cố, sửa cổng, thêm chỉ số theo dõi, chạy ba mốc | `lab10/guards.py`, `lab10/monitors.py` |
| **Sản phẩm và kinh doanh** (1 người) | Mục tiêu, thước đo, bản đồ dữ liệu, lăng kính kinh doanh của pre-mortem, cổng `business`, tiêu chí để ký | Đọc chi phí mỗi ticket, ROI, trần tiền; quyết định phạm vi pilot; viết quyết định v2 | `config/acceptance_criteria.json`, `config/operating_gates.json` mục `business`, Phiếu A, Phiếu B mục B8, Phiếu C mục C12 |
| **Vận hành và pháp lý** (1 người) | HAZOP mở rộng, checklist 9 nhóm việc có PIC, cổng `operations` và `legal`, runbook phần 1–3 và giờ cao điểm | Đọc hàng chờ người duyệt, số người trực, bên thứ ba bị ảnh hưởng; runbook phần 4–5; gom bài nộp | `config/operating_gates.json` mục `operations` và `legal`, Phiếu B mục B4–B5 và B7.5–B7.6, Phiếu C mục C11, `submission/` |

Mọi quyết định (v1, v2) do cả bàn chốt. Người không viết code vẫn đọc trace cùng Kỹ sư cổng và chỉ ra ticket nào còn hỏng.

---

# PHẦN A · VÒNG 1 (phát đầu buổi)

## Tình huống

LogiX-VN đã chạy PoC trợ lý xử lý yêu cầu hoàn tiền giao trễ. Trợ lý đọc ticket, tra đơn và tracking, áp chính sách hoàn tiền, ghi sổ cái, ghi lỗi cho hãng vận chuyển chịu trách nhiệm, báo cho hãng và trả lời khách. Bàn của bạn là nhóm chuẩn bị **hồ sơ Bước đánh giá 1** (trong bài giảng gọi là **Gate 1**; hai tên chỉ cùng một bước): có đáng chạy thử với người dùng thật ở 2 depot không.

Bạn có: eval card và PRD v1.1 từ Lab 9; codebase Day 10 với bộ nền 22 ticket × 5 seed; MockLLM tất định nên mọi lần chạy tái lập được. Mỗi lần chạy còn cho các con số kinh doanh và vận hành: tỉ lệ chuyển người duyệt, thời gian chờ người duyệt, số ca bị ùn, chi phí mỗi ticket so với làm tay, ROI, tổng tiền hoàn so với trần, và một khối **theo kho và hãng**.

Câu trả lời phải bám tình huống LogiX và dữ kiện trong code. Trả lời chung chung không đạt.

Checklist chín nhóm việc go-live (Phiếu B mục B5) là danh sách việc phải xong trước khi chạy thử thật. Bàn điền lần đầu ở khối 2A.

## Khối 1 · Mục tiêu và đo lường (45 phút, phút 15–60), rồi ký (phút 60–65)

**Đặt luật trước, xem số sau.** Trong khối này bàn **chưa chạy trợ lý lần nào**. Bàn viết xong Bản tiêu chí rồi ký ở phút 60–65; chỉ sau khi ký mới được chạy `lab10.eval`. Nếu chạy sớm, lệnh sẽ từ chối và nhắc bàn ký trước. Câu 1.5 cho sẵn một kết quả để tập đọc khoảng tin cậy; đó không phải lần chạy của bàn.

> **Khung tư duy: Thước đo → Dữ liệu → Cách tính (câu 1.3–1.4); câu tiêu chí thành công có hành động đi kèm (câu 1.6)**
> - Câu hỏi dẫn dắt: thành công nhìn từ ai? Con số nào, tính thế nào, để hai người độc lập ra cùng kết quả? Điều gì phải viết ra trước khi xem bằng chứng?
> - Ví dụ mẫu: trong Phiếu A mục A2 và A4.

| Câu | Nội dung | Phút | Vai cầm bút | Viết vào |
|---|---|---|---|---|
| **1.1** | Nêu **một mục tiêu cấp hệ thống** của trợ lý (không cần thước đo). Phải khác "model trả lời đúng". Dựa vào PRD v1.1 §3 | 2 | Sản phẩm và kinh doanh | Phiếu A, mục A1 · Câu 1.1 |
| **1.2** | Nêu **một mục tiêu nhìn từ chị Oanh, kế toán đối soát** (người không dùng trợ lý nhưng phải khớp sổ với hãng và shop mỗi tuần), và **một mục tiêu nhìn từ chị Hạnh, trưởng ca CSKH** (người phải duyệt những ca trợ lý chuyển sang). Dựa vào PRD v1.1 §2, §6; `data/world.json` → `staff` | 3 | Vận hành và pháp lý | Phiếu A, mục A1 · Câu 1.2 |
| **1.3** | Chọn **MỘT bước** của agent (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Thiết kế **một offline metric** cho riêng bước đó: Thước đo · Dữ liệu (lấy gì, ở đâu, ai gán nhãn) · Cách tính | 10 | Kỹ sư cổng | Phiếu A, mục A2, cột "Offline" |
| **1.4** | Thiết kế **telemetry production** để biết trợ lý có đang gây thiệt hại cho bên ngoài LogiX không. Cùng ba ô, thêm **khung thời gian** và **ngưỡng báo động**. Không có nhãn trong production | 5 | Vận hành và pháp lý | Phiếu A, mục A2, cột "Telemetry production" |
| **1.5** | Đọc kết quả sau rồi chọn MỘT kết luận đúng và giải thích một câu. **Các số dưới đây là số minh hoạ**, không phải số của bộ nền lab (bàn sẽ tự đo số thật ở câu 2.1, sau khi đã ký): bản X có pass_rate 0,9800 (49/50 lần chạy), khoảng tin cậy 95% [0,9400; 1,0]. Bản Y có pass_rate 1,0 (50/50). (a) Y tốt hơn X có ý nghĩa thống kê. (b) Chưa đủ căn cứ nói Y tốt hơn X; chênh 1 lần chạy nằm trong khoảng tin cậy của X. (c) X và Y chắc chắn như nhau. (d) Phải chạy thêm seed thì X mới đạt | 3 | Cả bàn | Phiếu A, mục A3 · Câu 1.5 |
| **1.6** | **Viết Bản tiêu chí**: (a) viết mỗi chỉ số bắt buộc thành một câu "Nếu … thì chúng tôi sẽ …"; (b) soát bốn câu hỏi (có ý nghĩa với mọi bên? ai thiệt? ngày 1? ngày 1.000?); (c) chép ngưỡng và hành động vào `config/acceptance_criteria.json`: 5 ngưỡng bắt buộc, 1 nên có, **nhóm `business_ops`** (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa), điều kiện dừng, `decision_rule` cho cả bốn quyết định; (d) viết thêm hai câu ranh giới đầu ra (**không thêm trường JSON**): một đầu ra hoặc hành động bị cấm, và một ngưỡng chuyển cho người duyệt. **Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`. Xem cách viết ở `config/acceptance_criteria.example.json` (đừng chép ngưỡng). **Viết xong thì ký ngay ở phút 60–65, trước khi chạy đánh giá lần nào** | 20 | Sản phẩm và kinh doanh | Phiếu A, mục A4 · Câu 1.6 (cả phần "Ranh giới đầu ra") |

Ghi chú 1.5: các số 0,9800, [0,9400; 1,0] và 50 lần chạy là **số minh hoạ**, tính khoảng tin cậy cùng cách lệnh `lab10.eval` dùng (bootstrap 1.000 mẫu). Chúng cố ý khác số thật của mốc base trên bộ nền. Bàn sẽ tự chạy và đọc số thật ở câu 2.1, sau khi đã ký.

### Ký tiêu chí (5 phút, phút 60–65) · Phiếu A, mục A5

1. Soát lại `config/acceptance_criteria.json` lần cuối: tên bàn, đủ ngưỡng, `decision_rule`, điều kiện dừng.
2. Chạy `python3 -m lab10.criteria sign`.
3. **Ngay sau đó, trước lần đánh giá đầu tiên**, chạy đúng lệnh máy in ra:
   `git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main`
4. Từ lúc này **không sửa tiêu chí**. Mọi báo cáo về sau đều in hash; file đổi sau commit ký thì bài không được tính.

Bàn chưa chạy đánh giá lần nào cho tới bước này. Đó là chủ ý: ngưỡng phải được viết khi chưa ai biết trợ lý đạt hay trượt.

## Khối 2A · Tìm rủi ro trước khi nó xảy ra (20 phút, phút 65–85)

> **Khung tư duy: pre-mortem bốn lăng kính (kỹ thuật, kinh doanh, con người và vận hành, pháp lý); HAZOP mở rộng ra ngoài code; bản đồ dữ liệu (câu 2.3) và bảng soát lỗi (câu 2.2)**
> - Câu hỏi dẫn dắt: ba tháng sau pilot phải tắt trợ lý, vì sao? Thứ gì hết trước khi lượng việc tăng gấp ba: máy, tiền, hay người? Dữ liệu của ai rời hệ thống mà họ không biết?
> - Ví dụ mẫu: bảng "Mở rộng ra ngoài kỹ thuật" trong Phiếu B mục B4.

Ba vai làm song song 10 phút đầu, rồi cả bàn làm pre-mortem 10 phút.

| Câu | Nội dung | Phút | Vai cầm bút | Viết vào |
|---|---|---|---|---|
| **2.1** | **Lần chạy đánh giá đầu tiên của bàn (tiêu chí đã ký).** Chạy mốc **base**: `python3 -m lab10.eval --suite base --stage base --note "baseline"`, rồi `python3 -m lab10.gate --run runs/<mã>/report.json`. Ghi **mã lần chạy**. Đọc cả khối "kinh doanh và vận hành" và khối "theo kho và hãng" ở cuối. Nêu lý lẽ chính ủng hộ và phản đối việc để cổng so tiêu chí này **tự chặn** một bản phát hành (so với để người duyệt), rồi khoanh khuyến nghị: tự chặn / người duyệt / kết hợp | 6 | Kỹ sư cổng | Phiếu B, mục B1 (và dòng 1 của B0) |
| **2.2** | Dò `python3 -m lab10.trace --suite base --ticket T-002 --seed 55`. **Điền bảng soát lỗi cho lỗi này** (ghi lỗi + loại lỗi, tìm nguồn, hướng xử lý) | 4 | Kỹ sư cổng | Phiếu B, mục B2 |
| **2.3** | **Điền bản đồ dữ liệu** (trường then chốt, nguồn sự thật hay bản sao, thế giới thật làm lệch ở đâu). Rút ra **một ví dụ drift cụ thể** trong 3 tháng tới: cái gì đổi, đổi ngày nào, trường nào cho thấy, con số nào của Bản tiêu chí bị ảnh hưởng. Đây là đầu vào đổi hay quan hệ vào–ra đổi? Chỉ số nào sẽ phát hiện? Gợi ý: mở `data/world.json` phần `policies`, `orders[].parcels`, `ops_limits`, `ops_facts` | 10 | Sản phẩm và kinh doanh | Phiếu B, mục B3 |
| **2.4** | **HAZOP mở rộng**: một vòng trên một tool ghi (≥ 3 dòng), cộng **ít nhất hai dòng ngoài kỹ thuật** (người duyệt, ngân sách, phạm vi pilot, dữ liệu gửi bên thứ ba). Rồi điền **checklist 9 nhóm việc lần 1**: trạng thái, bằng chứng, và **PIC có tên** cho từng dòng | 10 | Vận hành và pháp lý | Phiếu B, mục B4 (HAZOP vòng 1) và B5 (checklist) |
| **2.5** | **Pre-mortem bốn lăng kính**: cả bàn, 8–10 phút. Lăng kính nào trống thì viết thêm. Chọn **2–3 lý do** sẽ thành cổng phòng ngừa ngay hôm nay | 10 | Cả bàn | Phiếu B, mục B6 |

## Khối 2B · Cổng phòng ngừa (20 phút, phút 85–105)

> **Khung tư duy: biện pháp cấp hệ thống nằm ngoài model và prompt; rò rỉ dữ liệu; behavioral test**
> - Câu hỏi dẫn dắt: cổng này chặn trước lệnh ghi nào? Nó dựa vào nguồn sự thật nào? Nó có làm hỏng ticket đang đúng không? Con số nào không cần code, chỉ cần một người có thẩm quyền quyết?

| Câu | Nội dung | Phút | Vai cầm bút | Viết vào |
|---|---|---|---|---|
| **2.6** | **Code 2–3 cổng phòng ngừa** trong `lab10/guards.py` (hàm `pre_guard(ctx)` hoặc `write_gate(ctx, action)`), mỗi cổng ứng với một lý do của pre-mortem hoặc một dòng HAZOP. Chạy `python3 -m lab10.eval --suite base --stage after --note "cổng vòng 1: ..."` và `python3 -m unittest discover -s tests`. Cổng không được làm hỏng ticket đang đúng của bộ nền. Hướng dẫn ở đầu `lab10/guards.py`, hàm tra cứu trong `lab10/helpers.py`, ví dụ trong `docs/guide.md` (Phụ lục C) | 16 | Kỹ sư cổng | Phiếu B, mục B7.1 |
| **2.7** | Bàn đang chỉnh cổng cho tới khi 22 ticket của bộ nền xanh hết. Nêu **2 bước cụ thể** để tránh rò rỉ dữ liệu (chỉnh trên chính bộ dùng để chấm). Gắn với thứ có thật trong lab: bộ nền, gói sự cố, bài kiểm tra ẩn | 3 | Kỹ sư cổng | Phiếu B, mục B7.2 |
| **2.8** | Viết **một behavioral test**: phát biểu tính chất (một câu), rồi viết **2 ticket mới** kiểm tính chất đó và chạy bằng `python3 -m lab10.trace --suite base --stage after --adhoc "..." --order O-10xx --customer C-xx`. Dán kết quả. Giữ 2 ticket này làm "ticket hiểm" cho phần demo | 7 | Kỹ sư cổng cùng một người không viết code | Phiếu B, mục B7.3 |
| **2.9** | **Đặt cổng kinh doanh** trong `config/operating_gates.json` mục `business`: trần tiền hoàn tự động mỗi ngày, ngân sách chi phí mỗi ticket, phạm vi pilot (tất cả / kho nào / bao nhiêu phần trăm), ngưỡng ROI. Mỗi con số kèm một câu lý do, lấy từ `data/world.json` → `ops_limits`, `ops_facts`. Nghĩa từng khoá: `docs/guide.md`, mục "Cổng trong config" | 10 | Sản phẩm và kinh doanh | Phiếu B, mục B7.4 |
| **2.10** | **Đặt cổng con người, vận hành, pháp lý** trong `config/operating_gates.json` mục `operations` và `legal`: PIC, người duyệt, số người trực mỗi ca, công suất duyệt mỗi giờ, thời gian chờ tối đa, điều kiện dừng, kênh báo tin; trường dữ liệu cá nhân không gửi cho bên thứ ba; ghi lỗi cho hãng phải có nguyên nhân trong tracking. Viết **runbook phần 1–3** khớp với các con số đó, kể cả dòng thời hạn dừng (từ tín hiệu đỏ đến lúc dừng xong tối đa bao nhiêu phút và ai bấm), và mục **Giờ cao điểm** (ai trực, mấy người, ngưỡng gọi thêm người, ngưỡng thu hẹp hoặc tắt) | 16 | Vận hành và pháp lý | Phiếu B, mục B7.5 (runbook 1–3) và B7.6 (giờ cao điểm) |

## Chốt · quyết định v1 (10 phút, phút 105–115) · Phiếu B, mục B8

Tiêu chí đã ký từ phút 60–65; ở đây không ký nữa. Làm đúng thứ tự:

1. **Chốt cổng vòng 1:** `python3 -m lab10.checkpoint`. Lệnh chụp lại `lab10/guards.py` và `config/operating_gates.json` thành mốc **prepared**. Sau khi chốt, bàn vẫn sửa tiếp hai file gốc ở vòng 2; không sửa hai bản chụp.
2. **Quyết định v1:** chạy bộ nền ở mốc prepared (`python3 -m lab10.eval --suite base --stage prepared`), so với tiêu chí đã ký (`python3 -m lab10.gate --run runs/<mã>/report.json`), rồi điền cột **v1** ở Phiếu B mục B8: một trong bốn quyết định, ba dòng bằng chứng có mã lần chạy, dòng `decision_rule` tương ứng, ngày quyết định lại.
3. Commit và push (lệnh ở cuối Phiếu B mục B8). Sau mốc này v1 không sửa được.

> **Khung tư duy: ba câu tự vấn trước khi quyết** · Rủi ro còn lại chấp nhận được như hiện trạng? Cần thêm biện pháp nào, tốn bao lâu? Có phần nào không nên làm tiếp?

---

# PHẦN B · VÒNG 2 · SỰ CỐ (khối 3) · thẻ tới ở phút 125

## Cách tung

- Phút 125: Lab Coach báo "đã phát thẻ" (thẻ được đẩy lên **repo mẫu**, không phải repo của từng bàn). Mỗi bàn chạy `git pull --no-rebase --no-edit --allow-unrelated-histories -X ours upstream main` để tải về thư mục `incidents/S1…S8/` và file `incident-cards.md` (trước mốc này repo của bàn chưa có hai thứ đó). Các cờ `--allow-unrelated-histories -X ours` giữ nguyên bài của bàn và chỉ lấy thêm thẻ. Nếu chưa gắn `upstream`, xem README mục 2. Mỗi **cặp bàn** cử một người lên **bốc số** (S1–S8). Bàn **chỉ làm đúng thẻ có số bốc được**: `incidents/Sx/card.md`.
- Ghi số đã bốc vào dòng `Thẻ đã bốc:` ở đầu Phiếu C (`templates/form-c-incident.md`).
- **Việc đầu tiên, trước khi sửa bất cứ thứ gì:** `python3 -m lab10.grade --incident Sx` (câu 3.0, bước 0 trên thẻ).
- Lab Coach đọc một câu: *"Đây là tin nhắn bàn nhận được sáng nay. Bản tiêu chí đã ký giữ nguyên. Sau 60 phút, bàn cho tôi biết quyết định Gate 1 còn đứng được không."*
- **Thẻ sự cố chính là khối 3.** Tám thẻ, mỗi thẻ một tác hại cho một bên cụ thể. Năm thẻ có nguyên nhân chính ở kỹ thuật; ba thẻ có nguyên nhân chính ở **kinh doanh hoặc con người** (lượng việc tăng làm hàng chờ ngập, chi phí mỗi ticket cao hơn làm tay, nhân viên không tin trợ lý). Ở các thẻ đó, cách sửa nằm nhiều ở phạm vi, nhân sự, giải thích, quy trình hơn là ở code.

## Khối 3 · Một tác hại cụ thể, nhiều nguyên nhân (60 phút, phút 125–185)

> **Khung tư duy: phân tích hazard (HAZOP) → fault tree → specification và giả định môi trường → biện pháp ngoài model, giảm hay bảo đảm → cập nhật fault tree**
> - Câu hỏi dẫn dắt: tác hại cho ai, đo bằng gì? Ngoài model còn nhánh nào dẫn tới nó: dữ liệu, quyền hạn, tiền, người? Cổng đặt ở tầng nào: phát hiện, chặn, giới hạn thiệt hại, hay vận hành? Nó giảm khả năng hay ngăn hẳn?
> - Ví dụ mẫu: ô Khung tư duy riêng trên từng thẻ; ví dụ fault tree ở Phiếu C mục C6.

| Câu | Bước trên thẻ | Nội dung | Phút | Vai cầm bút | Viết vào |
|---|---|---|---|---|---|
| **3.0** | 0 | **Mốc prepared** (phút 125–135, gồm cả nhận thẻ và bốc số). Chạy `python3 -m lab10.grade --incident Sx` khi chưa sửa gì. Ghi: cổng vòng 1 đỡ được ô nào; khối kinh doanh và vận hành có dòng nào vượt trần; sự cố này có nằm trong pre-mortem của bàn không | 10 | Cả bàn | Phiếu C, mục C1 (và C0) |
| **3.1** | 1–4 | **Phân tích hazard** (phút 135–155 cho câu 3.1–3.4). Dò ≥ 2 ticket hỏng theo kiểu khác nhau (`python3 -m lab10.trace --suite Sx --ticket <ID> --seed 11`). Điền **bảng soát lỗi** (≥ 2 lỗi có nguồn khác nhau, ≥ 1 lỗi chìm). Làm **phần riêng của thẻ**. Viết **HAZOP của thẻ** (≥ 3 dòng, mục riêng, không ghi đè HAZOP vòng 1). Nêu tác hại: cho ai, đo bằng gì, bao nhiêu ở mốc base | 8 | Kỹ sư cổng (trace) · Vận hành và pháp lý (phần riêng) | Phiếu C, mục C2 (soát lỗi, tác hại), C3 (phần riêng theo thẻ), C4 (HAZOP của thẻ) |
| **3.2** | 4 | Viết **một specification** mà nếu bị vi phạm thì gây ra tác hại trên thẻ. Kiểm được bằng code hoặc bằng một con số trong report | 3 | Sản phẩm và kinh doanh | Phiếu C, mục C5 · Câu 3.2 |
| **3.3** | 4 | Nêu **một giả định về môi trường** mà người thiết kế đã ngầm tin, nhưng nhiều khả năng sai ngoài thực tế | 3 | Vận hành và pháp lý | Phiếu C, mục C5 · Câu 3.3 |
| **3.4** | 4 | Vẽ **fault tree trước khi sửa**: sự kiện đỉnh là tác hại; ít nhất hai nhánh ở hai tầng khác nhau (kỹ thuật, kinh doanh, con người); mỗi lá có bằng chứng (ticket@seed, trường dữ liệu, hoặc một dòng của report) | 6 | Cả bàn | Phiếu C, mục C6 |
| **3.5** | 5–7 | **Sửa, đúng chỗ cho từng nguyên nhân** (phút 155–180). Code: `lab10/guards.py`. Con số và quy trình: `config/operating_gates.json` (phạm vi, người trực, trần, ngân sách, kiểm mẫu, ghi chú giải thích, cổng pháp lý). Chạy `python3 -m lab10.eval --suite Sx --stage after --note "…"`, rồi `python3 -m lab10.grade --incident Sx`. Ghi rõ từng biện pháp **giảm khả năng** hay **ngăn hẳn** | 25 | Kỹ sư cổng (code) · Sản phẩm và kinh doanh (`business`) · Vận hành và pháp lý (`operations`, `legal`) | Phiếu C, mục C7 |
| **3.6** | 5 | Thêm **chỉ số theo dõi** trong `lab10/monitors.py` (một hàm mới, đăng ký vào `MONITORS`) bắt được sự cố (kỹ thuật, vận hành, hay kinh doanh đều được). Viết đủ ba ô thước đo → dữ liệu → cách tính | (trong 3.5) | Kỹ sư cổng | Phiếu C, mục C8 |
| **3.7** | 8 | **Cập nhật fault tree** sau khi sửa (cổng nằm ở nhánh nào, tầng nào, nhánh nào còn hở). Thêm ≥ 1 dòng Risk register. Cập nhật checklist 9 nhóm việc (cột PIC). Viết **runbook phần 4–5** (phút 180–185; runbook có thể xong trong 185–200) | 5 | Vận hành và pháp lý | Phiếu C, mục C9 (fault tree sau), C10 (risk register), C11 (checklist, runbook 4–5) |

**Report tự kiểm tra cho bàn biết gì.** Sáu mục kiểm (file khoá, tiêu chí, gói sự cố, bài kiểm tra ẩn, bộ nền, chỉ số theo dõi); bảng **kinh doanh · vận hành · pháp lý** ở ba mốc (thời gian chờ, số ca ùn, tỉ lệ chuyển người duyệt, chi phí mỗi ticket, ROI, tổng tiền hoàn so với trần, lộ dữ liệu cá nhân, lỗi oan cho hãng); bảng **theo kho và hãng**; và một dòng kết: **được phép cân nhắc "Tiếp tục"** hay **không đủ căn cứ**. Bài kiểm tra ẩn (đơn khác, khách khác, cách viết khác) do team chấm chạy sau buổi học.

## Quyết định Gate 1 · v2 (15 phút, phút 185–200) · Phiếu C, mục C12 (bước 9 trên thẻ)

Điền cột **v2**: quyết định, đổi hay giữ so với v1 và vì con số nào, mã lần chạy của ba mốc, và **ba dòng bắt buộc**:

1. Một giả định về môi trường mà thiết kế của đội đang dựa vào, có thể sai ngoài thực tế.
2. Cổng của đội chỉ GIẢM khả năng hay thực sự NGĂN được tác hại, và vì sao.
3. Vì data là mock, cần đo lại gì trong pilot thật trước Bước đánh giá 2.

**Quy tắc quyết định (điều kiện để bài qua):** quyết định phải khớp bằng chứng và khớp tiêu chí đã ký.
- Chọn **Tiếp tục** khi report còn dòng vượt trần, hoặc còn ngưỡng đã ký chưa đạt, là quyết định không đạt.
- **Thu hẹp** (ghi rõ cắt kho nào, còn bao nhiêu phần trăm, mấy người trực, ticket bị cắt đi đâu), **Cải tiến thêm** (giả thuyết cụ thể, có hạn), **Dừng** (bài học ghi lại) có lý do và có số thì đều là quyết định đạt.

---

# PHẦN C · DEMO BA MỐC (phút 200–230)

Hai bàn cùng thẻ ghép cặp, mỗi bàn 5 phút, rồi 2–3 bàn trình bày trước lớp. Mỗi bàn chiếu **ba cột base · prepared · after** của report và trả lời:

1. Cổng vòng 1 nào đã đỡ được sự cố này trước khi bàn biết nó? Cổng nào bàn không nghĩ tới, và nó thuộc lăng kính nào?
2. Phần sửa ở vòng 2 là code, là con số, hay là người? Vì sao đúng chỗ đó?
3. Quyết định v2, và con số nào đỡ cho nó.
4. Bàn kia đưa một ticket hiểm (câu 2.8) hoặc đổi một con số trong `config/operating_gates.json` (ví dụ bớt một người trực): chạy trực tiếp, đọc kết quả. **Sau demo, trả con số đó về bản v2** rồi chạy lại `python3 -m lab10.grade --incident Sx` và `python3 -m lab10.check_submission --collect` trước khi đẩy bài lần cuối.

Lab Coach hỏi soi theo phiếu thẻ. Không cho điểm.

---

# PHẦN D · NỘP BÀI (không chấm tại lớp)

Bài nộp là thư mục `submission/`. Cách làm và danh sách đầy đủ: `submission/README.md`.

1. Điền `submission/submission.json`: tên bàn, thành viên, số thẻ, quyết định v1 và v2, ba dòng bắt buộc (chép từ Phiếu C mục C12).
2. Chạy `python3 -m lab10.check_submission --collect`. Lệnh gom: code cổng vòng 1 (bản chốt) và vòng 2, config cổng kinh doanh + vận hành + pháp lý (bản vòng 1 và bản hiện tại), tiêu chí đã ký kèm hash, mã lần chạy và report của ba mốc, nhật ký mọi lần chạy (`runs/journal.jsonl`), và **ba phiếu A, B, C**.
3. Sửa các dòng `THIẾU` tới khi lệnh in `ĐỦ THÀNH PHẦN`. Rồi đẩy lên repo của bàn (tên đúng dạng `K5-L3A-DAY10-<TenNhom>-PoCtoPilotGate1` hoặc `K5-L3B-DAY10-<TenNhom>-PoCtoPilotGate1`, ví dụ `K5-L3A-DAY10-XXX-PoCtoPilotGate1`; TenNhom không dấu, không cách):
   `git add -u && git add submission templates TEAM.md && git commit -m "LAB 10: bài nộp" && git push -u origin main`
   Gửi **link repo** cho team chấm theo cách Lab Coach hướng dẫn; **mỗi thành viên** tự nộp link trên LMS trước deadline (GMT+7, [`SUBMISSION.md`](SUBMISSION.md)). Thang điểm: [`RUBRIC.md`](RUBRIC.md).

Lệnh này chỉ kiểm **đủ thành phần**. Team chấm sẽ chấm sau buổi học theo ba lớp: phần máy đo (bài kiểm tra ẩn, chỉ số kinh doanh và vận hành, mức chuẩn bị ở mốc prepared, hash, không làm hỏng ca đang đúng); phần người đọc (pre-mortem và HAZOP có phủ kinh doanh, con người, pháp lý; checklist có PIC; runbook; phân tích sự cố ở Phiếu C; ba dòng bắt buộc; câu trả lời lúc demo); và điều kiện qua (quyết định khớp bằng chứng và tiêu chí đã ký).
