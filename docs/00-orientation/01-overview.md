---
title: Tổng quan khóa học
---

# Tổng quan khóa học

Simultaneous translation đặt ra một câu hỏi rất khác với dịch máy offline. Nếu dịch offline giống như đọc xong toàn bộ câu rồi mới dịch, thì dịch đồng thời giống như vừa nghe vừa phải nói. Người dịch, hoặc hệ thống dịch, không có toàn bộ thông tin tương lai. Mỗi lần phát ra một từ, hệ thống đang cam kết với một lựa chọn có thể không dễ sửa lại.

Điểm làm bài toán này thú vị là nó nằm giữa ba thế giới: sequence modeling, decision making và system latency. Một mô hình có thể dịch đúng khi nhìn thấy toàn câu, nhưng vẫn hoạt động tệ khi chỉ được nhìn thấy prefix. Ngược lại, một policy có thể giảm độ trễ rất mạnh, nhưng làm hệ thống phát ra token quá sớm và sai ở những vị trí quan trọng.

## Khóa học này dạy gì

Khóa học đi theo một đường học có chủ ý:

1. Hiểu sự khác nhau giữa offline translation và simultaneous translation.
2. Biểu diễn hệ thống bằng hai hành động `READ` và `WRITE`.
3. Đọc latency trace `g(t)` để biết mỗi target token được phát ra sau bao nhiêu source token.
4. Tính Average Proportion, Average Lagging và quality score đơn giản.
5. So sánh các policy như wait-k, fixed chunk, local agreement và confidence threshold.
6. Quan sát code PyTorch nhỏ để nối lý thuyết với implementation.
7. Tự mở rộng policy, metric hoặc synthetic data để thấy tradeoff thay đổi ra sao.

## Vì sao không bắt đầu bằng model lớn

Một khóa học tốt không nhất thiết bắt đầu bằng hệ thống mạnh nhất. Nếu mục tiêu là học cơ chế, ta cần một môi trường đủ nhỏ để nhìn thấy từng quyết định. Repo này dùng synthetic data, GRU encoder-decoder và attention đơn giản không phải vì đó là state of the art, mà vì mọi thành phần đều có thể được đọc, chạy, sửa và kiểm tra.

Khi người học nhìn thấy một policy phát token quá sớm, họ có thể truy ngược lại: tại thời điểm đó source prefix là gì, hypothesis là gì, confidence là bao nhiêu, read position là mấy, và metric latency phản ánh điều đó thế nào. Đó là kiểu hiểu khó có được nếu ta bắt đầu bằng một hệ thống lớn không quan sát được.

## Kết quả mong đợi

Sau khóa học, bạn nên có khả năng giải thích simultaneous translation như một bài toán điều khiển thời điểm phát token. Bạn cũng nên biết vì sao model và policy là hai lớp khác nhau: model trả lời “token nào có vẻ hợp lý”, còn policy trả lời “đã đủ an toàn để phát token đó chưa”.

Quan trọng hơn, bạn sẽ có một codebase nhỏ để tự thử nghiệm. Bạn có thể thay `wait-k`, thêm một policy mới, làm metric khác, hoặc tăng độ khó của synthetic grammar để xem hệ thống hỏng theo cách nào.
