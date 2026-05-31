---
title: Chạy Lab
---

# Hướng dẫn chạy Lab đầu tiên

Xin chào! Lý thuyết đã đủ rồi. Bây giờ là lúc chúng ta thực sự biến các khái niệm toán học thành những dòng code đang chạy. Trong phần Labs này, bạn sẽ được tự tay huấn luyện mô hình trên dữ liệu ruồi giấm (synthetic data) và quan sát trực tiếp các vết độ trễ (latency traces) của những Policy khác nhau.

## 1. Môi trường (Environment)

Mã nguồn của khóa học được tối giản hóa đến mức tối đa để tránh sự phức tạp của các framework khổng lồ như Fairseq hay HuggingFace. Mọi thứ được viết bằng PyTorch thuần túy.

Đầu tiên, hãy đảm bảo bạn đã clone repo và cài đặt các thư viện cơ bản. Bạn chỉ cần Python 3.8+ và PyTorch:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Sau đó chạy test:

```bash
pytest
```

## 2. Cấu trúc thư mục Labs

Phần code thực hành cốt lõi nằm ở thư mục `src/`. Bạn sẽ thấy các thành phần chính như sau:
- `data.py`: Script sinh dữ liệu tổng hợp (Synthetic Data với Reordering).
- `model.py`: Chứa định nghĩa kiến trúc mạng `EncoderRNN`, `AttentionDecoderRNN` và hàm `train()`.
- `policy.py`: Nơi định nghĩa các class Policy: `WaitKPolicy`, `LocalAgreementPolicy`,... (Đây là nơi bạn sẽ code thêm các policy mới).
- `simultaneous.py`: Vòng lặp giả lập môi trường streaming (thực hiện liên tục các hàm READ/WRITE).
- `run_experiment.py`: Script chính ráp nối tất cả lại với nhau và in ra kết quả.

## 3. Chạy Lab: Huấn luyện và Đánh giá

Hãy chạy câu lệnh sau ở thư mục gốc:

```bash
python examples/compare_policies.py
```

### Chuyện gì đang xảy ra dưới nền?

Script này sẽ tự động thực hiện một Pipeline trọn vẹn:
1. **Sinh dữ liệu:** Tạo ra 10,000 cặp câu nguồn-đích với cấu trúc S-V-O-T bị đảo ngược thành S-O-V-T.
2. **Train Model:** Huấn luyện nhanh một mô hình GRU nhỏ trong khoảng 10-20 epoch. Bạn sẽ thấy loss giảm dần trên terminal. Mất chưa tới 1 phút trên CPU.
3. **Simulate (Giả lập):** Chọn ngẫu nhiên vài câu chưa từng thấy (Test set) và đưa vào môi trường giả lập luồng.
4. **Áp dụng Policies:** Lần lượt ép mô hình chạy qua các Policy: `Wait-2`, `Wait-4`, và `Local Agreement`.

### Đọc Hiểu Kết Quả Output

Đừng bỏ lỡ bất kỳ dòng log nào, đó chính là "vàng" của bài lab. Bạn sẽ thấy output có dạng như sau:

```text
==================================================
Câu nguồn: s_2 v_5 o_1 t_8
Bản dịch đúng (Reference): s_2 o_1 v_5 t_8
--------------------------------------------------
Chạy với Policy: Wait-2
Bản dịch sinh ra: s_2 o_2 v_5 t_8  <-- SAI! (Ảo giác o_2 thay vì o_1)
Trace g(t) (read_positions): [2, 3, 4, 5]
Latency Metrics: AP = 0.70, AL = 2.25

Chạy với Policy: Wait-4
Bản dịch sinh ra: s_2 o_1 v_5 t_8  <-- ĐÚNG!
Trace g(t) (read_positions): [4, 5, 5, 5]
Latency Metrics: AP = 0.95, AL = 3.50

Chạy với Policy: Local Agreement (N=2)
Bản dịch sinh ra: s_2 o_1 v_5 t_8  <-- ĐÚNG!
Trace g(t) (read_positions): [2, 4, 5, 5]
Latency Metrics: AP = 0.80, AL = 2.75
==================================================
```

## 4. Phân tích kết quả Lab (Crucial Step)

Hãy nhìn vào output trên với tư cách là một nhà nghiên cứu:

1. **Tại sao Wait-2 sai?**
   Nhìn vào Trace `[2, 3, 4, 5]`. Để sinh ra token đích thứ 2 (là `o_1`), Wait-2 chỉ cho phép hệ thống đọc đến token nguồn thứ $g(2) = 3$ (tức là `s_2 v_5 o_1`). Tuy nhiên, do mạng Neural bị hạn chế năng lực hoặc do học chưa đủ sâu, khi chỉ thấy `v_5`, nó đã hoảng loạn và đoán bừa ra `o_2`.

2. **Wait-4 đúng, nhưng...**
   Wait-4 bắt hệ thống chờ đến 4 token: `[4, 5, 5, 5]`. Ở bước $t=2$, $g(2) = 5$, hệ thống đã nghe trọn vẹn toàn bộ câu nguồn. Hiển nhiên nó dịch đúng 100%. Tuy nhiên cái giá phải trả là Độ trễ $AL = 3.50$ (Rất cao, gần giống offline).

3. **Sự kỳ diệu của Local Agreement:**
   Dịch đúng như Wait-4, nhưng Trace lại thông minh hơn: `[2, 4, 5, 5]`.
   - Ở bước 1, nó tự tin xuất `s_2` chỉ với 2 token đầu ($g(1)=2$).
   - Ở bước 2, nó cảm thấy bất ổn (do bị gãy Local Agreement), nó chủ động ngậm miệng giữ lệnh READ cho đến khi đọc đến 4 token nguồn, lúc đó nó mới thốt ra `o_1`.
   - Kết quả: Dịch đúng 100%, mà độ trễ $AL = 2.75$ lại thấp hơn Wait-4 ($3.50$). Đây chính là định nghĩa của Pareto Optimal (Tối ưu điểm cân bằng)!

## Tự ngẫm (Reflection)

Xin chúc mừng! Bạn đã vừa chứng minh bằng thực nghiệm một trong những Paper quan trọng nhất của lĩnh vực này. Không cần hàng nghìn GPU, không cần mô hình tỷ tham số, cơ chế lõi của vạn vật đều nằm ở đây.

Trong bài Lab tiếp theo, chúng ta sẽ xem cách vọc vạch và phá vỡ codebase này để thiết kế những thứ của riêng bạn.
