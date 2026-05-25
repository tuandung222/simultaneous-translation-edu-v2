# Syllabus: Simultaneous Translation Text-to-Text

## Mục tiêu khóa học

Khóa học xây dựng nền tảng khái niệm và năng lực implementation để người học có thể giải thích, chạy, sửa và mở rộng một hệ thống simultaneous translation nhỏ từ đầu đến cuối.

Trọng tâm không phải là đạt benchmark cao. Trọng tâm là hiểu vì sao một hệ thống dịch đồng thời phải quyết định dưới điều kiện thiếu thông tin tương lai, và vì sao latency-quality tradeoff cần được đo bằng cả trace lẫn metric.

## Đối tượng học

- Người đã biết cơ bản về deep learning.
- Người đã gặp sequence-to-sequence model ở mức khái niệm.
- Người muốn một lộ trình nhỏ gọn từ lý thuyết đến code chạy được.
- Người quan tâm tới streaming NLP, speech translation, realtime UX hoặc agentic generation.

## Điều kiện tiên quyết

- Python và PyTorch cơ bản.
- Embedding, RNN, attention và teacher forcing.
- Tokenization, padding và batching.
- Tư duy đánh giá cơ bản cho sequence generation.

## Hình thức khóa học

Khóa học gồm sáu buổi, mỗi buổi phù hợp cho 90 đến 120 phút. Mỗi buổi nên có ba phần: trực giác, formalization và lab nhỏ.

## Lộ trình bài học

### Bài 1. Problem framing

Người học phân biệt offline translation và simultaneous translation, hiểu `READ`, `WRITE`, source prefix và commitment risk.

Sản phẩm đầu ra: người học có thể formalize task và giải thích tradeoff giữa latency và quality.

### Bài 2. Metrics and tradeoffs

Người học hiểu vì sao quality metric đơn lẻ là không đủ, biết đọc latency trace, tính Average Proportion và Average Lagging.

Sản phẩm đầu ra: người học có thể tính và diễn giải latency metrics từ một token emission trace.

### Bài 3. Policy design

Người học so sánh fixed policies và adaptive policies, bao gồm wait-k, chunk-based policy, local agreement và confidence-based policy.

Sản phẩm đầu ra: người học có thể mô tả mỗi policy dùng tín hiệu gì và đánh đổi điều gì.

### Bài 4. Model design for the repo

Người học hiểu vì sao repo dùng toy seq2seq model, synthetic data, controlled reordering và prefix decoding.

Sản phẩm đầu ra: người học có thể map notation trong bài học vào PyTorch modules cụ thể.

### Bài 5. Implementation practicum

Người học chạy training loop, decode trên source prefix, cắm policy vào shared runner và đo quality cùng latency.

Sản phẩm đầu ra: người học có thể chạy experiment và sửa code có kiểm soát.

### Bài 6. Beyond the baseline

Người học hiểu giới hạn của toy repo và liên hệ với prefix training, learned policies, simultaneous speech translation và LLM streaming.

Sản phẩm đầu ra: người học có thể viết một proposal mở rộng từ baseline sang hệ thống nghiên cứu nghiêm túc hơn.

## Gợi ý đánh giá

- Coding exercise: implement một policy mới.
- Analysis exercise: so sánh hai policy trên cùng một sentence và giải thích trace.
- Essay exercise: lập luận khi nào giảm latency đáng đánh đổi bằng giảm quality.
- Research exercise: thiết kế một stress test cho delayed evidence.

## Milestones gắn với repo

1. Đọc giáo trình và chạy lại example.
2. Thay synthetic grammar và quan sát policy behavior.
3. Implement một adaptive policy bổ sung.
4. Thêm một metric mới để đo stability hoặc burstiness.
5. Viết báo cáo ngắn kết nối toy system với một hướng nghiên cứu thật.
