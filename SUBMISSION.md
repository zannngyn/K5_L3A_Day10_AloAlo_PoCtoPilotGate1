# Submission · LAB 10 · From PoC to Pilot (Gate 1)

## Loại bài

**Nhóm** (một bàn 3–4 người). Một repo cho cả bàn, do trưởng nhóm tạo, kèm [`TEAM.md`](TEAM.md) điền đầy đủ.

## Đặt tên repo

| Loại | Tên | Ghi chú |
|---|---|---|
| Repo đề (repo mẫu) | `K5_L3_Day10_PoC-to-Pilot_Gate1_student` | Không push lên repo này |
| Repo bài nộp của bàn | `K5-<L3A\|L3B>-DAY10-<TenNhom>-PoCtoPilotGate1` | Ví dụ `K5-L3A-DAY10-NhomSao-PoCtoPilotGate1`. `TenNhom` không dấu, không khoảng trắng, không thêm chữ `Lop` |

Tên theo quy ước chung của khóa: `Kn-L3{A|B}-DAYxx-TenNhom-TenBai`. Với lab này, `TenBai` là `PoCtoPilotGate1`. Dòng cuối của lệnh 7 còn in dạng tên cũ (`K5_Day10_3A_…`). Không dùng dạng đó. Đặt tên repo theo dạng trong bảng trên. Giá trị `team` trong `config/acceptance_criteria.json` và `submission/submission.json` phải **giống hệt** tên repo.

## Cấu trúc và deliverable phải nộp

Bài nộp là thư mục `submission/` do lệnh 7 gom, cùng với `TEAM.md`. Danh sách đầy đủ từng file: [`submission/README.md`](submission/README.md#bài-nộp-gồm-gì).

| Thành phần | Ở đâu | Ai làm |
|---|---|---|
| Ba phiếu A, B, C | `templates/form-*.md` → lệnh 7 chép vào `submission/docs/` | Cả bàn |
| Tiêu chí đã ký + hash | `config/acceptance_criteria.json`, `.lock` | Sản phẩm và kinh doanh |
| Cổng vòng 1 (bản chốt) và vòng 2 | `lab10/guards.py`, `lab10/monitors.py`, `config/operating_gates.json` | Kỹ sư cổng · Vận hành và pháp lý |
| Report ba mốc, nhật ký lần chạy | lệnh 6 và lệnh 7 tự tạo | Kỹ sư cổng |
| `submission/submission.json` | `members` ghi dạng `"HoVaTen-MSSV"`, ví dụ `"NguyenVanAn-20241234"` | Vận hành và pháp lý |
| `TEAM.md` | Bảng thành viên và mục cá nhân của **từng** người | Trưởng nhóm + từng thành viên |

## Nơi nộp

1. Trưởng nhóm đẩy bài lên repo của bàn (README mục 6) và mời tài khoản team chấm quyền **Read** (README mục 2, bước 1).
2. **Mỗi thành viên tự nộp link repo của bàn trên LMS bằng tài khoản cá nhân**, kể cả khi trưởng nhóm đã gửi link cho Lab Coach. Ai không nộp link trên LMS thì không có bài.

## Deadline (GMT+7)

- Trong buổi: đẩy bài lần cuối trước phút 240 (README mục 6).
- Hạn chót nộp link trên LMS:
  - Lab **buổi sáng**: trước **23h59 GMT+7** ngày lab.
  - Lab **buổi chiều/tối**: trước **11h59 GMT+7** ngày hôm sau.
- Coach có thể gia hạn tối đa **48 giờ** nếu có lý do chính đáng. Nộp muộn: xem [`RULES.md`](RULES.md#nộp-muộn-và-lỗi-kỹ-thuật).

Commit sau hạn chót không được tính; team chấm lấy commit cuối cùng trước hạn.

## Checklist

- [ ] Repo của bàn đúng tên `K5-<L3A|L3B>-DAY10-<TenNhom>-PoCtoPilotGate1`, đã mời team chấm.
- [ ] `TEAM.md` có đủ họ tên, MSSV, vai của mọi thành viên và mục `## HoVaTen-MSSV` của từng người.
- [ ] Tiêu chí đã ký, commit và push **trước** lần đánh giá đầu tiên.
- [ ] Đã chốt cổng vòng 1 (lệnh 5) trước phút 115.
- [ ] Ba phiếu A, B, C đã điền **mọi mục** (A1–A5, B0–B8, C0–C12); dòng `Thẻ đã bốc:` đúng số thẻ. Lệnh 7 báo tên mục còn nguyên mẫu. Bàn bốc thẻ S4 không cần điền C3.
- [ ] `submission/submission.json` đủ trường, `members` có MSSV.
- [ ] Lệnh 7 in `ĐỦ THÀNH PHẦN` trên đúng code và config cuối cùng.
- [ ] Trên GitHub, thư mục `submission/runs/` có `journal.jsonl`, `grade-report.*` và report ba mốc. Team chấm dùng các file này để kiểm "ký trước khi đo".
- [ ] Không commit API key, mật khẩu, file `.env`.
- [ ] **Mỗi thành viên** đã nộp link repo trên LMS trước deadline.
