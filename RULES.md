# Rules · LAB 10

Luật vận hành của lab (ký tiêu chí, chốt vòng 1, test ẩn, không làm hỏng ca đúng…) nằm ở [README mục 5](README.md#5-luật). File này thêm các luật chung của khóa.

## AI và công cụ

- Được dùng trợ lý AI (ChatGPT, Claude, Copilot…) để đọc code, gợi ý cách viết cổng, soát câu chữ trong phiếu.
- Mọi ngưỡng trong Bản tiêu chí, mọi con số trong `config/operating_gates.json` và quyết định v1/v2 là **của bàn**: bàn phải giải thích được lúc demo vì sao chọn con số đó. Không giải thích được thì coi như không có.
- Không dùng AI để viết code xử lý riêng theo mã ticket hay câu chữ cụ thể (README mục 5, luật 4); bộ test ẩn sẽ bắt.
- Ghi vào mục cá nhân trong `TEAM.md` nếu đã dùng AI cho phần việc nào.

## Hợp tác và liêm chính

- Bài làm theo bàn. Không sao chép phiếu, cổng hay config của bàn khác, kể cả bàn cùng cặp thẻ.
- Chỉ làm đúng thẻ đã bốc; không mở hay tiết lộ thẻ của bàn khác (README mục 5, luật 6).
- Không sửa file bị khoá bằng hash, không sửa bản chốt vòng 1, không sửa tiêu chí sau khi ký.
- Ghi nguồn nếu dùng code, dữ liệu hoặc tài liệu bên ngoài.
- Mỗi thành viên ghi rõ đóng góp của mình trong `TEAM.md`.

## Secret và API key

- Lab không cần khóa API. Không commit API key, mật khẩu hay file `.env`.
- Danh tính Git dùng MSSV và email giả `<MSSV>@example.com` (README mục 2, bước 2b), không dùng email cá nhân.

## Nộp muộn và lỗi kỹ thuật

- Deadline: xem [`SUBMISSION.md`](SUBMISSION.md#deadline-gmt7).
- Commit sau hạn chót không được tính, trừ khi Coach đã gia hạn (tối đa 48 giờ).
- Gặp lỗi kỹ thuật (push hỏng, không kéo được thẻ…): báo Lab Coach ngay trong buổi; nếu sau buổi, gửi mô tả lỗi kèm ảnh chụp lệnh và output trước deadline.
