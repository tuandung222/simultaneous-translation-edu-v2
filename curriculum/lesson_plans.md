# Lesson Plans

## Bài 1. Problem framing

### Mục tiêu giảng dạy

Người học hiểu simultaneous translation như một bài toán điều khiển đặt trên nền sequence generation. Điểm cần nhấn mạnh là hệ thống không chỉ dự đoán token đúng, mà còn phải quyết định khi nào token đó đủ an toàn để commit.

### Dòng triển khai trên lớp

1. Mở bằng ví dụ phụ đề trực tiếp: nếu chờ quá lâu thì người xem khó theo dõi, nếu phát quá sớm thì dễ sai.
2. Định nghĩa source stream `x_1, x_2, ..., x_n` và target stream `y_1, y_2, ..., y_m`.
3. Giới thiệu hai hành động `READ` và `WRITE`.
4. Vẽ một timeline nhỏ để thấy token target được phát tại source position nào.
5. Thảo luận hai failure modes: latency thấp nhưng hallucination, hoặc quality cao nhưng delay không chấp nhận được.

### Bài tập tại lớp

Cho một câu mà object xuất hiện muộn trong source nhưng cần xuất hiện sớm trong target. Yêu cầu người học mô phỏng thủ công `wait-1`, `wait-3` và offline decoding.

### Bài đọc

Đọc `/docs/01-problem-setup/01-offline-vs-simultaneous` và tóm tắt vai trò của commitment risk.

## Bài 2. Metrics and tradeoffs

### Mục tiêu giảng dạy

Người học biết tính latency bằng số, thay vì chỉ nói theo trực giác “nhanh” hoặc “chậm”.

### Dòng triển khai trên lớp

1. Ôn lại `g(t)`: hệ thống đã đọc bao nhiêu source tokens khi phát target token thứ `t`.
2. Tính Average Proportion từ một trace nhỏ.
3. Tính Average Lagging và giải thích ideal policy có slope đều.
4. So sánh hai hệ thống có cùng final translation nhưng khác latency trace.
5. Thảo luận blind spots của metric trung bình.

### Bài tập tại lớp

Cho trace `g = [2, 4, 5, 5]`, source length `5`, target length `4`. Yêu cầu người học tính AP và AL, sau đó giải thích trace này có trải nghiệm như thế nào.

### Bài đọc

Đọc `/docs/02-metrics/01-latency-trace` và `/docs/02-metrics/02-average-proportion-average-lagging`.

## Bài 3. Policy design

### Mục tiêu giảng dạy

Người học phân biệt model uncertainty và policy conservatism. Một model tự tin không có nghĩa token đã an toàn để phát.

### Dòng triển khai trên lớp

1. Bắt đầu với fixed policies: wait-k và chunked read.
2. Chuyển sang adaptive policies: local agreement và confidence thresholding.
3. Lập bảng tín hiệu mà từng policy sử dụng: source position, hypothesis stability, token confidence.
4. Phân tích vì sao local agreement thường robust nhưng có thể bảo thủ.
5. Phân tích vì sao confidence threshold có thể aggressive nhưng phụ thuộc calibration.

### Demo tại lớp

Chạy cùng một source prefix sequence qua nhiều policy và hiển thị token commits, `read_positions`, AP, AL và F1.

### Bài đọc

Đọc `/docs/03-policies/01-wait-k-fixed-chunk` và `/docs/03-policies/02-local-agreement-confidence`. Viết một đoạn ngắn về khi nào confidence thresholding có thể thất bại.

## Bài 4. Model design

### Mục tiêu giảng dạy

Người học hiểu vì sao repo dùng mô hình nhỏ và inspectable. Mô hình không nhằm cạnh tranh benchmark, mà nhằm làm rõ interaction giữa source prefix, hypothesis và policy.

### Dòng triển khai trên lớp

1. Giới thiệu synthetic dataset với delayed target dependencies.
2. Xem source vocabulary và target vocabulary.
3. Giải thích encoder unidirectional.
4. Giải thích attention ở mức shape và intuition.
5. Giải thích decoder với teacher forcing.
6. Nhấn mạnh prefix decoding mismatch: train trên full source, test trên partial source.

### Trọng tâm bảng trắng

- Tensor shapes cho encoder outputs.
- Attention score computation.
- Vì sao partial-source decoding tạo distribution shift.

### Bài đọc

Đọc `/docs/04-model-training/01-synthetic-data` và `/docs/04-model-training/02-seq2seq-attention`, sau đó annotate training loop trong `src/simulst_edu/train.py`.

## Bài 5. Implementation practicum

### Mục tiêu giảng dạy

Người học có thể mở rộng code mà không phá evaluation loop.

### Dòng triển khai trên lớp

1. Walk through data generation.
2. Build vocabularies.
3. Train model.
4. Run simultaneous decoding.
5. Log quality và latency metrics.
6. Compare trajectories giữa các policy.

### Lab task

Implement một policy mới có ít nhất một internal state variable. Viết test cho behavior chính và chạy policy đó trong `examples/compare_policies.py`.

### Bài đọc

Hoàn thành bài trong `/docs/05-labs/01-run-the-lab` và `/docs/05-labs/02-extend-the-system`.

## Bài 6. Beyond the baseline

### Mục tiêu giảng dạy

Người học hiểu toy project dừng ở đâu và cần gì để tiến tới research system thật.

### Dòng triển khai trên lớp

1. Prefix-to-prefix training objectives.
2. Learned agents so với hand-designed policies.
3. Beam search trong streaming settings.
4. Real benchmark considerations.
5. Liên hệ với speech translation, online ASR và LLM streaming.

### Bài cuối

Viết một báo cáo ngắn so sánh hai policy, chỉ ra một hạn chế của model, và đề xuất một hướng mở rộng có thể kiểm chứng bằng experiment.
