# submission/ · Bài nộp của bàn

Mọi thứ bàn nộp nằm trong thư mục này, trên **repo của bàn**. Một team chấm tự động sẽ chấm **sau buổi học**; tại lớp không ai cho điểm.

Tên repo phải đúng dạng `K5-L3A-DAY10-<TenNhom>-PoCtoPilotGate1` hoặc `K5-L3B-DAY10-<TenNhom>-PoCtoPilotGate1` (ví dụ `K5-L3A-DAY10-XXX-PoCtoPilotGate1`). `L3A` / `L3B` là lớp của bàn (lớp 3A hoặc 3B). `TenNhom` viết không dấu, không khoảng trắng. Không viết thêm chữ `Lop`.

## Làm ba bước

**Bước 1. Điền `submission.json`** (mẫu có sẵn, mở bằng trình soạn thảo bất kỳ):

| Trường | Điền gì | Ví dụ |
|---|---|---|
| `team` | Tên bàn = đúng tên repo, giống hệt `team` trong Bản tiêu chí đã ký | `"K5-L3A-DAY10-XXX-PoCtoPilotGate1"` |
| `members` | Họ tên không dấu và MSSV của mọi thành viên, khớp `TEAM.md` | `["NguyenVanAn-20241234", "TranThiBinh-20245678"]` |
| `incident` | Số thẻ bàn bốc được | `"S4"` |
| `decision_v1` | Quyết định Gate 1 bản v1 | `"Tiếp tục"` |
| `decision_v2` | Quyết định Gate 1 bản v2 | `"Thu hẹp"` |
| `three_lines.environment_assumption` (chép từ Phiếu C mục C12) | Một giả định về môi trường mà thiết kế của bàn dựa vào, có thể sai ngoài thực tế | một câu |
| `three_lines.reduce_or_prevent` | Cổng của bàn chỉ GIẢM khả năng hay NGĂN hẳn tác hại, vì sao | một câu |
| `three_lines.measure_in_pilot` | Vì dữ liệu ở đây là giả, cần đo lại gì khi chạy thử thật | một câu |

Quyết định chỉ nhận một trong bốn giá trị: `Tiếp tục`, `Thu hẹp`, `Cải tiến thêm`, `Dừng`.

**Bước 2. Gom file và kiểm:**

```bash
python3 -m lab10.check_submission --collect
```

Lệnh này tự chép vào đây: code cổng vòng 1 và vòng 2, config cổng, tiêu chí đã ký, báo cáo tự kiểm tra cùng ba mốc, nhật ký mọi lần chạy (`runs/journal.jsonl`), và ba phiếu trong `templates/`. Sau đó nó in danh sách `ĐỦ` / `THIẾU`.

**Bước 3. Sửa chỗ `THIẾU`, chạy lại lệnh tới khi thấy `ĐỦ THÀNH PHẦN`.** Rồi đẩy lên repo của bàn và **gửi link repo** cho team chấm theo cách Lab Coach hướng dẫn:

```bash
git add -u
git add submission templates TEAM.md
git commit -m "LAB 10: bài nộp"
git push -u origin main
```

Link gửi đi là URL repo của bàn, ví dụ `https://github.com/<tài-khoản>/K5-L3A-DAY10-XXX-PoCtoPilotGate1`. Team chấm cần đã được mời vào repo (README mục 2, bước 1). **Mỗi thành viên** tự nộp link này trên LMS trước deadline (GMT+7, xem [`SUBMISSION.md`](../SUBMISSION.md#deadline-gmt7)). Không push lên repo mẫu.


## Bài nộp gồm gì

| Trong `submission/` | Là gì | Ai tạo |
|---|---|---|
| `submission.json` | Tên bàn, thành viên, số thẻ, quyết định v1 và v2, ba dòng bắt buộc | Bàn điền |
| `code/guards_round1.py` | Cổng phòng ngừa vòng 1, bản đã chốt | Lệnh gom |
| `code/guards.py`, `code/monitors.py` | Cổng sau khi sửa ở vòng 2, chỉ số theo dõi | Lệnh gom |
| `config/operating_gates.round1.json`, `config/operating_gates.json` | Cổng kinh doanh, vận hành, pháp lý: bản vòng 1 và bản hiện tại | Lệnh gom |
| `config/acceptance_criteria.json`, `.lock` | Bản tiêu chí đã ký và hash | Lệnh gom |
| `config/round1.lock`, `config/switches.json` | Dấu chốt vòng 1, công tắc | Lệnh gom |
| `runs/grade-report.json`, `.md` | Báo cáo tự kiểm tra gần nhất | Lệnh gom |
| `runs/<mã lần chạy>/report.json` | Ba mốc: base, prepared, after | Lệnh gom |
| `runs/journal.jsonl` | Nhật ký mọi lần chạy `eval` / `grade` (mã lần chạy có ngày giờ); team chấm dùng để kiểm "ký trước khi đo" | Lệnh gom |
| `docs/form-a-criteria.md` | Phiếu A: tiêu chí và cách đo (khối 1) | Bàn điền trong `templates/` |
| `docs/form-b-evaluation-gates.md` | Phiếu B: lần chạy đầu, soát lỗi, bản đồ dữ liệu, HAZOP vòng 1, checklist 9 nhóm, pre-mortem, cổng vòng 1, runbook 1–3, giờ cao điểm, quyết định v1 | Bàn điền trong `templates/` |
| `docs/form-c-incident.md` | Phiếu C: dòng `Thẻ đã bốc`, phân tích sự cố, phần riêng theo thẻ, HAZOP của thẻ, fault tree, bảng sửa, chỉ số theo dõi, risk register, runbook 4–5, quyết định v2 | Bàn điền trong `templates/` |
| `manifest.json` | Danh sách file kèm dấu vân tay, mã lần chạy | Lệnh gom |

Bàn điền phiếu ngay trong thư mục `templates/`. Đừng sửa các bản chép trong `submission/docs/`: lần gom sau sẽ ghi đè.
