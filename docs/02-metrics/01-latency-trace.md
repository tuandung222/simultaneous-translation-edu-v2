---
title: Latency trace g(t)
---

# Latency trace g(t)

Trước khi tính metric, ta cần một đối tượng rất đơn giản: latency trace. Với mỗi target token `y_t`, ta ghi lại hệ thống đã đọc bao nhiêu source token tại thời điểm phát token đó. Con số này được ký hiệu là `g(t)`.

Nếu source có độ dài `n = 5`, target có độ dài `m = 4`, một trace có thể là:

```text
g(1) = 2
g(2) = 4
g(3) = 5
g(4) = 5
```

Đọc theo nghĩa đời thường: target token đầu tiên được phát sau khi hệ thống đã đọc 2 source token. Token thứ hai được phát sau 4 source token. Hai token cuối chỉ được phát khi source đã đọc hết.

## Trace nói điều mà câu dịch cuối không nói

Hai hệ thống có thể sinh cùng một câu dịch cuối, nhưng trải nghiệm người dùng rất khác. Một hệ thống có thể phát đều từng token khi source đến. Hệ thống khác có thể im lặng gần hết câu rồi phát toàn bộ target ở cuối. Nếu chỉ nhìn final quality, ta không phân biệt được hai hành vi đó.

Trace `g(t)` làm timeline trở nên đo được. Nó cho phép ta hỏi: token quan trọng được phát sớm hay muộn? Hệ thống có chờ đến khi source kết thúc không? Có đoạn nào phát quá nhanh sau một khoảng im lặng dài không?

## Quan hệ giữa trace và policy

Policy quyết định hình dạng của trace. Wait-k thường tạo trace đều và dễ phân tích. Fixed chunk tạo trace theo từng đợt. Local agreement có thể chờ lâu ở những prefix bất ổn. Confidence threshold có thể phát sớm nếu model tự tin, nhưng sẽ dừng lại khi confidence thấp.

Vì vậy, khi so sánh policy, ta không nên chỉ nhìn một con số AP hoặc AL. Ta nên đọc cả trace để hiểu policy đã hành xử như thế nào.

## Trong code repo này

Trong `SimultaneousResult`, trường `read_positions` chính là trace cho các target token đã phát. Khi script in kết quả, bạn sẽ thấy dòng như:

```text
read_positions=[2, 4, 5, 5]
```

Đó là dữ liệu đầu vào để tính Average Proportion và Average Lagging.

## Điều cần giữ lại

`g(t)` là cầu nối giữa quyết định streaming và metric latency. Nếu không đọc được trace, ta sẽ dễ hiểu sai kết quả. Metric chỉ là bản tóm tắt, còn trace cho ta thấy câu chuyện của từng token.
