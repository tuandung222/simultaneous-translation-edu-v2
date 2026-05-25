---
title: Syllabus
---

# Syllabus

## Mục tiêu khóa học

Khóa học giúp người học hiểu simultaneous text-to-text translation như một bài toán streaming sequence generation có ràng buộc latency. Người học không chỉ chạy được code, mà còn đọc được trace, hiểu metric và thiết kế policy mới một cách có kiểm soát.

## Đối tượng phù hợp

- Người đã biết cơ bản về deep learning và sequence modeling.
- Người từng học machine translation hoặc text generation ở mức khái niệm.
- Người muốn có một repo nhỏ để dạy, live-code hoặc tự học về latency-quality tradeoff.
- Người làm NLP, speech, streaming UX hoặc agent systems muốn hiểu khái niệm commitment under partial information.

## Lộ trình học

| Phần | Chủ đề | Mục tiêu |
|---|---|---|
| Phần 0 | Định hướng | Hiểu vì sao simultaneous translation là bài toán tốt để học streaming decisions |
| Phần 1 | Nền tảng bài toán | Phân biệt offline và simultaneous translation, hiểu `READ`, `WRITE`, source prefix và commitment |
| Phần 2 | Metrics | Đọc latency trace, tính AP, AL và diễn giải tradeoff với quality |
| Phần 3 | Policy design | So sánh wait-k, fixed chunk, local agreement và confidence threshold |
| Phần 4 | Model và training | Hiểu synthetic data, seq2seq attention và prefix decoding mismatch |
| Phần 5 | Labs | Chạy demo, thay policy, thêm metric, stress-test data |
| Phần 6 | Nghiên cứu mở rộng | Kết nối toy repo với prefix training, learned policy, streaming attention và LLM streaming |

## Nhịp học đề xuất

Nếu học nhanh, bạn có thể đọc Phần 0 đến Phần 3 trước, sau đó chạy lab để nhìn trace. Nếu dạy trên lớp, mỗi phần có thể thành một buổi 90 đến 120 phút kèm live coding.

Một nhịp tốt cho mỗi buổi là:

1. mở bằng một ví dụ source-target cụ thể;
2. hỏi token nào có thể phát sớm và token nào cần chờ;
3. formalize bằng notation;
4. map notation vào code;
5. chạy một experiment nhỏ;
6. đọc trace và giải thích tradeoff.

## Deliverables

Sau khóa học, người học nên nộp được một trong các sản phẩm:

- một policy mới có test;
- một metric latency hoặc stability mới;
- một synthetic data pattern làm policy hiện tại hỏng;
- một báo cáo ngắn so sánh hai policy trên cùng ví dụ;
- một extension proposal nối toy repo với speech translation hoặc LLM streaming.
