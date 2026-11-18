# incidents/ · Gói sự cố (chưa có gì ở đây cho tới phút 125)

Thư mục này cố ý để trống lúc đầu buổi. Đây là chỗ các **gói sự cố** sẽ xuất hiện.

**Phút 125**, sau giờ nghỉ, giảng viên đẩy thẻ sự cố lên **repo mẫu**. Khi Lab Coach báo "đã phát":

1. Chạy lệnh sau từ thư mục repo của bàn (đúng đủ các cờ):

   ```bash
   git pull --no-rebase --no-edit --allow-unrelated-histories -X ours upstream main
   ```

   Repo của bàn tạo từ *Use this template* nên có lịch sử git khác repo mẫu: `--allow-unrelated-histories` cho phép gộp lần đầu (repo tạo bằng Fork thì cờ này vô hại); `-X ours` giữ nguyên bài của bàn và chỉ lấy thêm thẻ. `--no-rebase --no-edit` tránh bị hỏi cách gộp hay mở trình soạn thảo. Nếu báo `'upstream' does not appear to be a git repository`, gắn repo mẫu (bước 2a ở mục 2 của `README.md`) rồi chạy lại:

   ```bash
   git remote add upstream https://github.com/VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_student.git
   git remote -v
   ```

   Nếu máy báo `Please tell me who you are`, làm bước 2b rồi chạy lại. Nếu báo xung đột, chạy `git merge --abort` rồi chạy lại đúng đủ lệnh trên, hoặc gọi Lab Coach.

2. Bạn sẽ thấy 8 thư mục mới `incidents/S1/` … `incidents/S8/`, và một file mới `incident-cards.md` ở **gốc repo** (cùng chỗ với `README.md` chính, không nằm trong `incidents/`).
3. Mỗi **cặp bàn** (Lab Coach đã ghép sẵn) cử một người lên **bốc số**; hai bàn trong cặp làm cùng một thẻ. Số bốc được là một trong S1–S8. Lab Coach ghi số đó vào sổ.
4. Bàn **chỉ làm đúng thẻ đã bốc**. Mở `incidents/Sx/card.md` (thay `Sx` bằng số của bàn) và đọc mặt trước.
5. Ghi số đó vào dòng `Thẻ đã bốc:` ở đầu Phiếu C (`templates/form-c-incident.md`).
6. Chạy ngay `python3 -m lab10.grade --incident Sx`, khi chưa sửa gì, để xem cổng bàn dựng ở vòng 1 đỡ được bao nhiêu. Kéo thẻ đúng thì report có `1 integrity | ✅`.

Kéo trước phút 125 thì chưa có thẻ (lệnh báo `Already up to date`): chờ Lab Coach báo rồi kéo lại.

Mỗi thư mục `incidents/Sx/` sẽ có:

| File | Nó là gì |
|---|---|
| `card.md` | Thẻ sự cố: mặt trước là tin nhắn báo sự cố, mặt sau là nhiệm vụ và luật |
| `tickets.jsonl` | Các ticket của sự cố, kèm kết quả đúng |
| `world_patch.json` | Dữ liệu bổ sung của sự cố (đơn hàng, phê duyệt, sổ cái có sẵn…) |
| `card.json` | Hai lệnh chạy và tự kiểm tra của thẻ |

Không sửa các file này: chúng bị khoá, lệnh tự kiểm tra sẽ phát hiện.

Nếu chạy lệnh tự kiểm tra (`python3 -m lab10.grade`) trước khi nhận thẻ, bạn sẽ thấy dòng `TỪ CHỐI KIỂM TRA: chưa có gói sự cố …`. Đó là đúng thiết kế, không phải lỗi máy.
