---
title: Chạy lab và đọc output
---

# Chạy lab và đọc output

Lab chính của repo nằm ở `examples/compare_policies.py`. Script này tạo synthetic data, train một model nhỏ, chọn vài test examples, chạy nhiều policy và in quality-latency metrics.

## Cài đặt môi trường Python

Tạo virtual environment và cài package ở chế độ editable:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Sau đó chạy test:

```bash
pytest
```

Nếu test pass, bạn có thể chạy demo:

```bash
python examples/compare_policies.py
```

## Output cần đọc như thế nào

Với mỗi source sentence, script in `SRC`, `REF`, predicted tokens của từng policy, AP, AL, F1, `read_positions` và `actions`.

Đừng chỉ nhìn F1. Hãy đọc theo thứ tự:

1. Reference cần target order nào?
2. Policy phát token ở những source positions nào?
3. AP và AL có thấp hơn policy khác không?
4. F1 có giảm khi latency giảm không?
5. Action trace có bursty không?
6. Nếu policy sai, nó sai vì phát quá sớm hay vì model chưa học tốt?

## Thử nghiệm đầu tiên

Bài tập đơn giản nhất là thay `WaitKPolicy(k=2)` thành các giá trị khác:

```python
WaitKPolicy(k=1)
WaitKPolicy(k=3)
WaitKPolicy(k=4)
```

Kỳ vọng là `k` nhỏ hơn sẽ giảm latency nhưng tăng rủi ro sai. `k` lớn hơn thường an toàn hơn nhưng chậm hơn. Nếu kết quả không theo trực giác, hãy kiểm tra từng sentence. Có thể sentence đó gần monotonic nên `k` nhỏ vẫn ổn, hoặc model chưa đủ tốt nên `k` lớn cũng không cứu được quality.

## Thử nghiệm thứ hai

Thay threshold của `ConfidencePolicy`:

```python
ConfidencePolicy(threshold=0.70)
ConfidencePolicy(threshold=0.90)
```

Threshold thấp thường cho phép phát sớm hơn. Threshold cao thường bảo thủ hơn. Nhưng nếu model confidence không calibrated, thay threshold có thể tạo hành vi bất ngờ. Đây là lý do confidence không nên được xem là truth.

## Điều cần giữ lại

Lab không chỉ để chạy cho có output. Nó là công cụ đọc hành vi. Mỗi dòng `read_positions` và `actions` là bằng chứng về cách policy vận hành. Hãy học cách giải thích trace trước khi tối ưu metric.
