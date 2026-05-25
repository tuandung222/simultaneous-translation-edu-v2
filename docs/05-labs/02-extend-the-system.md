---
title: Mở rộng policy, metric và dữ liệu
---

# Mở rộng policy, metric và dữ liệu

Sau khi chạy lab cơ bản, bước học tốt nhất là sửa hệ thống theo một giả thuyết rõ ràng. Đừng bắt đầu bằng việc thay mọi thứ cùng lúc. Hãy chọn một lớp: policy, metric, data hoặc model.

## Thêm policy mới

Một policy mới nên trả lời bốn câu hỏi:

- Nó dùng tín hiệu nào?
- Nó lưu internal state gì?
- Khi nào nó trở nên aggressive hơn?
- Khi nào nó trở nên conservative hơn?

Ví dụ, bạn có thể tạo hybrid policy: chờ tối thiểu `k` source tokens, sau đó chỉ phát nếu confidence vượt threshold. Policy này kết hợp fixed lag và model signal.

## Thêm metric mới

AP và AL hữu ích nhưng không đủ. Bạn có thể thêm metric đo burstiness, ví dụ số lần hệ thống phát nhiều token liên tiếp sau một chuỗi `READ` dài. Metric này gần với trải nghiệm người dùng hơn trong một số giao diện.

Bạn cũng có thể thêm metric phạt token quan trọng bị trễ. Trong dịch thật, trễ một function word và trễ một content word không nên luôn được xem như nhau.

## Thay đổi synthetic data

Synthetic data là nơi dễ tạo stress test. Hãy thử:

- tăng xác suất adjective;
- tăng xác suất time word;
- tăng xác suất negation;
- tạo pattern source mà object xuất hiện rất muộn;
- tạo target order cần object rất sớm.

Sau đó so sánh policy nào degrade nhanh nhất. Một policy tốt trong setting dễ có thể hỏng rõ ràng khi reordering mạnh hơn.

## Khi nào nên thay model

Chỉ nên thay model khi bạn đã hiểu policy behavior trên model nhỏ. Nếu thay ngay sang transformer, bạn sẽ khó biết cải thiện đến từ architecture hay từ data size, training stability, tokenization, hoặc policy.

Một hướng mở rộng hợp lý là giữ API policy cũ, nhưng thay `Seq2SeqModel` bằng transformer encoder-decoder. Khi đó, lab vẫn đo cùng AP, AL và token F1, giúp so sánh công bằng hơn.

## Điều cần giữ lại

Mở rộng tốt bắt đầu từ một câu hỏi cụ thể. Nếu câu hỏi là “policy nào ổn định hơn khi reordering tăng”, hãy chỉ thay synthetic data và giữ các phần khác cố định. Nếu câu hỏi là “confidence có đáng tin không”, hãy log confidence và so với local agreement. Đó là cách biến repo thành công cụ nghiên cứu nhỏ.
