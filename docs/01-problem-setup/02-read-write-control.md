---
title: READ, WRITE và sequential decision view
---

# READ, WRITE và sequential decision view

Một cách nhìn rất hữu ích là xem simultaneous translation như một chuỗi hành động. Tại mỗi bước, hệ thống chọn một trong hai hành động:

- `READ`: đọc thêm một source token.
- `WRITE`: phát ra một target token.

Chuỗi hành động có thể trông như sau:

```text
READ, READ, WRITE, READ, WRITE, WRITE, READ, WRITE
```

Dãy này cho ta nhiều thông tin hơn câu dịch cuối cùng. Nó cho biết hệ thống đã chờ bao lâu trước mỗi token, phát có đều không, có bursty không, và token nào được phát khi source context còn thiếu.

## State tại một thời điểm

Tại mỗi thời điểm, state tối thiểu cần biết gồm:

- đã đọc bao nhiêu source token;
- đã commit bao nhiêu target token;
- hypothesis hiện tại của model khi chỉ nhìn source prefix;
- confidence của các token trong hypothesis nếu model cung cấp;
- source đã kết thúc chưa.

Trong code, các thông tin này được gom vào `PolicyContext`. Policy không cần biết toàn bộ chi tiết bên trong model. Nó chỉ cần đủ tín hiệu để quyết định `READ` hay `WRITE`.

## Model khác policy như thế nào

Đây là điểm người học rất dễ nhầm. Model và policy không phải cùng một thứ.

Model trả lời: với source prefix hiện tại, target sequence nào có vẻ hợp lý? Nó tạo hypothesis và có thể trả confidence. Policy trả lời: token tiếp theo trong hypothesis đã đủ ổn định để phát chưa?

Một model mạnh hơn có thể làm hypothesis tốt hơn, nhưng không tự động giải quyết timing. Nếu target token phụ thuộc vào source tương lai, model vẫn có thể tự tin sai khi chỉ thấy prefix. Ngược lại, một policy quá bảo thủ có thể làm latency cao dù model đã đủ tốt.

## Vì sao tách hai lớp này

Tách model và policy giúp repo trở thành môi trường học rõ ràng. Ta có thể giữ model cố định rồi thay policy để thấy latency-quality tradeoff thay đổi. Ta cũng có thể giữ policy cố định rồi thay model để xem model confidence và hypothesis stability thay đổi ra sao.

Trong engineering, separation of concerns này rất quan trọng. Nếu mọi logic timing bị trộn vào model, ta khó debug. Khi một ví dụ hỏng, ta không biết lỗi đến từ khả năng dịch, calibration, hay rule commit.

## Điều cần giữ lại

Simultaneous translation có thể được xem như một policy điều khiển `READ` và `WRITE` trên nền một sequence model. Muốn debug hệ thống, hãy nhìn trace hành động, source prefix, hypothesis và read positions, không chỉ nhìn câu dịch cuối cùng.
