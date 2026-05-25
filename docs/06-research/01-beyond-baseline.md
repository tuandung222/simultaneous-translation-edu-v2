---
title: Từ toy repo tới nghiên cứu thật
---

# Từ toy repo tới nghiên cứu thật

Repo này cố ý nhỏ. Điều đó giúp học cơ chế, nhưng cũng có giới hạn rõ ràng. Khi chuyển sang research system thật, ta cần mở rộng cả model, training objective, policy và evaluation.

## Prefix-to-prefix training

Trong repo, model được train chủ yếu như một offline seq2seq model. Khi simultaneous decoding, model phải decode từ source prefix. Đây là mismatch lớn. Research system thường dùng prefix-to-prefix training hoặc objective latency-aware để model quen với partial source.

Ý tưởng chung là không chỉ dạy model dịch khi thấy toàn câu, mà dạy nó sinh target hợp lý ở nhiều mức source prefix khác nhau.

## Learned policy

Hand-designed policy dễ hiểu, nhưng có giới hạn. Learned policy có thể dùng reinforcement learning, imitation learning hoặc differentiable objectives để học khi nào nên `READ` và `WRITE`.

Tuy nhiên learned policy khó debug hơn. Nó cần reward hoặc objective cân bằng quality và latency. Nếu reward thiết kế kém, policy có thể học hành vi nhìn tốt trên metric nhưng tệ với người dùng.

## Streaming attention

Một hướng khác là thay attention full-context bằng attention có ràng buộc monotonic hoặc streaming. Mục tiêu là làm architecture phù hợp hơn với input đến dần. Điều này đặc biệt quan trọng khi chuyển từ text-to-text sang speech translation, nơi acoustic frames đến theo thời gian.

## Evaluation thật

Token F1 trong repo chỉ là metric toy. Hệ thống thật cần đánh giá bằng nhiều lớp:

- quality metrics như BLEU, chrF, COMET hoặc human rating;
- latency metrics như AP, AL hoặc biến thể phù hợp speech;
- stability metrics nếu output có revision;
- user-facing metrics như smoothness, burstiness và perceived delay.

Không có một metric đơn lẻ nào đủ để đại diện toàn bộ trải nghiệm.

## Liên hệ với LLM streaming

Dù repo nói về translation, tư duy timing cũng xuất hiện trong LLM streaming. Một assistant có thể stream token quá sớm rồi phải sửa ý. Một agent có thể gọi tool quá sớm khi chưa đủ context. Một hệ thống retrieval có thể trả lời trước khi bằng chứng quan trọng được retrieved.

Vì vậy, bài học rộng hơn là: trong mọi hệ thống generation có thời gian, ta cần tách prediction khỏi commitment. Biết nói gì là một chuyện. Biết khi nào nên nói là chuyện khác.

## Điều cần giữ lại

Toy repo là điểm xuất phát, không phải đích đến. Nó cho ta ngôn ngữ để nói về latency, policy và trace. Khi sang nghiên cứu thật, các thành phần sẽ phức tạp hơn, nhưng câu hỏi nền vẫn giữ nguyên: hệ thống đã có đủ bằng chứng để commit output chưa?
