---
title: Average Proportion và Average Lagging
---

# Average Proportion và Average Lagging

Một hệ thống simultaneous translation cần được đánh giá trên ít nhất hai trục: chất lượng output và độ trễ phát token. Repo này dùng token F1 đơn giản cho chất lượng trong môi trường toy, và dùng hai latency metrics kinh điển: Average Proportion và Average Lagging.

## Average Proportion

Average Proportion, viết tắt là AP, đo trung bình hệ thống đã tiêu thụ bao nhiêu phần source trước khi phát mỗi target token.

Với source length `n`, target length `m`, và trace `g(t)`, công thức là:

```text
AP = (1 / (n * m)) * sum_{t=1}^{m} g(t)
```

Đọc công thức này theo nghĩa đời thường: lấy tổng số source tokens đã được đọc tại các thời điểm phát target, rồi chuẩn hóa theo kích thước tối đa `n * m`. AP càng thấp thì hệ thống càng có xu hướng phát sớm. AP càng cao thì hệ thống càng có xu hướng chờ.

Điểm mạnh của AP là dễ tính và dễ giải thích. Điểm yếu là nó có thể che mất vị trí delay. Hai trace khác nhau có thể có AP gần nhau nhưng trải nghiệm người dùng khác nhau.

## Average Lagging

Average Lagging, viết tắt là AL, so sánh reading curve thực tế với một policy lý tưởng có tốc độ đọc đều. Nếu target dài `m` và source dài `n`, ta đặt `gamma = m / n`. Một dạng thường dùng của AL là:

```text
AL = (1 / tau) * sum_{t=1}^{tau} (g(t) - (t - 1) / gamma)
```

Trong đó `tau` là bước target đầu tiên mà source đã được đọc hết, hoặc là `m` nếu điều đó không xảy ra sớm hơn. Ý tưởng chính không nằm ở ký hiệu, mà ở việc AL hỏi: so với một đường đọc lý tưởng, hệ thống đang bị tụt lại bao nhiêu?

AL hữu ích vì nó nhìn vào lag thay vì chỉ nhìn proportion. Tuy vậy, AL vẫn là một bản tóm tắt. Nó không thay thế việc đọc trace.

## Ví dụ tính tay

Giả sử:

```text
n = 5
m = 4
g = [2, 4, 5, 5]
```

Khi đó:

```text
AP = (2 + 4 + 5 + 5) / (5 * 4) = 0.8
```

Với AL, ta có `gamma = 4 / 5 = 0.8`. Nếu `tau = 3`, các điểm ideal cho `t = 1, 2, 3` là `0`, `1.25`, `2.5`. Do đó:

```text
AL = ((2 - 0) + (4 - 1.25) + (5 - 2.5)) / 3 = 2.4167
```

Giá trị cụ thể ít quan trọng hơn cách đọc: trace này chờ khá nhiều trước khi phát token.

## Quality score trong repo

Repo dùng token F1 dạng bag overlap để minh họa chất lượng. Đây không phải metric dịch máy production. Nó chỉ đủ để hỏi trong toy setting: predicted tokens có trùng với reference tokens ở mức nào?

Trong nghiên cứu thật, ta có thể dùng BLEU, chrF, COMET hoặc human evaluation. Nhưng cho mục tiêu học policy, metric đơn giản giúp ta tập trung vào tradeoff.

## Điều cần giữ lại

AP và AL giúp latency trở thành số đo được. Nhưng đừng để metric thay thế tư duy. Khi thấy một policy có AP thấp, hãy hỏi nó có phát sai token quan trọng không. Khi thấy AL cao, hãy nhìn trace để biết delay xảy ra ở đâu.
