# Rubric · LAB 10 · From PoC to Pilot (Gate 1)

Không chấm tại lớp. Team chấm chấm **sau buổi học** từ repo của bàn, theo ba lớp mô tả ở [`problem-set.md` phần D](problem-set.md#phần-d--nộp-bài-không-chấm-tại-lớp): phần máy đo, phần người đọc, và điều kiện qua.

## Điều kiện qua (không đạt thì bài không được tính điểm)

| Điều kiện | Bằng chứng |
|---|---|
| Tiêu chí ký **trước** lần đánh giá đầu tiên và không đổi sau khi ký | Lịch sử git, `config/acceptance_criteria.lock`, `runs/journal.jsonl` |
| File bị khoá và bản chốt vòng 1 còn nguyên | `1 integrity ✅` trong report; `config/round1.lock` |
| Quyết định v2 khớp bằng chứng và tiêu chí đã ký | Phiếu C mục C12, report ba mốc. Chọn **Tiếp tục** khi còn vượt trần hoặc ngưỡng đã ký chưa đạt là không qua |
| Lệnh 7 in `ĐỦ THÀNH PHẦN` | `submission/manifest.json` |

## Điểm chính (100)

| Tiêu chí | Điểm | Bằng chứng | Trừ điểm khi |
|---|---:|---|---|
| C1 · Tiêu chí và cách đo (Phiếu A, câu 1.1–1.6) | 15 | Phiếu A; `config/acceptance_criteria.json` | Ngưỡng chép từ file example; thiếu `business_ops` hoặc `decision_rule` |
| C2 · Rủi ro trước sự cố (câu 2.1–2.5) | 15 | Phiếu B mục B1–B6 | HAZOP < 3 dòng hoặc không có dòng ngoài kỹ thuật; checklist thiếu PIC có tên; pre-mortem thiếu lăng kính |
| C3 · Cổng vòng 1 và quyết định v1 (câu 2.6–2.10, B8) | 15 | `submission/code/guards_round1.py`, `config/operating_gates.round1.json`, Phiếu B | Không có mốc `prepared`; runbook 1–3 không khớp con số trong config |
| C4 · Kết quả máy đo trên thẻ sự cố và test ẩn | 25 | Report ba mốc `base · prepared · after`; test ẩn | Chặn hết, thu hẹp về 0 hay xếp quá nhiều người trực; làm hỏng ca trước đó đúng (`regression`); xử lý riêng theo mã ticket |
| C5 · Phân tích và sửa sự cố (câu 3.0–3.7) | 20 | Phiếu C mục C2–C11; `lab10/monitors.py` | Fault tree không có bằng chứng ở lá; thiếu chỉ số theo dõi mới; thiếu risk register |
| C6 · Quyết định v2 và ba dòng bắt buộc | 10 | Phiếu C mục C12; `submission/submission.json` | Ba dòng chung chung, không gắn con số; không nêu đổi hay giữ so với v1 |
| **Tổng điểm chính** | **100** | | |

## Bonus (tối đa +10, là điểm lab, ghi riêng)

| Bonus | Điểm | Bằng chứng |
|---|---:|---|
| Cổng vòng 1 đã đỡ được phần lớn sự cố trước khi biết thẻ (`prepared` gần `after`) | +5 | Report ba mốc |
| Chỉ số theo dõi hoặc cổng phát hiện được lỗi chìm ngoài thẻ, có bằng chứng trace | +5 | Phiếu C, `ticket@seed` |

Bonus không cộng quá 10 và không bù cho điều kiện qua. Demo và trả lời phản biện được Lab Coach ghi nhận cho C5–C6, không phải điểm phát biểu riêng.

## Trừ điểm chung

- Thiếu `TEAM.md` hoặc thiếu mục cá nhân của thành viên: thành viên đó không có điểm cá nhân.
- `members` trong `submission.json` không có MSSV hoặc không khớp `TEAM.md`: −5.
- Sai tên repo hoặc `team` không khớp tên repo: −5.
