---
title: Wait-k và fixed chunk
---

# Wait-k và fixed chunk

Trước khi dùng policy phức tạp, ta nên học các baseline đơn giản. Baseline tốt không chỉ để so sánh điểm số. Nó buộc ta hiểu bài toán bằng một rule rõ ràng, dễ chạy và dễ phân tích.

## Wait-k

Wait-k là policy nổi tiếng trong simultaneous translation. Ý tưởng rất đơn giản: ban đầu đọc `k` source tokens, sau đó mỗi target step chỉ phát khi đã đọc đủ một lượng source theo độ trễ cố định.

Một cách viết rule là:

```text
g(t) = min(k + t - 1, n)
```

Với `t` là vị trí target token và `n` là source length. Nếu `k = 2`, token đầu tiên cần 2 source tokens, token thứ hai cần 3 source tokens, token thứ ba cần 4 source tokens, và cứ thế cho đến khi source hết.

Điểm mạnh của wait-k là dễ hiểu, dễ tái hiện và tạo lag khá đều. Điểm yếu là nó không biết câu nào khó hơn câu nào. Một câu gần monotonic có thể bị chờ quá lâu. Một câu có reordering mạnh có thể bị phát quá sớm.

## Fixed chunk

Fixed chunk policy đọc source theo từng đoạn kích thước `c`. Sau mỗi chunk boundary, policy cho phép phát một phần hypothesis đang được mở khóa.

Nếu wait-k giống như đi đều từng bước, fixed chunk giống như đọc từng đoạn rồi nói một đợt. Cách này gần với một số hệ thống xử lý batch nhỏ trong thực tế, nơi input đến theo segment hoặc frame chunk.

Điểm mạnh của fixed chunk là dễ tích hợp vào pipeline hệ thống. Điểm yếu là output có thể bursty. Người dùng có thể thấy hệ thống im lặng rồi phát nhiều token cùng lúc. AP hoặc AL có thể không phản ánh hết cảm giác này.

## So sánh trực giác

Wait-k ưu tiên độ đều. Fixed chunk ưu tiên ranh giới xử lý. Cả hai đều không nhìn vào nội dung hypothesis. Chúng không hỏi token đã ổn định chưa, cũng không hỏi model có tự tin không. Vì vậy, chúng là baseline tốt nhưng không phải lời giải cuối.

Trong repo, hai policy này đều được implement trong `src/simulst_edu/policies.py`. Khi chạy `examples/compare_policies.py`, bạn có thể thay `k` hoặc `chunk_size` để thấy latency-quality tradeoff thay đổi.

## Khi nào baseline vẫn có giá trị

Một policy đơn giản có thể rất mạnh nếu hệ thống cần predictability. Trong môi trường production, một rule dễ giải thích đôi khi tốt hơn một policy adaptive khó debug. Baseline cũng giúp phát hiện bug: nếu một policy phức tạp không thắng được wait-k trên ví dụ rõ ràng, ta cần xem lại implementation hoặc metric.

## Điều cần giữ lại

Wait-k và fixed chunk là hai cách kiểm soát latency bằng rule cố định. Chúng không hiểu nội dung, nhưng giúp ta thiết lập nền so sánh rõ ràng trước khi dùng adaptive policy.
