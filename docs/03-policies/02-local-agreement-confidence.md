---
title: Local Agreement và Confidence
---

# Chiến lược thích ứng (Adaptive Policies): Local Agreement và Confidence

Chào các bạn! Nếu như *Wait-k* và *Fixed Chunk* (Chiến lược Tĩnh) giống như một cái máy metronome gõ nhịp đều đặn mù quáng, thì hôm nay chúng ta sẽ tìm hiểu về các **Chiến lược Thích ứng (Adaptive Policies)**.

Đây là những bộ Policy có "tri giác". Chúng biết "đọc bầu không khí": nếu nguồn và đích đang có ngữ pháp xuôi chiều, chúng sẽ dịch liên tục với độ trễ sát nút 0. Nhưng ngay khi phát hiện cụm từ phức tạp, chúng tự động ghìm lại, trì hoãn lệnh `WRITE` và ra lệnh `READ` để nạp thêm ngữ cảnh.

Trong bài này, chúng ta sẽ mổ xẻ hai cơ chế Adaptive nổi tiếng nhất: **Local Agreement (Sự đồng thuận cục bộ)** và **Confidence Threshold (Ngưỡng tự tin)**.

---

## 1. Local Agreement (Sự đồng thuận cục bộ)

### Ý Tưởng Cốt Lõi (Liu et al., 2020)
Giả sử bạn đang làm bài thi trắc nghiệm. Bạn chưa đọc hết câu hỏi nhưng đã đoán đáp án là A. Sau khi đọc thêm một cụm từ nữa, bạn vẫn thấy đáp án A là đúng. Bạn đọc thêm một cụm nữa, đáp án vẫn là A. Khi nào bạn nộp bài? Chắc chắn là khi linh cảm của bạn được *xác nhận (agree)* qua nhiều bước liên tiếp.

**Local Agreement** mô phỏng y hệt tâm lý đó. Hệ thống sẽ luôn thử dự đoán xem từ tiếp theo nên dịch là gì. Nếu sau $N$ lần đọc thêm (READ) từ vựng nguồn mà dự đoán (hypothesis) của mô hình về từ đích đó *không hề thay đổi*, hệ thống sẽ xem như nó đã "chốt" được và an tâm phát nó ra (WRITE).

### Cơ Chế Hoạt Động

Tham số duy nhất của thuật toán này là ngưỡng chờ $N$ (Ví dụ: $N=2$).

1. Tại bước hiện tại, hệ thống đã đọc $i$ token nguồn. Mô hình dự đoán token tiếp theo là $y_A$.
2. Hệ thống gọi `READ`, đọc thêm token $i+1$. Mô hình dự đoán lại. Nếu kết quả vẫn là $y_A$, ta có chuỗi đồng thuận dài 2.
3. Nếu $N=2$, hệ thống kết luận: "Ok, qua 2 lần thêm thông tin mà đáp án vẫn không đổi, chứng tỏ từ $y_A$ này rất chắc chắn." -> Gọi lệnh `WRITE(y_A)`.
4. Nếu tại bước 2, mô hình đổi ý sang $y_B$, chuỗi đồng thuận bị "gãy" về 0. Hệ thống lại phải gọi `READ` và bắt đầu tích lũy lại chuỗi đồng thuận.

### Minh họa bằng Mermaid (Với $N=2$)

```mermaid
flowchart TD
    Start[Trạng thái hiện tại: Đã đọc x_i] --> Pred1{Dự đoán y_target là gì?}
    Pred1 -- "Gợi ý: 'Apple'" --> Read1[READ: Đọc thêm x_{i+1}]
    Read1 --> Pred2{Dự đoán lại có đổi ý không?}

    Pred2 -- "Đổi ý thành 'Banana'!" --> Reset[Reset chuỗi đồng thuận = 0]
    Reset --> Read1

    Pred2 -- "Vẫn là 'Apple'" --> Agree[Chuỗi đồng thuận = 2. Đạt ngưỡng N=2]
    Agree --> Write[WRITE: Phát ra 'Apple']
```

**Ưu điểm:** Phương pháp này phản ứng cực nhạy với điểm "delayed evidence" (bằng chứng bị trì hoãn) mà ta đã bàn ở chương 1. Khi chưa có đủ bằng chứng, mô hình dự đoán sẽ nhảy múa liên tục, Local Agreement sẽ liên tục giữ lệnh READ. Khi bằng chứng cốt lõi xuất hiện, dự đoán ổn định lại, `WRITE` sẽ được kích hoạt.

---

## 2. Confidence Threshold (Ngưỡng tự tin)

### Ý Tưởng Cốt Lõi
Nếu bạn để ý, Local Agreement cần phải gọi `READ` tốn tài nguyên chỉ để "test" xem dự đoán có thay đổi không. Các nhà nghiên cứu tự hỏi: *Mô hình Neural Network sinh ra phân bố xác suất Softmax. Tại sao ta không dùng chính cái xác suất ấy làm độ đo tự tin?*

**Confidence Policy** cực kỳ trực diện:
"Nếu mô hình dự đoán từ đích tiếp theo với xác suất vượt qua một ngưỡng $\beta$ (ví dụ 85%), tôi sẽ WRITE ngay. Nếu dưới 85%, tôi cảm thấy không an tâm $\implies$ READ tiếp."

### Cơ Chế Hoạt Động

Tham số điều khiển là Threshold $\beta \in [0, 1]$.

Tại mỗi bước, mô hình tính toán xác suất $p = P(y_t | x_{\le i}, y_{<t})$ cho token có xác suất cao nhất.
- Nếu $p \ge \beta$: Gọi `WRITE`.
- Nếu $p < \beta$: Gọi `READ`. (Sau khi READ, do có thêm thông tin, xác suất cho token đúng thường sẽ tăng lên cho đến khi vượt ngưỡng $\beta$).

### Tại Sao Confidence Đôi Khi Thất Bại? (Overconfidence Issue)

Nghe có vẻ hoàn hảo, nhưng Confidence Threshold gặp phải một "gót chân Achilles" vô cùng nổi tiếng trong Deep Learning: **Neural Networks are Overconfident!** (Mạng nơ-ron luôn tự tin thái quá).

Do được huấn luyện bằng hàm mất mát Cross-Entropy, mô hình có xu hướng đẩy xác suất của dự đoán lên tiệm cận 100% kể cả khi nó đang sai bét (hallucination).

**Ví dụ thực tế:**
Source đang nói: `The President of...`
Model ngôn ngữ đã "học vẹt" quá nhiều tin tức, nên nó lập tức gắn xác suất 99% cho từ `America`, mặc dù nguồn còn chưa nói hết!
Nếu $\beta = 0.95$, Policy sẽ hồn nhiên `WRITE` chữ "America". Nhưng vài mili-giây sau, source hiện ra: `The President of France`. Hệ thống vỡ trận.

### Giải pháp khắc phục Overconfidence
Để khắc phục, các nhà nghiên cứu thường không dùng trực tiếp Softmax thô, mà sử dụng các kỹ thuật như:
1. **Entropy của phân bố xác suất:** Thay vì chỉ nhìn token top 1, ta đo độ "phân tán" của toàn bộ từ điển. Entropy cao nghĩa là mô hình đang phân vân giữa nhiều lựa chọn $\rightarrow$ READ.
2. **Train một module Confidence riêng rẽ:** Huấn luyện một phân hệ nhỏ (classifier) chuyên làm nhiệm vụ đánh giá xem "Mô hình dịch đang bốc phét hay đang nói thật" dựa trên hidden states.

## Bức Tranh Tổng Thể Về Policies

Đến đây, bạn đã nắm trong tay "Tứ đại pháp bảo" của bộ định tuyến dịch đồng thời:
1. **Wait-k:** Dễ cài đặt, kiểm soát độ trễ tuyệt đối, nhưng mù quáng.
2. **Fixed Chunk:** Gom khối tốt cho âm thanh, nhưng thiếu linh hoạt ngữ nghĩa.
3. **Local Agreement:** Phát hiện "dấu hiệu ngập ngừng" của mô hình rất tinh tế, nhưng tốn kém tính toán (phải sinh ra tương lai để test).
4. **Confidence Threshold:** Ra quyết định siêu nhanh, linh hoạt, nhưng phải vật lộn với "ảo giác tự tin" của Deep Learning.

Một hệ thống dịch đồng thời tinh hoa trong thực tế (như ở các hội nghị lớn) thường không dùng lẻ loi một chiến lược nào, mà là một cơ chế lai (Hybrid) kết hợp sự kiên định của Wait-k (như một Safety net - lưới an toàn) và sự linh hoạt của Confidence!
