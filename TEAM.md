# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `AloAlo`
- Lớp: `L3A`
- Repo của bàn: `K5_L3A_Day10_AloAlo_PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S4`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên        | MSSV        | Vai                    | Trưởng nhóm |
| --: | ---------------- | ----------- | ---------------------- | :---------: |
|   1 | Nguyễn Thế Văn   | 2A202603474 | Sản phẩm và Kinh Doanh |      x      |
|   2 | Trần Văn Tài     | 2A202603506 | Vận hành và pháp lý    |             |
|   3 | Phan Nhật Trường | 2A202603459 | Kỹ sư cổng             |             |
|   4 | Nguyễn Tiến Đạt  | 2A202603452 | Kỹ sư cổng             |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenTheVan-2A202603474

### Phần việc phụ trách

- **Vai trong bàn:** Trưởng nhóm · Sản phẩm và Kinh doanh (phối hợp thiết lập cổng vận hành/pháp lý vòng 1 và gom bài nộp cuối buổi).
- **Câu đề & mục phiếu:** Câu 1.1, 1.6 (Phiếu A mục A1, A4, A5); Câu 2.4, 2.10 (Phiếu B mục B4, B5, B7.5, B7.6); Câu 3.2, 3.7 và quyết định Gate 1 v2 (Phiếu C mục C5, C10, C11, C12).
- **File phụ trách:** `config/acceptance_criteria.json` (người ký `signed_by`), `config/operating_gates.json` (điều chỉnh `daily_refund_cap_vnd = 300000`, `roi_min = 0.3`, `reviewers_on_shift = 2`), `submission/submission.json`, `TEAM.md`.

### Đóng góp cụ thể

- Khởi tạo repo bàn, cấu hình remote `origin`/`upstream`, điều phối chia vai và chốt ngưỡng Bản tiêu chí chấp nhận trước khi chạy đánh giá (`pass_rate >= 0,94`, `pass_k >= 0,86`, 3 ngưỡng an toàn `= 0`, `cost <= 6.000đ`, `ROI >= 0,5`).
- Viết phân tích HAZOP vòng 1 (`file_carrier_fault`), Checklist 9 nhóm việc go-live lần 1 và Runbook phần 1–3 cùng kịch bản Giờ cao điểm (B7.5–B7.6) ở vòng 1.
- Ở vòng 2 (thẻ `S4` đêm sale 11.11): đối chiếu ngân sách ngày sale `300.000đ` của Finance, hạ `business.daily_refund_cap_vnd` từ `500.000đ` về `300.000đ`, kích hoạt ca 2 người trực (`12 ca/giờ`), lập Risk register (C10) và tổng hợp bằng chứng đổi quyết định từ `Tiếp tục` (v1) sang `Thu hẹp` (v2) do chi phí ngày sale `7.296đ/ticket > 6.000đ` (riêng kho `DN` `7.568đ/ticket`).

### Bằng chứng

- Mã commit: `43d89f8`, `1f88cd3`, `e343882` (hash tiêu chí `6ec55a46`), `2721d76`.
- Mã lần chạy: `R-S4-after-20261118-213118-55a516`, `R-S4-after-20261118-213302-5d39b2`, `R-S4-grade-20261118-213302-5d39b2`.
- Dòng trong phiếu: Phiếu A mục A1, A4, A5; Phiếu B mục B4, B5, B7.5–B7.6; Phiếu C mục C5 (Câu 3.2), C10 (R1), C11, C12 và `submission/submission.json`.

### Exit ticket

- **Một điều học được:** Đặt ngưỡng chấp nhận và `decision_rule` trước khi nhìn số giúp nhóm không tự hợp thức hoá kết quả — khi đêm sale 11.11 làm chi phí tăng lên `7.296đ/ticket` (`ROI = 0,37`), nhóm có căn cứ rõ ràng để chọn `Thu hẹp` thay vì cố chọn `Tiếp tục` khi đã vượt ngưỡng ký `6.000đ`.
- **Một điều còn chưa chắc:** Ngoài thực tế khi tách riêng form hàng vỡ/thất lạc (`DAMAGED`, `NOT_RECEIVED`) trước khi vào trợ lý, tỉ lệ khách chọn nhầm danh mục "giao trễ" để được xử lý nhanh sẽ là bao nhiêu phần trăm và làm đội chi phí lên bao nhiêu.

---

## TranVanTai-2A202603506

### Phần việc phụ trách

- **Vai trong bàn:** Vận hành và pháp lý (phối hợp phân tích dữ liệu, cổng kinh doanh vòng 1 và quyết định v1/v2).
- **Câu đề & mục phiếu:** Câu 1.2, 1.4 (Phiếu A mục A1, A2); Câu 2.3, 2.9 và quyết định v1 (Phiếu B mục B3, B7.4, B8); Câu 3.1, 3.3, 3.7 (Phiếu C mục C1, C3/B7.6, C5 Câu 3.3, C11 Runbook phần 4–5, C12).
- **File phụ trách:** `config/operating_gates.json` (mục `business`, `operations`, `legal`), `.gitattributes`, `templates/form-b-evaluation-gates.md`, `templates/form-c-incident.md`.

### Đóng góp cụ thể

- Thiết kế mục tiêu từ góc nhìn kế toán đối soát chị Oanh & trưởng ca CSKH chị Hạnh (Câu 1.2) cùng telemetry không nhãn theo dõi lệnh phạt hãng (Câu 1.4).
- Xây dựng Bản đồ dữ liệu và kịch bản drift chính sách `REFUND-v3 → REFUND-v4` ngày `01/12/2026` (B3), thiết lập bộ số `business` vòng 1 (B7.4) và tổng hợp bằng chứng chốt quyết định Gate 1 `v1 = Tiếp tục` trên mốc `prepared` (B8), đồng thời xử lý `.gitattributes` để giữ khớp byte hash giữa Windows và macOS.
- Ở vòng 2 (`S4`): phân tích giả định môi trường ca đêm 11.11 (Câu 3.3), cập nhật đối chiếu Giờ cao điểm (B7.6) và viết Runbook phần 4–5 (quy trình truyền thông với 5 hãng vận chuyển, chị Oanh, chị Hạnh và 3 kịch bản tuần đầu pilot ở C11).

### Bằng chứng

- Mã commit: `e6bbb7e`, `2fe7f8a`, `dd8167e`, `4f7f90c`, `89e470d`.
- Mã lần chạy: `R-base-prepared-20261118-172112-8f5a8c`, `R-S4-grade-20261118-205039-5720e5`, `R-S4-grade-20261118-213302-5d39b2`.
- Dòng trong phiếu: Phiếu A mục A1 (Câu 1.2), A2 (Câu 1.4); Phiếu B mục B3, B7.4, B7.6, B8; Phiếu C mục C1, C5 (Câu 3.3), C11, C12.

### Exit ticket

- **Một điều học được:** Không phải mọi sự cố của hệ thống AI đều sửa bằng code — ở thẻ `S4`, cổng code vòng 1 đã chặn sạch 100% hoàn sai và lỗi hãng oan, nhưng hệ thống vẫn thất bại vận hành (`5` ca ùn, chờ `82` phút) cho tới khi điều chỉnh đúng bài toán con người (`reviewers_on_shift = 2`) và trần tài chính ngày sale (`300.000đ`).
- **Một điều còn chưa chắc:** Mức kiểm mẫu `review_sampling_pct = 5%` kèm `decision_note = true` có đủ để duy trì lòng tin dài hạn của chị Hạnh khi chuyển từ MockLLM sang LLM thật có câu chữ đa dạng hơn hay không.

---

## PhanNhatTruong-2A202603459

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng.
- **Câu đề & mục phiếu:** Câu 1.3 (Phiếu A mục A2 Offline metric); Câu 2.1, 2.2, 2.6 (Phiếu B mục B0, B1, B2, B7.1); Câu 3.0, 3.1, 3.5, 3.6 (Phiếu C mục C0, C1, C2, C7, C8).
- **File phụ trách:** `lab10/guards.py` (vòng 1 `guards_round1.py` và mở rộng vòng 2), `lab10/monitors.py`, chạy các lệnh `criteria sign`, `eval`, `trace`, `gate`, `checkpoint`, `grade`, `check_submission`.

### Đóng góp cụ thể

- Thiết kế offline metric `policy_selection_error_rate` (Câu 1.3), ký tiêu chí (`e343882`), chạy baseline `base`, phân tích lỗi chìm `model_override` trên `T-002@55` (B1–B2).
- Hiện thực 3 cổng phòng ngừa vòng 1 trong `lab10/guards.py` (`pre_guard` ghim `effective_policy`, `write_gate` đối chiếu `entitlement_vnd`/phê duyệt chính chủ, chặn `file_carrier_fault` sai căn cứ, lọc allowlist `notify_carrier`) và chốt `checkpoint` `61022954` — giúp chặn trước 100% lỗi hoàn sai (`160.000đ → 0đ`) và 27 lỗi hãng oan ngay khi chạm thẻ `S4` ở mốc `prepared`.
- Ở vòng 2 (`S4`): dò trace `S4-05@11`, `S4-08@11`, `S4-13@11` phát hiện cơ chế `429 → fail_open` và nguy cơ `confirm 429 → write_retry`; bổ sung kiểm chống ghi trùng (`ledger_rows`), kiểm động `ops_limits()` và chuẩn hoá `basis="policy"` trong `lab10/guards.py`, cùng 4 hàm giám sát mới trong `lab10/monitors.py` (`peak_hour_review_load`, `llm_degraded_rate`, `daily_cap_hit_rate`, `model_override_rate`).

### Bằng chứng

- Mã commit: `e343882`, `5834960`, `8d66313`, `4f2cff0`, `a477219`.
- Mã lần chạy: `R-base-before-20261118-164248-bde05c`, `R-base-after-20261118-172029-8f5a8c`, `R-base-prepared-20261118-172112-8f5a8c`, `R-S4-after-20261118-213004-8048a4`, `R-base-after-20261118-213302-5d39b2`, `R-S4-grade-20261118-213302-5d39b2`.
- Dòng trong phiếu: Phiếu A mục A2 (cột Offline); Phiếu B mục B0, B1, B2, B7.1; Phiếu C mục C0, C2, C7, C8.

### Exit ticket

- **Một điều học được:** Chế độ fallback "chiều khách" (`fail_open`) khi dịch vụ LLM bị `429` cực kỳ nguy hiểm với các agent có quyền ghi sổ cái và phạt đối tác; mọi thao tác ghi không đảo ngược phải đi qua lớp kiểm tra tất định từ nguồn sự thật (DB) và đảm bảo tính idempotent khi retry.
- **Một điều còn chưa chắc:** Khi triển khai thật với nhiều worker chạy song song, kiểm tra trần ngày `auto_refund_today_vnd()` và chống ghi trùng `ledger_rows` sẽ cần khoá giao dịch (transaction lock / atomic counter) ở tầng DB như thế nào để không bị race condition ở giây cao điểm 11.11.

---

## NguyenTienDat-2A202603452

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng (phụ trách kiểm thử hành vi, chống rò rỉ dữ liệu, Pre-mortem và phân tích cây lỗi Fault tree / HAZOP sự cố).
- **Câu đề & mục phiếu:** Câu 1.5 (Phiếu A mục A3); Câu 2.5, 2.7, 2.8 (Phiếu B mục B6, B7.2, B7.3); Câu 3.1, 3.4, 3.7 (Phiếu C mục C4 HAZOP thẻ S4, C6 Fault tree trước khi sửa, C9 Fault tree sau khi sửa, C10 R3).
- **File phụ trách:** `templates/form-b-evaluation-gates.md` (B6, B7.2, B7.3), `templates/form-c-incident.md` (C4, C6, C9), phối hợp kiểm thử `lab10/guards.py` và `tests/test_public.py`.

### Đóng góp cụ thể

- Phân tích khoảng tin cậy bootstrap ở Câu 1.5 (A3) và chủ trì tổng hợp bảng Pre-mortem 4 lăng kính ở B6, chốt 3 cổng ưu tiên cho vòng 1.
- Thiết kế quy trình 2 bước chống rò rỉ dữ liệu đánh giá (B7.2) và xây dựng bộ behavioral test kèm 2 ticket hiểm chạy `--adhoc` kiểm chứng tính chất bất biến nguồn dữ liệu DB (B7.3).
- Ở vòng 2 (`S4`): thực hiện phân tích HAZOP chuyên sâu cho luồng suy thoái `429` đêm sale (C4 — phát hiện nhánh `llm.confirm` retry ghi đúp chưa lộ trên trace công khai), dựng Fault tree trước và sau khi sửa (C6, C9) phân tách rõ cổng nào **ngăn hẳn** (code DB/idempotency/trần tiền) và cổng nào chỉ **giảm khả năng** (tăng công suất người trực), đồng thời rà lỗi chìm `model_override` (`T-001@55, T-015@55, T-021@55, T-022@55`) và phân khúc kho `?` (`T-018`) trên bộ nền.

### Bằng chứng

- Mã commit: `5453e91`, `67c6b8a`, `ebdd8be`.
- Mã lần chạy: `R-base-after-20261118-172029-8f5a8c`, `R-S4-grade-20261118-205039-5720e5`, `R-S4-grade-20261118-213302-5d39b2` (cùng `Ran 13 tests … OK`).
- Dòng trong phiếu: Phiếu A mục A3; Phiếu B mục B6, B7.2, B7.3; Phiếu C mục C4, C6, C9, C10 (R3).

### Exit ticket

- **Một điều học được:** Phân biệt rạch ròi giữa **ngăn hẳn** (biến nhánh `HOẶC` thành `VÀ` với một cổng code tất định không phụ thuộc LLM) và **giảm khả năng** (thêm người trực `12 ca/giờ` chỉ dời ngưỡng gãy lên cao hơn) giúp đánh giá trung thực rủi ro còn hở trên Fault tree.
- **Một điều còn chưa chắc:** Làm sao thiết kế bộ sinh tải (load/stress test) sát với phân phối dồn cục thực tế của các chiến dịch flash-sale 0h/20h mà không bị quá khớp (overfit) vào một kịch bản cố định như 41 ticket của `S4`.
