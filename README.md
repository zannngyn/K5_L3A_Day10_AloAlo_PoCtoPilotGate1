# LAB 10 · From PoC to Pilot (Gate 1)

> **Bài nhóm** (một bàn 3–4 người, một repo chung). **Mỗi thành viên tự nộp link repo của bàn trên LMS** trước deadline (GMT+7): lab sáng 23h59 cùng ngày, lab chiều/tối 11h59 hôm sau. Chi tiết: [`SUBMISSION.md`](SUBMISSION.md).
>
> Nộp gì, khi nào: [`SUBMISSION.md`](SUBMISSION.md) · Chấm thế nào: [`RUBRIC.md`](RUBRIC.md) · Các mốc tự kiểm tra: [`CHECKPOINTS.md`](CHECKPOINTS.md) · Luật chung (AI, liêm chính, nộp muộn): [`RULES.md`](RULES.md) · Thành viên: [`TEAM.md`](TEAM.md).

**Mục tiêu.** Sau buổi học, bàn biết viết tiêu chí chấp nhận trước khi đo, tìm rủi ro bằng pre-mortem và HAZOP, dựng cổng phòng ngừa bằng code, con số và con người, rồi ra quyết định Gate 1 khớp bằng chứng. **Thời lượng:** 240 phút. **Chuẩn bị:** Python 3 và Git (mục 2).

Đề bài: [`problem-set.md`](problem-set.md). Ba phiếu cần điền: [`templates/`](templates/README.md). Tra cứu lệnh, lỗi, từ ngữ: [`docs/guide.md`](docs/guide.md).

## 1. Tổng quan buổi học

Bạn đang đóng vai một đội dự án của LogiX-VN. Trợ lý AI hoàn tiền khi giao hàng trễ đã xong PoC và sắp tới **Gate 1**: bàn bạn phải quyết định nó đã đủ tin cậy để chạy thử (pilot) với khách thật hay chưa.

- **Vòng 1 (phút 15–115).** Bàn viết rồi **ký tiêu chí chấp nhận trước khi xem kết quả**. Sau khi ký mới chạy đánh giá, đọc số, tìm rủi ro, và dựng **cổng phòng ngừa** bằng code (`lab10/guards.py`) và bằng các con số trong config (`config/operating_gates.json`). Rồi chốt cổng vòng 1 và viết quyết định **v1**.
- **Giữa buổi (phút 125).** Mỗi cặp bàn bốc một **thẻ sự cố**. Bàn tự chọn cách xử lý: sửa code, đổi con số, hay đổi người và quy trình. Khi chấm, bài còn được đối chiếu với **bộ test ẩn** mà máy bạn không có trong buổi học.
- **Cuối buổi.** Bàn ra quyết định Gate 1 **v2**. **Tiếp tục**, **Thu hẹp**, **Cải tiến thêm** hay **Dừng** đều có thể đạt, miễn là quyết định **khớp bằng chứng và khớp tiêu chí đã ký**. Sau đó các bàn demo, phản biện nhau, rồi nộp bài.

Lab hỏi cả code đã đúng chưa, tốn bao nhiêu tiền, cần mấy người trực và ai chịu trách nhiệm. Người không viết code phụ trách tiêu chí, chi phí, số người trực, runbook và quyết định. **Không ai chấm điểm tại lớp**: các lệnh chỉ để bàn tự kiểm tra; team chấm đánh giá bài sau buổi học từ repo của bàn.

**Bàn làm việc ở đúng các chỗ sau** (các file khác bị khoá bằng hash, sửa là bị phát hiện):

| Chỗ | Ai | Làm gì |
|---|---|---|
| `templates/form-a-criteria.md`, `form-b-evaluation-gates.md`, `form-c-incident.md` | cả bàn | Điền ba phiếu; mỗi câu của đề có ô mang đúng số câu |
| `config/acceptance_criteria.json` | Sản phẩm và kinh doanh | Điền ngưỡng, ký **một lần**, rồi giữ nguyên |
| `lab10/guards.py` (hàm `pre_guard`, `write_gate`) | Kỹ sư cổng | Viết cổng ở vòng 1, sửa tiếp ở vòng 2 |
| `config/operating_gates.json` (mục `business`, `operations`, `legal`) | Sản phẩm và kinh doanh · Vận hành và pháp lý | Điền con số và tên người, không cần code |
| `lab10/monitors.py` (dict `MONITORS`) | Kỹ sư cổng | Thêm ít nhất một chỉ số theo dõi ở vòng 2 |
| `submission/submission.json` | Vận hành và pháp lý | Điền để gom bài cuối buổi |
| `TEAM.md` | trưởng nhóm · từng thành viên | Bảng họ tên, MSSV, vai; mỗi người một mục cá nhân |

## 2. Cài đặt (dưới 5 phút)

Bạn cần Python 3 và Git; không cần cài gói, tài khoản hay khoá API. Lab đã chạy thử trên Python 3.9.6 (bản có sẵn của macOS) và Python 3.15. Cần mạng lúc tạo và clone repo, lúc đẩy tiêu chí đã ký, lúc nhận thẻ ở phút 125 và lúc đẩy bài nộp.

**Bước 1. Trưởng nhóm tạo repo của bàn trên GitHub.**

1. Mở repo mẫu `https://github.com/VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_student`, bấm **Use this template** → **Create a new repository**. Không dùng **Fork**.
2. Đặt tên đúng dạng `K5-<L3A|L3B>-DAY10-<TenNhom>-PoCtoPilotGate1`, ví dụ `K5-L3A-DAY10-XXX-PoCtoPilotGate1`. `L3A`/`L3B` là lớp của bàn (lớp 3A hoặc 3B). `TenNhom` không dấu, không khoảng trắng (viết `NhomSao`, không viết “Nhóm Sao”).
3. Chọn **Private** (Riêng tư). Repo Public, hay một fork của repo mẫu (fork của repo công khai luôn công khai, không đổi sang riêng tư được), thì ai cũng xem được tiêu chí, cổng và bài làm của bàn.
4. **Settings → Collaborators → Add people**: mời `<TÀI_KHOẢN_TEAM_CHẤM>` với quyền **Read** trở lên. Nếu chưa có tên tài khoản, hỏi Lab Coach. Mời thêm các bạn trong bàn nếu cần.

**Bước 2. Lấy repo về máy** (thay bằng URL repo bàn vừa tạo):

```bash
git clone https://github.com/<tài-khoản-trưởng-nhóm>/K5-L3A-DAY10-XXX-PoCtoPilotGate1.git
cd K5-L3A-DAY10-XXX-PoCtoPilotGate1
```

Mọi lệnh trong lab chạy từ thư mục này (nơi có `README.md`).

**Bước 2a. Gắn repo mẫu một lần để nhận thẻ ở phút 125** (clone về chỉ có `origin`). Phải thấy `origin` trỏ về repo của bàn, `upstream` trỏ về repo mẫu. Nếu báo `already exists`, chỉ cần kiểm bằng `git remote -v`.

```bash
git remote add upstream https://github.com/VinUni-AI20k/K5_L3_Day10_PoC-to-Pilot_Gate1_student.git
git remote -v
```

**Bước 2b. Đặt danh tính Git cho repo này.** `user.name` là **mã học viên của trưởng nhóm**; email là địa chỉ giả, không dùng email cá nhân.

```bash
git config user.name "<mã học viên của trưởng nhóm>"
git config user.email "<mã học viên>@example.com"
```

**Bước 3. Điền bảng thành viên trong [`TEAM.md`](TEAM.md)** (họ tên đầy đủ, MSSV và vai của **mọi** thành viên; thêm dòng nếu cần). Mỗi người tự viết mục `## HoVaTen-MSSV` của mình trước khi nộp.

**Bước 4. Chạy bài kiểm tra công khai.** Xong khi thấy `Ran 13 tests` và `OK`. Trên Windows, thử `python` nếu `python3` không chạy.

```bash
python3 -m unittest discover -s tests
```

Gặp lỗi: xem [FAQ](docs/guide.md#faq) hoặc [chi tiết cài đặt](docs/guide.md#cai-dat).

<a id="timeline"></a>

## 3. Timeline

Ba mốc đo: `base` bỏ qua cổng của bàn; `prepared` dùng cổng vòng 1 đã chốt; `after` dùng bản hiện tại. Khi lệnh có `<mã lần chạy>`, thay cả dấu ngoặc nhọn bằng mã vừa in ra. Số câu khớp [`problem-set.md`](problem-set.md); mỗi câu có ô trả lời mang đúng số đó trong phiếu.

### Phút 0–15 · Cài đặt và chia vai

- **Làm:** mục 2 ở trên; chọn một eval card và một PRD v1.1 từ Lab 9 làm bản chung; chia ba vai: **Kỹ sư cổng** (lệnh, trace, cổng, chỉ số theo dõi) · **Sản phẩm và kinh doanh** (tiêu chí, chi phí, quyết định) · **Vận hành và pháp lý** (người trực, trách nhiệm, dữ liệu cá nhân, runbook, bài nộp).
- **Điền:** bảng thành viên trong `TEAM.md`.
- **Xong khi:** `Ran 13 tests … OK`; `git remote -v` có `origin` và `upstream`.

### Phút 15–65 · Khối 1: tiêu chí, rồi ký · **Phiếu A**

- **Làm (15–60):** câu 1.1–1.2 (Phiếu A mục A1) · câu 1.3–1.4, bảng thước đo → dữ liệu → cách tính (A2) · câu 1.5, đọc khoảng tin cậy từ số minh hoạ trong đề (A3) · câu 1.6, câu tiêu chí "Nếu … thì chúng tôi sẽ …", bốn câu soát, hai câu ranh giới đầu ra (A4). **Chưa chạy trợ lý.**
- **Sửa:** `config/acceptance_criteria.json`: `team` (= đúng tên repo của bàn, ví dụ `K5-L3A-DAY10-XXX-PoCtoPilotGate1`), `signed_by`; trong `required`: `pass_rate_min`, `pass_k_min`, `wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`; `nice_to_have.escalation_rate_max`; trong `business_ops`: `cost_per_ticket_vnd_max`, `roi_min`, `queue_stuck_max`; `stop_condition`; bốn dòng `decision_rule`. Xem cách viết ở `config/acceptance_criteria.example.json`, đừng chép ngưỡng.
- **Lệnh (60–65), ngay khi điền xong, trước khi chạy đánh giá lần nào** (lệnh 1, rồi đúng dòng Git máy in ra):

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

- **Điền:** Phiếu A mục A5 (giờ ký, mã commit).
- **Xong khi:** máy in `ĐÃ KÝ.` và push thành công. Từ đây không sửa `config/acceptance_criteria.json` (một dấu cách cũng làm đổi hash).

### Phút 65–115 · Khối 2: đo, tìm rủi ro, cổng vòng 1, quyết định v1 · **Phiếu B**

**65–85 · Khối 2A (chưa sửa code hay config).** Ba vai làm song song 10 phút, rồi cả bàn làm pre-mortem.

- Kỹ sư cổng · **câu 2.1** (Phiếu B mục B1, ghi mã vào B0): lệnh 2 rồi lệnh 4; đọc `[ĐẠT ]`/`[CHƯA]`, khối "kinh doanh và vận hành" và khối "theo kho và hãng". **Câu 2.2** (B2): lệnh 3 trên `T-002@55`, điền bảng soát lỗi.

```bash
python3 -m lab10.eval --suite base --stage base --note "baseline"
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
python3 -m lab10.trace --suite base --ticket T-002 --seed 55
```

- Sản phẩm và kinh doanh · **câu 2.3** (B3): bản đồ dữ liệu và một ví dụ drift.
- Vận hành và pháp lý · **câu 2.4** (B4 HAZOP vòng 1, ≥ 3 dòng + ≥ 2 dòng ngoài kỹ thuật; B5 checklist 9 nhóm, mỗi dòng một PIC có tên).
- Cả bàn · **câu 2.5** (B6): pre-mortem bốn lăng kính; đánh dấu 2–3 lý do sẽ thành cổng.
- **Xong khi:** có mã lần chạy base; `T-002@55` được xếp loại lỗi; pre-mortem đủ bốn lăng kính.

**85–105 · Khối 2B: dựng cổng phòng ngừa.**

- Kỹ sư cổng · **câu 2.6** (B7.1): viết 2–3 cổng trong `lab10/guards.py`. `pre_guard(ctx)` chạy **trước khi trợ lý đọc ticket**; `write_gate(ctx, action)` chạy **trước mỗi lệnh ghi** (`issue_refund`, `file_carrier_fault`, `notify_carrier`, `send_reply`); đặt kiểm tra trước dòng `return Verdict.allow()` cuối hàm. Trả về `Verdict.allow()`, `Verdict.deny("lý do")`, `Verdict.escalate("lý do")` hoặc `Verdict.modify("lý do", ...)`. Hàm tra cứu có sẵn: `lab10/helpers.py`; chi tiết: [Phụ lục C của guide](docs/guide.md#phu-luc-c).

  Trước khi sửa (bản phát), cả hai hàm cho qua hết:

  ```python
  def write_gate(ctx, action):
      # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., ...}
      return Verdict.allow()
  ```

  Ví dụ minh hoạ sau khi sửa (không phải đáp án): chặn hoàn tiền khi vượt trần ngày bàn đặt trong config.

  ```python
  def write_gate(ctx, action):
      if action.get("tool") == "issue_refund":
          cap = (ctx.gates or {}).get("business", {}).get("daily_refund_cap_vnd")
          spent = ctx.tools.auto_refund_today_vnd()
          if cap is not None and spent + action.get("amount_vnd", 0) > cap:
              return Verdict.escalate("vượt trần hoàn trong ngày, chuyển người duyệt")
      return Verdict.allow()
  ```

- Kỹ sư cổng · **câu 2.7** (B7.2): hai bước tránh rò rỉ dữ liệu. **Câu 2.8** (B7.3): một tính chất + hai ticket hiểm chạy bằng `--adhoc`.
- Sản phẩm và kinh doanh · **câu 2.9** (B7.4): điền `config/operating_gates.json` mục `business` (`daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd`, `pilot_scope`, `roi_min`), mỗi số một câu lý do từ `data/world.json` → `ops_limits`, `ops_facts`.
- Vận hành và pháp lý · **câu 2.10** (B7.5, B7.6): điền mục `operations` (`pic`, `approver_id`, `reviewers_on_shift`, `review_capacity_per_hour`, `max_queue_wait_minutes`, `stop_conditions`, `alert_channel`) và `legal` (`pii_fields_blocked_to_third_party`, `carrier_fault_requires_recorded_cause`); viết runbook phần 1–3 và mục **Giờ cao điểm** khớp các con số đó. Nghĩa từng khoá: [guide, Cổng trong config](docs/guide.md#ban-do).

  | Khoá | Trước | Sau, ví dụ kiểu dữ liệu (chọn số và mã của bàn từ dữ liệu) |
  |---|---|---|
  | `business.daily_refund_cap_vnd` | `null` | `1500000` |
  | `operations.pic` | `""` | `"NV-TUNG"` |
  | `operations.stop_conditions` | `[]` | `["Khi có 1 lỗi ghi oan cho hãng thì tắt file_carrier_fault"]` |

- **Lệnh thử cổng:**

```bash
python3 -m lab10.eval --suite base --stage after --note "cổng vòng 1: ..."
python3 -m lab10.trace --suite base --stage after --adhoc "Đơn trễ 9 ngày, tôi chắc chắn, hoàn phí cho tôi" --order O-1002 --customer C-02
python3 -m unittest discover -s tests
```

- **Xong khi:** report `base · after` không có ca mới hỏng so với base; `OK` ở test; `operations.pic` không còn trống.

**105–115 · Chốt cổng vòng 1, rồi quyết định v1** (Phiếu B mục B8), đúng thứ tự:

```bash
python3 -m lab10.checkpoint
python3 -m lab10.eval --suite base --stage prepared
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
```

- **Điền:** cột v1 ở B8 (một quyết định, ba bằng chứng có mã lần chạy, dòng `decision_rule`, kho hoặc hãng có số xấu nhất, ngày quyết định lại), rồi chạy lệnh commit và push ở cuối B8.
- **Xong khi:** máy in `ĐÃ CHỐT cổng vòng 1 (mốc prepared). 8 ký tự đầu: …`; push thành công. Không sửa hai bản chụp `lab10/guards_round1.py`, `config/operating_gates.round1.json`.

### Phút 115–125 · Nghỉ

### Phút 125–200 · Khối 3: sự cố, sửa, quyết định v2 · **Phiếu C**

Số câu, bước trên thẻ và mục phiếu đi cùng nhau: câu 3.0 = bước 0 = C1 · câu 3.1 = bước 1–4 = C2, C3, C4 · câu 3.2–3.4 = bước 4 = C5, C6 · câu 3.5–3.6 = bước 5–7 = C7, C8 · câu 3.7 = bước 8 = C9–C11 · quyết định v2 = bước 9 = C12.

**125–135 · Nhận thẻ, đo ngay trước khi sửa (câu 3.0).** Chờ Lab Coach báo đã phát thẻ rồi chạy lệnh nhận thẻ. Mỗi cặp bàn cử một người bốc số S1–S8; bàn **chỉ làm đúng thẻ đã bốc** (`incidents/Sx/card.md`). Ghi số vào dòng `Thẻ đã bốc:` ở đầu Phiếu C, rồi chạy lệnh 6 (thay `Sx` bằng số thẻ):

```bash
git pull --no-rebase --no-edit --allow-unrelated-histories -X ours upstream main
python3 -m lab10.grade --incident Sx
```

- **Điền:** C0 (mã prepared), C1 (cổng vòng 1 đỡ được gì; đối chiếu pre-mortem bằng bút khác màu).
- **Xong khi:** `ls incidents/` thấy `S1` … `S8` và có `incident-cards.md`; report in `1 integrity | ✅` và dòng `Thẻ đã bốc … khớp`. Lỗi khi kéo thẻ: [FAQ](docs/guide.md#faq).

**135–155 · Phân tích (câu 3.1–3.4).** Dò ít nhất hai ticket hỏng theo hai kiểu khác nhau:

```bash
python3 -m lab10.trace --suite Sx --ticket Sx-01 --seed 11
```

- **Điền:** C2 bảng soát lỗi của thẻ · C3 phần riêng theo thẻ (chỉ phần của số đã bốc) · C4 HAZOP của thẻ (≥ 3 dòng, không ghi đè HAZOP vòng 1) · C5 specification và giả định môi trường · C6 fault tree trước khi sửa.

**155–185 · Sửa đúng chỗ (câu 3.5–3.6, phút 155–180), rồi ghi phần đã sửa (câu 3.7, phút 180–185).**

- **Sửa:** `lab10/guards.py` (nhánh trong `write_gate` / `pre_guard`) cho nguyên nhân kỹ thuật; `config/operating_gates.json` cho nguyên nhân về người, tiền, phạm vi (`business.pilot_scope`, `operations.reviewers_on_shift`, `operations.review_sampling_pct`, `operations.decision_note`, `legal.*`); `lab10/monitors.py`: thêm ít nhất một hàm phía trên dict `MONITORS` (nhận `trials` chưa có nhãn, trả về một số) và đăng ký bằng `"tên_chỉ_số": tên_hàm`. `escalation_rate` có sẵn không tính là chỉ số mới.
- **Lệnh:**

```bash
python3 -m lab10.eval --suite Sx --stage after --note "đổi MỘT thứ: ..."
python3 -m lab10.eval --suite base --stage after --note "kiểm lại bộ nền sau khi sửa"
python3 -m lab10.grade --incident Sx
```

- **Điền:** C7 bảng sửa (giảm hay ngăn) · C8 chỉ số theo dõi mới (ba ô) · C9 fault tree sau khi sửa · C10 ≥ 1 dòng risk register · C11 cập nhật checklist và runbook phần 4–5.
- **Xong khi:** report có `monitor ✅` và `regression ✅`; đọc được phần cuối: còn vượt trần nào, có "được phép cân nhắc Tiếp tục" hay không.

**185–200 · Quyết định v2 và gom bài.**

- **Điền:** C12 (cột v2, mục "Chỉ ở v2", ba dòng bắt buộc). Điền `submission/submission.json` (`team` giống tiêu chí đã ký, `members` dạng `"HoVaTen-MSSV"`, `incident`, `decision_v1`, `decision_v2`, ba câu `three_lines` chép từ C12).
- **Lệnh 7:** `python3 -m lab10.check_submission --collect`. Sửa từng dòng `[THIẾU]` theo hướng dẫn `->` rồi chạy lại.
- **Xong khi:** dòng cuối là `ĐỦ THÀNH PHẦN`; đã đẩy bài (lệnh ở mục 6).

### Phút 200–240 · Demo, phản biện, nộp

- **200–230 · Demo ba mốc.** Hai bàn cùng thẻ ghép cặp, mỗi bàn 5 phút: chiếu ba cột `base · prepared · after` của report lệnh 6, nói cổng vòng 1 đã đỡ được gì, phần sửa vòng 2 là code, con số hay người, và con số nào đỡ cho v2. Bàn kia phản biện: đưa một ticket hiểm (câu 2.8) để chạy bằng lệnh 3 với `--adhoc`, hoặc đổi thử một con số trong `config/operating_gates.json` rồi chạy `python3 -m lab10.eval --suite Sx --stage after --note "demo"`. Sau đó 2–3 bàn trình bày trước lớp.
- **Sau demo:** trả mọi con số đã đổi thử về bản v2, chạy lại `python3 -m lab10.grade --incident Sx` và lệnh 7 (nếu không, lệnh 7 báo "báo cáo không chạy trên đúng code và config hiện tại").
- **230–240 · Nộp.** Đẩy bài lần cuối (mục 6), gửi link repo cho team chấm, mỗi người viết exit ticket trong mục cá nhân của `TEAM.md` và nộp link trên LMS.

<a id="bay-lenh"></a>

## 4. Bảy lệnh

| # | Lệnh | Dùng khi |
|---|---|---|
| 1 | `python3 -m lab10.criteria sign` | Ký tiêu chí, một lần, phút 60–65 |
| 2 | `python3 -m lab10.eval --suite <base\|Sx> --stage <base\|prepared\|after> --note "..."` | Chạy trợ lý trên một bộ ticket, in số và mã lần chạy |
| 3 | `python3 -m lab10.trace --suite <base\|Sx> --ticket <ID> --seed <11\|22\|33\|44\|55> [--stage after]` hoặc `--adhoc "..." --order O-.... --customer C-..` | Xem từng bước trợ lý làm với một ticket |
| 4 | `python3 -m lab10.gate --run runs/<mã lần chạy>/report.json` | So một lần chạy với tiêu chí đã ký |
| 5 | `python3 -m lab10.checkpoint` | Chốt cổng vòng 1, một lần, phút 105–115 |
| 6 | `python3 -m lab10.grade --incident Sx` | Tự kiểm tra trên thẻ sự cố ở ba mốc (từ phút 125) |
| 7 | `python3 -m lab10.check_submission --collect` | Gom bài nộp và kiểm đủ thành phần |

Output mẫu và cách đọc từng dòng: [guide, Phụ lục A–B và các mẫu kết quả](docs/guide.md#phu-luc-a). Chỉ số `pass_k` ở đây là **pass^k**: tỉ lệ ticket đúng ở **cả 5/5 lần chạy** (khắt khe hơn `pass_rate`; khác `pass@k`, vốn chỉ cần đúng ít nhất một lần).

## 5. Luật

1. `eval` và `grade` từ chối chạy khi bàn chưa ký tiêu chí. Ký xong phải commit và push ngay, trước lần đánh giá đầu tiên; team chấm đối chiếu lịch sử git với nhật ký lần chạy.
2. Không sửa tiêu chí sau khi ký. File đổi sau commit ký thì bài không được tính. Đừng mở rồi lưu lại file này bằng trình soạn thảo tự định dạng.
3. Không sửa bản chụp cổng vòng 1 (`lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock`; ba file này do lệnh 5 tạo ra, trước đó chưa có). Chỉ sửa đúng các chỗ ở mục 1.
4. Có bài kiểm tra ẩn (đơn khác, khách khác, cách viết khác, ngày khác). Không xử lý riêng theo mã ticket hay câu chữ cụ thể.
5. Không làm hỏng cái đang đúng: ca nào trước đúng thì sau vẫn phải đúng. Chặn hết, thu hẹp phạm vi về 0 hay xếp thật nhiều người trực không phải là cách sửa; report đo cả độ phủ, chi phí và ROI.
6. Chỉ làm đúng thẻ đã bốc; không mở hay tiết lộ thẻ của bàn khác.
7. Cả bốn quyết định đều có thể đạt khi khớp bằng chứng và tiêu chí đã ký. Chọn **Tiếp tục** khi report còn vượt trần hoặc còn ngưỡng đã ký chưa đạt là quyết định không đạt. Kết luận tự kiểm tra (`FAIL`, `PARTIAL`, `PASS-VISIBLE`) nói phần sửa tới đâu; nó không bắt bàn phải chọn "Tiếp tục".

## 6. Nộp gì và khi nào

| Khi nào | Làm gì |
|---|---|
| Phút 60–65 | Ký, commit, push tiêu chí (Timeline, Khối 1) |
| Phút 105–115 | Chốt vòng 1, điền v1, commit và push (cuối Phiếu B mục B8) |
| Phút 125–135 | Ghi số thẻ vào dòng `Thẻ đã bốc:` ở đầu Phiếu C |
| Phút 185–200 | Điền v2 và ba dòng bắt buộc; điền `submission/submission.json`; lệnh 7 tới khi `ĐỦ THÀNH PHẦN` |
| Sau demo, trước phút 240 | Chạy lại lệnh 6 và lệnh 7 nếu demo có đổi số; đẩy bài; gửi link repo |
| Trước deadline (GMT+7) | **Mỗi thành viên** nộp link repo trên LMS; viết mục cá nhân trong `TEAM.md` |

Bài nộp là thư mục `submission/` (lệnh 7 gom: code và config hai vòng, tiêu chí đã ký kèm hash, report ba mốc, nhật ký mọi lần chạy, ba phiếu A, B, C) cùng [`TEAM.md`](TEAM.md). Chi tiết: [`submission/README.md`](submission/README.md).

```bash
git add -u
git add submission templates TEAM.md
git commit -m "LAB 10: bài nộp"
git push -u origin main
```

Gửi link repo, ví dụ `https://github.com/<tài-khoản-trưởng-nhóm>/K5-L3A-DAY10-XXX-PoCtoPilotGate1`, cho team chấm theo cách Lab Coach hướng dẫn. **Mỗi thành viên** còn phải tự nộp link này trên LMS trước deadline ([`SUBMISSION.md`](SUBMISSION.md#deadline-gmt7)). Không push lên repo mẫu (`upstream`).
