# Checkpoints · LAB 10

Mỗi checkpoint ứng với một mốc trong [Timeline ở README mục 3](README.md#timeline). Lệnh 1–7: [README mục 4](README.md#bay-lenh).

## CP1 · Cài đặt và chia vai (phút 0–15)

- **Mục tiêu:** repo của bàn chạy được, mọi người biết vai của mình.
- **Cần làm:** README mục 2 (tạo repo, clone, gắn `upstream`, danh tính Git); điền `TEAM.md`; chia ba vai.
- **Sản phẩm:** repo `K5-<L3A|L3B>-DAY10-<TenNhom>-PoCtoPilotGate1` đã mời team chấm; bảng thành viên trong `TEAM.md`.
- **Cần hiểu:** vì sao cần `upstream` (thẻ sự cố tới từ repo mẫu ở phút 125).
- **Tự kiểm tra:** `python3 -m unittest discover -s tests` in `Ran 13 tests … OK`; `git remote -v` có `origin` và `upstream`.

## CP2 · Ký tiêu chí (phút 15–65) · Phiếu A

- **Mục tiêu:** viết ngưỡng chấp nhận **trước** khi biết trợ lý đạt hay trượt.
- **Cần làm:** câu 1.1–1.6; điền `config/acceptance_criteria.json`; lệnh 1; commit và push ngay.
- **Sản phẩm:** Phiếu A mục A1–A5; `config/acceptance_criteria.json` + `.lock` đã push.
- **Cần hiểu:** câu tiêu chí "Nếu … thì chúng tôi sẽ …"; khác nhau giữa `pass_rate`, `pass^k` và `pass@k`.
- **Tự kiểm tra:** máy in `ĐÃ KÝ.`; commit ký có trên GitHub trước mọi lần chạy `eval`.

## CP3 · Đo, rủi ro, cổng vòng 1, quyết định v1 (phút 65–115) · Phiếu B

- **Mục tiêu:** tìm rủi ro trước khi sự cố xảy ra và dựng cổng phòng ngừa.
- **Cần làm:** câu 2.1–2.10 (lệnh 2, 3, 4); code 2–3 cổng trong `lab10/guards.py`; điền `config/operating_gates.json`; lệnh 5; quyết định v1.
- **Sản phẩm:** Phiếu B mục B0–B8; bản chốt `lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock` (lệnh 5 tạo ra).
- **Cần hiểu:** cổng code và cổng con số khác nhau thế nào; vì sao không chặn hết.
- **Tự kiểm tra:** có mã lần chạy base; `T-002@55` được xếp loại lỗi; lệnh 5 chạy thành công; đã commit và push.

## CP4 · Sự cố (phút 125–185) · Phiếu C

- **Mục tiêu:** đo cổng vòng 1 đỡ được gì, rồi sửa đúng chỗ.
- **Cần làm:** kéo thẻ (`incidents/README.md`); ghi `Thẻ đã bốc:`; lệnh 6 trước khi sửa; câu 3.0–3.7; thêm ít nhất một chỉ số trong `lab10/monitors.py`.
- **Sản phẩm:** Phiếu C mục C0–C11 (bàn bốc thẻ S4 không cần điền C3); report có `base · prepared · after`.
- **Cần hiểu:** sửa là **giảm** hay **ngăn** tác hại; fault tree có nhánh ngoài kỹ thuật.
- **Tự kiểm tra:** report có `1 integrity ✅`, `3 visible ✅`, `5 regression ✅`, `6 monitor ✅`. Hai dòng `visible` và `regression` chỉ ✅ khi độ phủ pilot lớn hơn 0. Thu hẹp phạm vi về 0 không phải cách sửa.

## CP5 · Quyết định v2, demo, nộp (phút 185–240)

- **Mục tiêu:** quyết định Gate 1 khớp bằng chứng và tiêu chí đã ký.
- **Cần làm:** Phiếu C mục C12; `submission/submission.json` (`members` dạng `HoVaTen-MSSV`); lệnh 7; demo; đẩy bài.
- **Sản phẩm:** thư mục `submission/` đầy đủ; mục cá nhân trong `TEAM.md`.
- **Cần hiểu:** vì sao chọn Tiếp tục khi còn vượt trần là quyết định không đạt.
- **Tự kiểm tra:** lệnh 7 không báo mục phiếu nào còn nguyên mẫu và in `ĐỦ THÀNH PHẦN`; mỗi thành viên đã nộp link trên LMS ([`SUBMISSION.md`](SUBMISSION.md)).
