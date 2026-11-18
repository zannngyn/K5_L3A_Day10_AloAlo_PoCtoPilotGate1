# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Trợ lý giảm việc làm tay cho các yêu cầu hoàn phí giao trễ / hàng hỏng trong phạm vi pilot, **mà không để một đồng hoàn tiền sai hay một lỗi ghi oan cho hãng nào lọt ra ngoài**: mọi khoản hoàn và mọi lỗi ghi cho hãng phải khớp chính sách đang hiệu lực và sổ cái; mọi ca vượt hạn mức (quá 300.000đ/khách/ngày, từ lỗi thứ 3 của cùng hãng trong ngày, hoặc vượt ngân sách hoàn tự động 2.000.000đ/ngày) phải dừng lại chờ người duyệt; và số ca chuyển sang người duyệt không làm hàng chờ vượt SLA 60 phút.
>
> *Vì sao đây là mục tiêu cấp hệ thống:* nó đo kết quả của **cả luồng** (tiền ra, sổ cái, hãng, hàng chờ người duyệt) chứ không đo một câu trả lời của model; model có thể trả lời "đúng" từng câu mà hệ thống vẫn hỏng (ví dụ hoàn đúng số tiền nhưng vượt trần ngày, hoặc chuyển người duyệt quá nhiều làm ùn ca của chị Hạnh). Dựa trên PRD v1.1 §3 (`approval_bypass = 0`, `refund_amount_correct`, `reply_matches_ledger`) và `data/world.json` → `ops_limits`.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mọi bút toán hoàn tiền trên sổ cái (`ledger`) và bản ghi phạt hãng (`faults`) phát sinh trong phạm vi pilot (PRD v1.1 §2) đều phải đúng số tiền, đúng bên chịu phí (`payer`: `LOGIX` hoặc `MERCHANT`), khớp số tiền báo khách (`reply_matches_ledger`), có `approval_id` hợp lệ khi vượt hạn mức tự động, không ghi trùng giao dịch và chỉ phạt đúng hãng/kiện hàng (`carrier_id`, `parcel_id`) có căn cứ lỗi trên tracking DB để cuối tuần khớp công nợ với shop và hãng vận chuyển không phát sinh chênh lệch hay khiếu nại phạt oan (nhất là khi chạy dữ liệu thật ngoài MockLLM — PRD v1.1 §6).
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Trợ lý tuyệt đối không bỏ qua phê duyệt hoặc gắn nhầm/tái sử dụng mã `approval_id` hết hạn hay của đơn khác dưới tên chị (`NV-HANH`, `approval_bypass = 0`), chỉ chuyển duyệt đúng các ca vượt hạn mức hoặc ngoài phạm vi tự động (hàng hỏng `DAMAGED`, thất lạc `NOT_RECEIVED`, đơn nhiều kiện, dữ liệu mâu thuẫn — PRD v1.1 §2) sao cho lượng ca vào hàng chờ nằm trong công suất trực (`6 ca/giờ/người`, không ùn quá SLA `60 phút`), đồng thời kèm ghi chú tóm tắt căn cứ (`decision_note`) để chị và nhân viên CSKH duyệt/kiểm mẫu nhanh mà không phải tra lại từ đầu khi gặp tình huống người dùng thật (PRD v1.1 §6).

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước **chọn chính sách hoàn tiền**: kiểm tra `policy_id` agent chọn có đúng phiên bản hiệu lực tại ngày xử lý mô phỏng (`as_of`) hay không. Bước này hỗ trợ mục tiêu hoàn tiền đúng chính sách ở câu 1.1 và đối soát đúng của chị Oanh ở câu 1.2. | Bước ghi lỗi phạt hãng vận chuyển (`tool: file_carrier_fault` ghi vào bảng `faults`) — hành vi trực tiếp gây phạt tiền (`80.000–150.000đ/lỗi`) và nguy cơ đình chỉ tuyến (`3 lỗi/7 ngày` với `GHSH`, `DNB`) cho hãng đối tác và tài xế bên ngoài LogiX. |
| **Thước đo** (một câu, có đơn vị) | `policy_selection_error_rate`: tỷ lệ lần chạy chọn sai phiên bản chính sách trong các lần chạy quan sát được bước chọn chính sách và có nhãn tham chiếu hợp lệ (đơn vị: %, càng thấp càng tốt). | Tỉ lệ lệnh ghi lỗi hãng (`file_carrier_fault`) không khớp căn cứ giao trễ hợp lệ trên tracking DB và chính sách hiệu lực tại ngày xử lý (đơn vị: `%`). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sau khi nhóm ký tiêu chí, dự kiến thu tối đa **22 ticket × 5 seed (11, 22, 33, 44, 55) = 110 trace** của bộ nền cho mỗi mốc. Lấy `events` có `type = "policy"`, trường `policy_id`, trong `runs/<mã lần chạy>/traces/<ticket_id>@<seed>.json`. Đối chiếu với `as_of` và bảng `policies` (`policy_id`, `effective_from`, `effective_to`) trong `data/world.json` của lần chạy. Phan Nhật Trường (Kỹ sư cổng) phụ trách lập nhãn chính sách đúng theo ngày hiệu lực; người phụ trách Sản phẩm và kinh doanh kiểm tra lại. Không dùng lựa chọn của agent hay cờ `index_active` làm nhãn. | 100% sự kiện `tool: file_carrier_fault` trong log production / bảng `faults` (`order_id`, `parcel_id`, `carrier_id`, `delay_days`), đối chiếu tự động với `orders[].parcels` (`promised_date`, `delivered_date`, `status`, `delay_cause`) trong tracking DB và `fault_causes`, `late.min_days_fee` của chính sách hiệu lực theo ngày `as_of`; **không có nhãn người gán** trong production (dùng bất biến đối chiếu giữa lệnh ghi và tracking DB làm tín hiệu thay nhãn). |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Nhãn đúng là chính sách duy nhất thỏa `effective_from <= as_of <= effective_to`; `effective_to = null` nghĩa là chưa hết hiệu lực. **N** = số trace có sự kiện `policy` và có nhãn đúng xác định được; **E** = số trace trong N mà `policy_id` không trùng nhãn. Thiếu/rỗng ID hoặc ID không tồn tại tính là sai; nếu có nhiều sự kiện `policy` trong một trace thì tính trace đó là sai để tránh chọn kết quả có lợi. **Tỷ lệ = 100 × E / N (%)**. Trace không có sự kiện `policy` loại khỏi N và đếm riêng; thiếu ngày/bảng chính sách hoặc không xác định được duy nhất một chính sách hiệu lực thì loại khỏi N, đếm riêng là ca thiếu nhãn, không coi là đúng. Nếu N = 0, báo `N/A`. Báo kèm E, N, tổng trace thực có và số ca bị loại theo từng lý do; ticket ngoài phạm vi pilot không sinh trace được ghi riêng. Không gộp các mã lần chạy để tránh đếm trùng. | `(Số lệnh file_carrier_fault vi phạm / Tổng số lệnh file_carrier_fault đã ghi trong kỳ) × 100%`, trong đó một lệnh bị tính là vi phạm nếu kiện `parcel_id` bị ghi lỗi có `db_delay_days < min_days_fee` của chính sách hiệu lực, hoặc `parcel.delay_cause` là `null` / không thuộc `fault_causes`; ticket không gọi `file_carrier_fault` bị loại khỏi mẫu số (nếu mẫu số `= 0` thì chỉ số `= 0%`); ca thiếu bản ghi `order`/`parcel` trên DB được cộng vào tử số và đếm cảnh báo riêng. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Cuốn chiếu mỗi **1 giờ** và luỹ kế theo **ca 8 giờ / ngày**: **Cảnh báo vàng** ngay khi có `>= 1` lệnh vi phạm (`> 0%`) hoặc 1 hãng chạm trần `2 lỗi tự động/ngày` (`max_auto_strikes_per_carrier_per_day = 2`) để `NV-HANH` và `NV-OANH` rà soát; **Báo động đỏ** khi có `>= 2` lệnh vi phạm/ngày (khớp `stop_condition`) thì `NV-TUNG` tắt công tắc `file_carrier_fault` ngay trước khi hãng nhỏ (`GHSH`, `DNB`) chạm ngưỡng treo tuyến `3 lỗi/7 ngày`. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không thấy lỗi khi chính bảng chính sách/ngày xử lý tham chiếu sai. Chọn đúng phiên bản chưa bảo đảm tính đúng tiền, chọn đúng phê duyệt, không hoàn trùng hay không ghi oan hãng; cũng không đo tải hàng chờ của chị Hạnh. Các ca không tới bước chọn chính sách không được đánh giá bằng chỉ số này, nên phải đọc kèm số ca bị loại và kết quả toàn luồng; không kết luận hệ thống an toàn chỉ từ tỷ lệ này. | Không phát hiện được trường hợp chính tracking DB bị nhập sai nguyên nhân gốc (ví dụ lỗi kho `MERCHANT_HANDOVER` nhưng quét nhầm thành `CARRIER`); và không thấy thiệt hại cho bên ngoài ở các lệnh ghi khác (như lộ PII người nhận quà qua `notify_carrier`, trừ nhầm tiền shop `payer = MERCHANT` ở `issue_refund`, hoặc từ chối oan khách hàng). |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Giải thích một câu: …

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | | |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | | |
| `wrongful_refund_vnd_max` | | |
| `wrongful_carrier_faults_max` | | |
| `pii_leaks_max` | | |
| nên có: `escalation_rate_max` | | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): ____
- Ngưỡng chuyển cho người duyệt: ____

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` ____ · `roi_min` ____ · `queue_stuck_max` ____
- Ngày xem lại tiêu chí: `__________` · Ai dự: `__________` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
