---
title: Offline translation và simultaneous translation
---

# Offline translation và simultaneous translation

Hãy bắt đầu từ dịch máy quen thuộc. Trong offline machine translation, hệ thống nhận toàn bộ source sentence rồi mới sinh target sentence. Nếu source là `x = (x_1, x_2, ..., x_n)`, mô hình có thể dùng mọi token từ `x_1` đến `x_n` trước khi quyết định target `y = (y_1, y_2, ..., y_m)`.

Simultaneous translation thay đổi điều kiện thông tin. Tại thời điểm sinh `y_t`, hệ thống có thể chỉ thấy một prefix `x_{\le i}`. Phần còn lại của source chưa đến, hoặc đến nhưng hệ thống chưa kịp xử lý. Vì vậy bài toán không còn là “dịch câu này tốt nhất có thể” mà là “vừa đọc vừa quyết định khi nào nên nói”.

## Cam kết sớm tạo ra rủi ro

Trong giao diện streaming, một target token khi đã phát ra thường được xem là đã cam kết. Nếu sau đó source tiếp tục đến và làm token đó trở nên sai, hệ thống có ba lựa chọn đều không hoàn hảo: sửa lại output, phát thêm giải thích, hoặc chấp nhận lỗi. Với phụ đề trực tiếp, hội nghị đa ngôn ngữ, hoặc trợ lý hội thoại thời gian thực, cả ba đều có chi phí trải nghiệm.

Câu hỏi cốt lõi là: hệ thống nên chờ bao lâu? Chờ lâu giúp chất lượng tốt hơn vì có nhiều source context. Nhưng chờ quá lâu làm mất ý nghĩa của simultaneous translation. Phát sớm giúp latency thấp hơn, nhưng tăng nguy cơ hallucination, sai thứ tự, hoặc sai đối tượng.

## Một ví dụ nhỏ

Giả sử source theo thứ tự:

```text
subject verb adjective object time
```

Nhưng target cần thứ tự:

```text
subject object adjective time verb
```

Target token thứ hai cần object. Trong source, object lại đến sau verb và adjective. Nếu hệ thống phải phát target token thứ hai quá sớm, nó có thể chưa thấy object. Đây là delayed evidence, tức bằng chứng cần thiết đến muộn hơn vị trí ta muốn phát trong target.

## Ba khó khăn chính

Khó khăn thứ nhất là delayed evidence. Một token target có thể phụ thuộc vào source token chưa đến. Khó khăn thứ hai là reordering. Source và target không nhất thiết cùng thứ tự thông tin. Khó khăn thứ ba là commitment risk. Một token phát ra sớm có thể gây lỗi không dễ sửa trong giao diện người dùng.

Ba khó khăn này biến simultaneous translation thành bài toán vừa dự đoán vừa điều khiển. Prediction trả lời token nào nên sinh. Control trả lời khi nào nên sinh token đó.

## Điều cần giữ lại

Offline translation tối ưu câu dịch sau khi đã thấy toàn bộ source. Simultaneous translation tối ưu một quá trình phát token dưới điều kiện thiếu thông tin tương lai. Vì vậy, chỉ đo final accuracy là chưa đủ. Ta cần đo cả latency và đọc được timeline ra quyết định của hệ thống.
