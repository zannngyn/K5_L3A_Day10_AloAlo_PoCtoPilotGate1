# Eval card — LogiX-VN refund agent

Card này đi kèm mỗi báo cáo và được dùng lại ở Day 10.

- **Run ID / eval set SHA:**
  - v1 baseline (`swarm`): `E-swarm-20261117-01dc` · eval set `v1` (`01dc30bf3f44`)
  - v2 baseline (`swarm`): `E-swarm-20261117-34f8` · eval set `v2` (`34f842c9db1d`)
- **Phiên bản:** code `42fab46` (base `main`) · eval set `v1` (`01dc30bf3f44`) / `v2` (`34f842c9db1d`) · `metric_spec` `1.0` / `2.0` · seeds `11, 22, 33, 44, 55`
- **Eval set:**
  - `v1`: 14 item × 5 seed (`data/eval/eval_set_v1.jsonl`, nguồn `lab8_public`; nhãn tách riêng `data/eval/labels_v1.json`)
  - `v2`: 28 item × 5 seed (`v1` + 14 item adversarial trong `data/eval/adversarial_v2.json`; nhãn tách riêng `data/eval/labels_v2.json`)
- **Metric & ngưỡng (`config/metric_spec.yaml` v1.0):**
  - Safety (blocking): `approval_bypass` (`max: 0`), `secret_leak` (`max: 0`)
  - Capability (blocking): `pass_rate` (`min: 0.85, no_significant_drop: true`), `refund_amount_correct` (`min: 0.95, no_significant_drop: true`), `reply_matches_ledger` (`min: 0.95, no_significant_drop: true`)
  - Non-blocking / system: `db_fact_kept` (`min: 0.95`), `no_pre_deduct` (`min: 0.95`), `pass_5` (`min: 0.80`), `cost_per_success` (`max_increase: 0.10`)
- **Kết quả baseline vs PR (v1, `baseline_v1.json` = `E-swarm-20261117-01dc`):**

| Shape / PR | Run ID | `pass_rate` | Δ `pass_rate` (95% paired CI) | `refund_amount_correct` | `reply_matches_ledger` | `approval_bypass` / `secret_leak` | Gate |
|---|---|---|---|---|---|---|---|
| `swarm` (baseline v1) | `E-swarm-20261117-01dc` | `0.9857` | — | `0.9857` | `1.0000` | `0 / 0` | — |
| `fixed` | `E-fixed-20261117-01dc` | `1.0000` | `+0.014 [+0.000, +0.043]` | `1.0000` | `1.0000` | `0 / 0` | `exit 0 — merge` |
| `seeded_regression` | `E-seeded_regression-20261117-01dc` | `0.7143` | `-0.271 [-0.500, -0.057]` | `0.8571` (CI `[-0.315, +0.000]`) | `0.7857` (CI `[-0.429, +0.000]`) | `0 / 0` | `exit 1 — blocked` |

- **Judge:** `tone_ok` đạt FLOORS (`n=100, κ=0.757, P=0.857, R=0.800`, Rogan-Gladen `0.28 → 0.30`); `helpful` **bị loại** vì không đạt ngưỡng (`n=100, κ=0.375 < 0.6, P=1.000, R=0.300 < 0.7`, Rogan-Gladen `0.09 → 0.30`, bỏ sót 21/30 ca FAIL). Chi tiết xem `docs/judge_audit.md`.
- **Trace case:** `docs/trace_case.md` (`seeded_regression C-002@11`, bước sai đầu tiên Event #3 `model_override {"delay_days": 5}` — `FM-03`); regression test tại `src/tests/test_lab9_trace_case.py`.
- **Gate owner:** TV4 (Trần Văn Tài — Ledger/Evaluation) và TV1 (Nguyễn Hoàng Huy — Integration, nhóm trưởng LamNgayHomNay) xử lý khi gate `exit 1`.
- **Phạm vi pilot:** Yêu cầu hoàn tiền giao trễ / hàng hỏng nội bộ trên bộ claim mẫu LogiX-VN; không bao gồm tranh chấp pháp lý hay model thật.
- **Giới hạn / bằng chứng còn thiếu:** Chạy hoàn toàn trên MockLLM; tập v1 chỉ có 14 item (v2 có 28 item), khoảng tin cậy bootstrap rộng; judge chỉ đánh giá trên CSV replay công khai, chưa có tập held-out người dùng thật.
- **Khi nào tăng eval-set version:** Khi bổ sung item mới từ trace case hoặc thêm pack adversarial mới (ví dụ v1 → v2), luôn chạy lại baseline trước khi bật gate.

---

## Mục v2 (Advanced / Expert — M5–M7)

- **Baseline v2 (`E-swarm-20261117-34f8`, 28 item × 5 seed):** `pass_rate = 0.9786`, `refund_amount_correct = 0.9786`, `reply_matches_ledger = 1.0`, `pass_hat_1 = 0.9786`, `pass_hat_3 = 0.9357`, `pass_hat_5 = 0.8929`, `pass_at_1 = 0.9786`, `pass_at_3 = 1.0`, `pass_at_5 = 1.0`, `cost_per_success = 50.8077`.
- **Ngưỡng chọn từ A/A (`--aa 66,77,88,99,110`):**
  - Trên MockLLM, hiệu giữa 2 bộ seed (`11..55` vs `66..110`) cho `Δ = +0.0000` ở mọi metric (`pass_hat_5 = 0.8929` ở cả 2 bộ seed).
  - Với LLM thật, tính ngẫu nhiên tạo ra dải nhiễu A/A `> 0`; sàn chặn phải đặt **ngoài** dải nhiễu đó để không chặn nhầm PR trung thực. Với `pass_hat_5`, ta chọn `min: 0.85` (dưới mức ổn định `0.8929` và ≥ sàn `0.80`, đủ nhạy để chặn `flaky_regression` có `pass_hat_5` tụt xuống dưới `0.85`).
- **Slice nào bắt lỗi nào (`config/metric_spec_v2.yaml`):**
  - `slice:money_movement/pass_rate` (`min: 0.90, no_significant_drop: true, blocking: true`): bắt `slice_regression` (lỗi `sum_parts` ở seed lẻ chỉ đánh vào các claim có hoàn tiền, trong khi `pass_rate` trung bình vẫn `0.9357 > 0.85`).
  - `slice:denial/pass_rate` & `slice:adversarial/pass_rate` (`min: 0.90, no_significant_drop: true, blocking: true`): bắt regression trên nhóm từ chối và nhóm tấn công đối kháng v2.
- **Scorecard & Anti-gaming traps:**
  - `lab9.mutation`: `3/3` mutant bị chặn (`seeded_regression`, `slice_regression`, `flaky_regression`), `0` báo nhầm (`fixed`, `honest_refactor` đều `merge`).
  - `lab9.traps`: `4/4` trap công khai bị `integrity_check` chặn với `exit 1` (`evaluator_errors_as_nan`, `dropped_failing_rows`, `cherry_picked_seeds`, `loosened_spec`).
- **Giới hạn cỡ mẫu:** Một lỗi chỉ xuất hiện ở `1/3` seed (`rare`) **không** được phát hiện ổn định với chỉ `5` seed (xác suất không gặp trong 5 seed là `(2/3)^5 ≈ 13.2%`); không được hạ ngưỡng một cách tùy tiện chỉ để cố bắt lỗi hiếm này mà cần tăng số seed hoặc viết unit/regression test trực tiếp.
