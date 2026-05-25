---
title: Glossary
---

# Glossary

## Simultaneous translation

Dịch đồng thời, trong đó hệ thống phát target trong khi source vẫn đang đến. Khác với offline translation, hệ thống không nhất thiết thấy toàn bộ source trước khi bắt đầu sinh target.

## Source prefix

Phần source đã được đọc tại một thời điểm. Nếu toàn bộ source là `x_1, ..., x_n`, prefix có thể là `x_1, ..., x_i` với `i < n`.

## READ

Hành động đọc thêm source token. `READ` thường giảm rủi ro sai vì có thêm context, nhưng tăng latency.

## WRITE

Hành động phát một target token. `WRITE` giảm thời gian chờ của người dùng, nhưng tạo commitment risk nếu source tương lai làm token đó sai.

## Policy

Rule hoặc model quyết định bước tiếp theo là `READ` hay `WRITE`. Trong repo này, policy được tách khỏi model dịch để dễ so sánh và debug.

## Hypothesis

Chuỗi target mà model hiện tại dự đoán từ source prefix. Hypothesis có thể thay đổi khi source prefix dài hơn.

## Local agreement

Policy chỉ commit phần prefix target ổn định qua nhiều lần decode. Nếu hypothesis mới và cũ có prefix chung, phần đó được xem là an toàn hơn để phát.

## Confidence threshold

Policy phát token nếu confidence của token vượt một ngưỡng. Cách này đơn giản nhưng phụ thuộc vào calibration của model.

## Wait-k

Policy đọc `k` source tokens trước, sau đó giữ độ trễ tương đối đều giữa source và target. Đây là baseline quan trọng trong simultaneous translation.

## Average Proportion

Metric đo trung bình tỷ lệ source đã đọc trước khi phát target tokens. AP thấp thường tương ứng latency thấp hơn.

## Average Lagging

Metric so sánh reading curve thực tế với một đường đọc lý tưởng có tốc độ đều. AL giúp diễn giải hệ thống đang tụt lại bao nhiêu so với ideal policy.

## Commitment risk

Rủi ro xảy ra khi hệ thống phát token quá sớm và sau đó phát hiện token đó không phù hợp với source đầy đủ.

## Prefix decoding mismatch

Sự lệch giữa training bằng full source và inference bằng source prefix. Đây là lý do model offline tốt vẫn có thể bất ổn trong simultaneous decoding.
